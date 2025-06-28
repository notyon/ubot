import os

try:
    from pymongo import MongoClient
    from dotenv import load_dotenv
    load_dotenv()

    MONGO_URI = os.getenv("MONGO_URI")
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["ubot_database"]
    users = db["users"]
    sudoers = db["sudo"]
    sessions = db["sessions"]

    MONGO_AVAILABLE = True

except:
    # Fallback jika tidak pakai MongoDB
    users_data = {}
    sudo_data = set()
    sessions_data = {}
    MONGO_AVAILABLE = False


# === USER ===

def add_user(user_id):
    if MONGO_AVAILABLE:
        users.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    else:
        users_data[user_id] = True

def is_user_allowed(user_id):
    if MONGO_AVAILABLE:
        return users.find_one({"user_id": user_id}) is not None
    return users_data.get(user_id, False)


# === SUDO ===

def add_sudo(user_id):
    if MONGO_AVAILABLE:
        sudoers.update_one({"user_id": user_id}, {"$set": {"user_id": user_id}}, upsert=True)
    else:
        sudo_data.add(user_id)

def remove_sudo(user_id):
    if MONGO_AVAILABLE:
        sudoers.delete_one({"user_id": user_id})
    else:
        sudo_data.discard(user_id)

def get_sudo_list():
    if MONGO_AVAILABLE:
        return [user["user_id"] for user in sudoers.find()]
    return list(sudo_data)

def is_sudo(user_id):
    if MONGO_AVAILABLE:
        return sudoers.find_one({"user_id": user_id}) is not None
    return user_id in sudo_data


# === SESSION ===

def save_session(user_id, session_string):
    if MONGO_AVAILABLE:
        sessions.update_one({"user_id": user_id}, {"$set": {"session": session_string}}, upsert=True)
    else:
        sessions_data[user_id] = session_string

def get_session(user_id):
    if MONGO_AVAILABLE:
        data = sessions.find_one({"user_id": user_id})
        return data["session"] if data else None
    return sessions_data.get(user_id)

def delete_session(user_id):
    if MONGO_AVAILABLE:
        sessions.delete_one({"user_id": user_id})
    else:
        sessions_data.pop(user_id, None)

def get_all_sessions():
    if MONGO_AVAILABLE:
        return [x["session"] for x in sessions.find()]
    return list(sessions_data.values())
