import queue
import sys
import json
import time
import logging
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# also for the record i have no idea what the explation is because i put that task to a ai 

# Configure logging
logging.basicConfig(level=logging.INFO)
killme = logging.getLogger(__name__)

def process_transcription(text):
    """Function to handle the transcribed text."""
    sys.stdout.write(f"\nTranscription: {text}\n")
    sys.stdout.flush()

def audio_generator():
    """Generator function to yield audio chunks."""
    samplerate = 16000  # Default sample rate
    channels = 1  # Mono
    blocksize = 1024  # Smaller blocksize for reduced latency

    with sd.InputStream(samplerate=samplerate, blocksize=blocksize, dtype='int16', channels=channels):
        while True:
            data = (yield)
            yield data

def main():
    # Load models
    models = {
        "english": Model(r"g:/cods/speech to text/Vosk models/vosk-english"),
        "arabic": Model(r"g:/cods/speech to text/Vosk models/vosk-Arabic"),
        "hindi": Model(r"g:/cods/speech to text/Vosk models/vosk-hindi"),
        "malayalam": Model(r"g:/cods/speech to text/Vosk models/vosk-malayalam/vosk-malayalam-master/MODELS/vosk-model-malayalam-bigram")
    }

    recognizer = {
        lang: KaldiRecognizer(model, 16000)
        for lang, model in models.items()
    }

    audio_gen = audio_generator()
    next(audio_gen)  # Start the generator

    killme.info("Listening for speech... Press Ctrl+C to stop.")

    while True:
        try:
            data = audio_gen.send(sd.rec(int(16000 * 0.5)))
            for lang, rec in recognizer.items():
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    transcript = result.get("text", "")
                    if transcript:
                        process_transcription(f"({lang}) {transcript}")
                        break  # Stop capturing audio after sending transcription
            else:
                sys.stdout.write("\rListening...")  # Minimal logging for reduced CPU usage
                sys.stdout.flush()

        except KeyboardInterrupt:
            killme.info("\nRecording stopped by user.")
            break
        except Exception as e:
            killme.exception("Error occurred")
            break

if __name__ == "__main__":
    main()
