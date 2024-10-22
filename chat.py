from chat_history import ChatHistory
from cache import Cache
from llm_client import LLMClient


class Chat:
    def __init__(self, llm_client, cache, chat_history):
        self.client = llm_client
        self.cache = cache
        self.chat_history = chat_history

    def send(self, msg, chat_id, user_id, seed=None, **model_kwargs):
        # Добавляем сообщение в историю чата
        self.chat_history.add_message(user_id, chat_id, f"Пользователь: {msg}")
        # Пытаемся получить закэшированный ответ
        answer = self.cache.get(msg)
        if answer is None:
            # Генерируем новый ответ
            answer = self.client(msg, **model_kwargs)
            # Добавляем ответ в кэш
            self.cache.add(msg, answer)
        else:
            answer = f"[Из кэша] {answer}"
        # Добавляем ответ в историю чата
        self.chat_history.add_message(user_id, chat_id, f"Бот: {answer}")
        return answer

    def get_history(self, chat_id, user_id):
        return self.chat_history.get_history(user_id, chat_id)