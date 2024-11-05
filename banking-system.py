
import json

class BankSystem:
    def load_data(self):
        users = {}
        try:
            with open("bank_data.jsonl", "r") as file:
                for line in file:
                    user_data = json.loads(line.strip())
                    users[user_data["phone"]] = user_data
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return users


    def save_data(self):

        with open("bank_data.jsonl", "w") as file:
            for user_data in self.users.values():
                json.dump(user_data, file)
                file.write("\n")