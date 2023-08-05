import grpc
import vaiskit.speech.v1.cloud_speech_pb2_grpc as cloud_speech_pb2_grpc
import vaiskit.speech.v1.cloud_speech_pb2 as cloud_speech_pb2
import vaiskit.nlp.v1.cloud_nlp_pb2_grpc as cloud_nlp_pb2_grpc
import time

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

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 15
p = pyaudio.PyAudio()


class VaisService():
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "service.grpc.vais.vn:50051"
        self.channel = grpc.insecure_channel(self.url)
        self.channel.subscribe(callback=self.connectivity_callback, try_to_connect=True)
        self.stop = False
        self.stub = cloud_speech_pb2_grpc.SpeechStub(self.channel)
        self.stub_nlu = cloud_nlp_pb2_grpc.NLPStub(self.channel)

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
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        self.stop = False
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            if self.stop:
                break
            data = stream.read(CHUNK)
            if encoder:
                data = encoder.encode(data)
            request = cloud_speech_pb2.StreamingRecognizeRequest(audio_content=data)
            yield request

        stream.stop_stream()
        stream.close()
        p.terminate()

    def intent_recognize(self, app_id):
        start = time.time()
        timeout = 20
        metadata = [(b'api-key', self.api_key)]
        try:
            responses = self.stub.StreamingIntentRecognize(self.generate_messages(app_id=app_id), metadata=metadata)
            for response in responses:
                try:
                    if response.is_final:
                        result = response.intent_result.alternatives[0]
                        self.stop = True
                        yield True, {'intent': result.intent, 'entities': result.entities, 'confidence': result.confidence}
                    else:
                        yield False, response.asr_response.results[0].alternatives[0].transcript
                except Exception as e:
                    print(e)
                    pass

        except grpc._channel._Rendezvous as e:
            print(e)
            end = time.time()
            if end - start < timeout:
                return None, "bad_connection"
            else:
                return None, "timeout"

if __name__ == "__main__":
    a = VaisService("demo")
    for is_final, result in a.intent_recognize("e2039cd1-4a88-4283-9910-7b808d8fca53"):
        print(is_final, result)
