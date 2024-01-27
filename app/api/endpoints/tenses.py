# app/api/endpoints/tenses.py
from fastapi import APIRouter, HTTPException
from app.services.openai_service import get_tense_questions
from app.models.message_item import MessageItem
from app.utils.file_utils import read_markdown_file

router = APIRouter()


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