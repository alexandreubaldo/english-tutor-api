import json, os, uuid

class JsonDB:
    def __init__(self, filename):
        self.filename = filename
        self.data = self.load_from_file()

    def load_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_to_file(self):
        with open(self.filename, 'w') as file:
            json.dump(self.data, file, indent=4)

    def create_entry(self, entry_data):
        id = str(uuid.uuid4())  # Generate a unique UUID
        entry_data['id'] = id
        self.data.append(entry_data)
        self.save_to_file()
        return entry_data  # Return the generated UUID

    def read_entry(self, id):
        for entry in self.data:
            if entry['id'] == id:
                return entry
        return None

    def update_entry(self, id, updated_data):
        for entry in self.data:
            if entry['id'] == id:
                entry.update(updated_data)
                self.save_to_file()
                return
        print(f"Entry with id {id} does not exist.")

    def delete_entry(self, id):
        for i, entry in enumerate(self.data):
            if entry['id'] == id:
                del self.data[i]
                self.save_to_file()
                return
        print(f"Entry with id {id} does not exist.")

    def get_all_entries(self):
        return self.data

    def find_entry_by_property(self, property_name, property_value):
        for entry in self.data:
            if entry.get(property_name) == property_value:
                return entry
        return None
