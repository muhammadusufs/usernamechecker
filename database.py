import json

DB_FILE = "data.json"


def read_data():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def write_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def insert_username(username, is_free):
    data = read_data()
    data.append({"username": username, "is_free": is_free})
    write_data(data)


def update_username_status(username, is_free):
    data = read_data()
    for entry in data:
        if entry["username"] == username:
            entry["is_free"] = is_free
            break
    write_data(data)


def delete_username(username):
    data = read_data()
    data = [entry for entry in data if entry["username"] != username]
    write_data(data)


def get_all_usernames():
    data = read_data()
    print([entry["username"] for entry in data])
    return [{'username': entry["username"], 'is_free':entry['is_free']} for entry in data]


def get_free_usernames():
    data = read_data()
    return [entry["username"] for entry in data if entry["is_free"] == 0]
