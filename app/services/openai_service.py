# app/services/openai_service.py
from openai import OpenAI

API_KEY = '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'
API_MODEL = 'gpt-4'

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)

    def chat_completion(self, messages):
        return self.client.chat.completions.create(model=API_MODEL, messages=messages)

    def transcribe_text_to_voice(self, audio_location, model="whisper-1"):
        with open(audio_location, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(model=model, file=audio_file)
        return transcript.text

