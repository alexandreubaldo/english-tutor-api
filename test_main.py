from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Just another API" }

def test_send_messages():
    testing_data = json.dumps([
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "What's the weather like in New York today?"
    },
    {
        "role": "assistant",
        "content": "The current weather in New York is sunny with a high of 75°F and a low of 65°F."
    },
])
    response = client.post("/messages", content=testing_data)
    print(response)
    # assert response.text == testing_data
    # https://wise.com/rates/live?source=GBP&target=BRL