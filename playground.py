import JsonDB

db = JsonDB.JsonDB('uploads/teste.json')

db.create_entry({'role': 'system', 'content': 'Olá'})
db.create_entry({'role': 'assistant', 'content': 'Boa noite'})
db.create_entry({'role': 'system', 'content': 'Tchau'})