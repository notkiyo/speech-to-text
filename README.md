# Real-time Speech-to-Text Application

This Python application converts spoken language into text in real-time using the Vosk library. It supports multiple languages including Arabic, Hindi, English, and Malayalam.

## Installation

1. Install required Python packages using pip:

```bash
pip install vosk sounddevice
```
**For more, you can chack the code**

2. Download the language models for Arabic, Hindi, English, and Malayalam from the Vosk website (https://alphacephei.com/vosk/models).

## Dependencies

- [Vosk](https://alphacephei.com/vosk/): Vosk is an open-source speech recognition toolkit that offers pre-trained models for various languages.
- [sounddevice](https://python-sounddevice.readthedocs.io/en/0.4.1/): Python bindings for PortAudio, the cross-platform audio I/O library. It provides real-time audio input/output.
- **for the Malayalam one you have to ues [Malayalam model](https://gitlab.com/kavyamanohar/vosk-malayalam) or this one where you don't have to do the set-up part of the model. [malayalam pre-set](https://mega.nz/folder/UvEETZBL#TkKnFbvgo6sPJRfDkASi3w)**
## Usage

1. Replace the language model paths in the script with the paths to the downloaded models.

2. Customize the `process_transcription` function to handle the transcribed text according to your application's requirements.



3. Start speaking into the microphone; the transcribed text will be displayed in the console in real-time.

## Features

- **Lightweight**: The application is lightweight and designed for real-time speech recognition.
- **Multi-language Support**: Supports Arabic, Hindi, English, and Malayalam out of the box.
- **Real-time Transcription**: Provides instant transcription of spoken language.
- **transcription** : if you mess with it you can create a transcription

## Customization

- Replace the language model paths in the script with the paths to your downloaded models.
- Customize the `process_transcription` function to handle the transcribed text according to your application's requirements.

## Vosk

[Vosk](https://alphacephei.com/vosk/) is a free and open-source speech recognition toolkit developed by Alpha Cephei. It offers accurate and efficient speech recognition for various languages and is widely used in research and production environments.

## Known Issues

- if you try to make it run a auto detect Multi language it kinda laggy and slow if you dont have a high power pc

## Acknowledgments

- The development of this application is supported by the Vosk community and contributors.
- Special thanks to the developers of the Vosk library for providing an excellent speech recognition toolkit.

## License

This project is licensed under the [MIT License](LICENSE).
```

This version includes additional sections providing information on dependencies, Vosk, and acknowledgments to give users a better understanding of the tools and libraries used in your application. Feel free to customize it further to meet your specific needs!
