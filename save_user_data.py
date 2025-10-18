import json


def save_user_data(data_file, users):
    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(users, file, ensure_ascii=False, indent=2)