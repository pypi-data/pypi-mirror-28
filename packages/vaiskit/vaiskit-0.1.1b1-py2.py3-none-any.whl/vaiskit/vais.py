import grpc
import vaiskit.speech.v1.cloud_speech_pb2_grpc as cloud_speech_pb2_grpc
import vaiskit.speech.v1.cloud_speech_pb2 as cloud_speech_pb2
import vaiskit.nlp.v1.cloud_nlp_pb2_grpc as cloud_nlp_pb2_grpc
import threading

try:
    import pyaudio
except Exception as e:
    print("You don't have pyaudio installed")
    exit(1)

CHUNK = 640
encoder = None
try:
    from speex import WBEncoder
    encoder = WBEncoder()
    encoder.quality = 10
    packet_size = encoder.frame_size
    CHUNK = packet_size
except Exception as e:
    print("******** WARNING ******************************************************")
    print("* You don't have pyspeex https://github.com/NuanceDev/pyspeex installed. You might suffer from low speed performance! *")
    print("")
    print("***********************************************************************")

from ctypes import *
from contextlib import contextmanager

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 15

class VaisService():
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "service.grpc.vais.vn:50051"
        self.channel = grpc.insecure_channel(self.url)
        self.channel.subscribe(callback=self.connectivity_callback, try_to_connect=True)
        self.stop = False
        self.stub = cloud_speech_pb2_grpc.SpeechStub(self.channel)
        self.stub_nlu = cloud_nlp_pb2_grpc.NLPStub(self.channel)
        self.asr_callback = None
        self.intent_callback = None

    def __enter__(self):
        with noalsaerr():
            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)
        return self

    def __exit__(self, *args):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def connectivity_callback(self, c):
        pass

    def generate_messages(self, app_id=None):
        sc = cloud_speech_pb2.SpeechContext(app_id=app_id)
        audio_encode = cloud_speech_pb2.RecognitionConfig.SPEEX_WITH_HEADER_BYTE
        if encoder is None:
            audio_encode = cloud_speech_pb2.RecognitionConfig.LINEAR16

        config = cloud_speech_pb2.RecognitionConfig(speech_contexts=[sc], encoding=audio_encode)
        streaming_config = cloud_speech_pb2.StreamingRecognitionConfig(config=config, single_utterance=True, interim_results=True)
        request = cloud_speech_pb2.StreamingRecognizeRequest(streaming_config=streaming_config)
        yield request
        self.stop = False
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if self.stop:
                break
            data = self.stream.read(CHUNK)
            if encoder:
                data = encoder.encode(data)
            request = cloud_speech_pb2.StreamingRecognizeRequest(audio_content=data)
            yield request

    def _start_intent_recognize(self, app_id):
        metadata = [(b'api-key', self.api_key)]
        try:
            responses = self.stub.StreamingIntentRecognize(self.generate_messages(app_id=app_id), metadata=metadata)
            for response in responses:
                try:
                    if response.is_final:
                        result = response.intent_result.alternatives[0]
                        self.stop = True
                        if self.intent_callback:
                            self.intent_callback({'intent': result.intent, 'entities': result.entities, 'confidence': result.confidence})
                    else:
                        if self.asr_callback:
                            self.asr_callback(response.asr_response.results[0].alternatives[0].transcript)
                except Exception as e:
                    print(e)
                    pass

        except grpc._channel._Rendezvous as e:
            print(e)

    def intent_recognize(self, app_id):
        self._start_intent_recognize(app_id)

if __name__ == "__main__":
    a = VaisService("demo")
    for is_final, result in a.intent_recognize("e2039cd1-4a88-4283-9910-7b808d8fca53"):
        print(is_final, result)
    for is_final, result in a.intent_recognize("e2039cd1-4a88-4283-9910-7b808d8fca53"):
        print(is_final, result)
