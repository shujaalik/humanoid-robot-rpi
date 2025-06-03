
import io
import pygame
from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", name="en-US-Chirp-HD-F"
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

class Speaker:
    def __init__(self, lang='en'):
        self.lang = lang
        pygame.mixer.init()

    def speak(self, text):
        """Speaks the given text using gTTS and pygame."""
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        # write to the audio_fp
        self.audio_fp = io.BytesIO(response.audio_content)
        self.audio_fp.seek(0)
        
        # Load the sound from the BytesIO object
        pygame.mixer.music.load(self.audio_fp)
        
        # Play the sound
        pygame.mixer.music.play()
        
        # Keep the script running until the speech is finished
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(1)
    
    def stop(self):
        pygame.mixer.quit()