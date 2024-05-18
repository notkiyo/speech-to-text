import queue
import sys
import json
import time
import logging
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Configure logging
logging.basicConfig(level=logging.WARNING)  # Set to WARNING to reduce log output
itshim = logging.getLogger(__name__)

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
            itshim.error(status)
        audio_queue.put(bytes(indata))

    # Load Malayalam model
    malayalam_model_path = r"G:\cods\speech to text\Vosk models\vosk-malayalam\vosk-malayalam-master\MODELS\vosk-model-malayalam-bigram"  # Path to Malayalam model
    malayalam_model = Model(malayalam_model_path)
    recognizer = KaldiRecognizer(malayalam_model, samplerate)

    # Adjust these parameters according to your needs
    min_speech_length = 1  # Minimum length of speech segment in seconds
    max_silence_length = 0.5  # Maximum length of silence allowed in seconds

    # Variables for buffering audio data
    speech_buffer = b''
    last_speech_time = time.time()

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16', channels=channels, callback=callback):
        itshim.info("Listening for speech... Press Ctrl+C to stop.")
        
        while True:
            try:
                data = audio_queue.get()
                speech_buffer += data
                
                # Check for speech segments based on silence threshold
                if abs(time.time() - last_speech_time) >= min_speech_length and len(data) == 0:
                    if abs(time.time() - last_speech_time) >= max_silence_length:
                        # Process the buffered speech segment
                        if recognizer.AcceptWaveform(speech_buffer):
                            result = json.loads(recognizer.Result())
                            transcript = result.get("text", "")
                            
                            if transcript:
                                process_transcription(transcript)
                        
                        # Reset speech buffer and update last speech time
                        speech_buffer = b''
                        last_speech_time = time.time()

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
                itshim.info("\nRecording stopped by user.")
                break
            except Exception as e:
                itshim.exception("Error occurred")
                break

if __name__ == "__main__":
    main()
