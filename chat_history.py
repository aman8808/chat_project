from collections import defaultdict


class ChatHistory:
    def __init__(self):
        # Вложенный словарь: history[user_id][chat_id] = список сообщений
        self.history = defaultdict(lambda: defaultdict(list))

    def add_message(self, user_id, chat_id, msg):
        self.history[user_id][chat_id].append(msg)

    def get_history(self, user_id, chat_id):
        # Возвращаем историю чата как есть
        return self.history[user_id][chat_id]