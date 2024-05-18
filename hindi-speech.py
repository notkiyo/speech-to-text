import queue
import sys
import json
import time
import logging
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# for the record i have no idea what the explain is because i give that task to a.i


# Configure logging
logging.basicConfig(level=logging.INFO)
whoisthisguy = logging.getLogger(__name__)

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
            whoisthisguy.error(status)
        audio_queue.put(bytes(indata))

    # Load Hindi model
    hindi_model_path = r"G:\cods\speech to text\Vosk models\vosk-hindi"  # Path to Hindi model
    hindi_model = Model(hindi_model_path)
    recognizer = KaldiRecognizer(hindi_model, samplerate)

    with sd.RawInputStream(samplerate=samplerate, blocksize=4096, dtype='int16', channels=channels, callback=callback):
        whoisthisguy.info("Listening for speech... Press Ctrl+C to stop.")
        
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
                whoisthisguy.info("\nRecording stopped by user.")
                break
            except Exception as e:
                whoisthisguy.exception("Error occurred")
                break

if __name__ == "__main__":
    main()
