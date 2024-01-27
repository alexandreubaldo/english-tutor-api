from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import JsonDB
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import json, re, os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


API_KEY = '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'
API_MODEL = 'gpt-4'

db = JsonDB.JsonDB('uploads/conversation.json')


class MessageItem(BaseModel):
    role: str
    content: str

client = OpenAI(api_key=API_KEY)

def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


@app.get("/tenses")
async def tenses():
    file_path = 'db/tenses.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

@app.get("/tenses/{tense_id}")
async def get_tense_by_id(tense_id: int):
    file_path = 'db/tenses.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    tense = None
    
    for item in data:
        if item.get("id") == tense_id:
            tense = item
            break
    
    if tense is not None:
        # Prepare the messages for the API call
        user_message = read_markdown_file('./db/prompts/questions_and_tense.md')
        system_message = "ok"

        messages = [
            {"role": "user", "content": user_message},
            {"role": "system", "content": system_message},
            {"role": "user", "content": tense["name"]}
        ]

        print(messages)

        response = client.chat.completions.create(model=API_MODEL, messages=messages)
        # Assuming the API response contains the questions in the desired format
        questions = response.choices[0].message.content  # Parse the response accordingly

        print(questions)
        # Add the questions to the tense
        tense['questions'] = json.loads(questions)

        return tense

    # If no matching ID is found, raise an HTTP 404 error
    raise HTTPException(status_code=404, detail="Tense not found")


###################### End of Tenses API ######################

@app.get("/")
async def root():
    return {"message": "Just another API"}

@app.post("/message")
async def send_message(message :MessageItem):
    return db.create_entry(message.model_dump())


@app.post("/messages")
async def send_messages(messages: List[MessageItem]):
    # return messages
    response = client.chat.completions.create(model=API_MODEL, messages=messages)
    message = response.choices[0].message.content
    try:
        return extract_json(message)
    except ValueError:
        return {'errorMessage': 'The AI Assistant is not feeling well :)'}

def transcribe_text_to_voice(audio_location):
    client = OpenAI(api_key=API_KEY)
    audio_file= open(audio_location, "rb")
    transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return transcript.text

@app.post("/audio-messages")
async def audio_messages(file: UploadFile = File(...)):
    try:
        file_location = f"./uploads/{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)

        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        transcript = transcribe_text_to_voice(file_location)

        return JSONResponse(status_code=200, content={"fileLocation": file_location, 'transcript': transcript})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


def extract_json(string_data):
    strin = str(string_data)
    json_str = re.search(r'\{.*\}', strin, re.DOTALL)
    # Parsing the extracted string as JSON, if found
    if json_str:
        json_data = json.loads(json_str.group())
        return json_data
    else:
        raise ValueError('No Json Found')