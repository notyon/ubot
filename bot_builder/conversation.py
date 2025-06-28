# bot_builder/conversation.py

class ConversationManager:
    def __init__(self):
        self.states = {}
        self.data = {}

    def start(self, user_id, state):
        self.states[user_id] = state
        self.data[user_id] = {}

    def set_state(self, user_id, state):
        self.states[user_id] = state

    def get_state(self, user_id):
        return self.states.get(user_id)

    def set_data(self, user_id, key, value):
        if user_id not in self.data:
            self.data[user_id] = {}
        self.data[user_id][key] = value

    def get_data(self, user_id):
        return self.data.get(user_id, {})

    def end(self, user_id):
        self.states.pop(user_id, None)
        self.data.pop(user_id, None)
