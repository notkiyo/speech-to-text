import queue
import sys
import json
import time
import logging
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_transcription(text):
    """Function to handle the transcribed text."""
    sys.stdout.write(f"\nTranscription: {text}\n")
    sys.stdout.flush()

def main():
    samplerate = 16000  # Default sample rate
    channels = 1  # Mono
    
    audio_queue = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            logger.error(status)
        audio_queue.put(bytes(indata))

    # Load English model
    english_model_path = r"G:\cods\speech to text\Vosk models\vosk-english"  # Path to English model
    english_model = Model(english_model_path)
    recognizer = KaldiRecognizer(english_model, samplerate)

    with sd.RawInputStream(samplerate=samplerate, blocksize=4096, dtype='int16', channels=channels, callback=callback):
        logger.info("Listening for speech... Press Ctrl+C to stop.")
        
        while True:
            try:
                data = audio_queue.get()
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    transcript = result.get("text", "")
                    
                    if transcript:
                        process_transcription(transcript)
                        break  # Stop capturing audio after sending transcription
                else:
                    sys.stdout.write("\rListening" + "." * (int(time.time()) % 3 + 1))  # Dynamic listening dots
                    sys.stdout.flush()
            
            except KeyboardInterrupt:
                logger.info("\nRecording stopped by user.")
                break
            except Exception as e:
                logger.exception("Error occurred")
                break

if __name__ == "__main__":
    main()
