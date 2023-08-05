import os
from setuptools import setup

if __name__ == "__main__":
    setup(
        name="vaiskit",
        author='VAIS',
        packages=['vaiskit'],
        package_data={'': ['./vaiskit/nlp', './vaiskit/speech']},
        author_email='support@vais.vn',
        url='https://vais.vn',
        include_package_data=True,
        install_requires=["grpcio==1.4.0", "pyaudio==0.2.11"],
        version="0.1.0.dev6",
        python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    )
