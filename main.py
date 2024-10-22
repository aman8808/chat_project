from chat import Chat
from cache import Cache
from llm_client import LLMClient
from chat_history import ChatHistory


def main():
    # Создаем экземпляры компонентов
    llm_client = LLMClient(model_params={'temperature': 0.7})
    cache = Cache(max_size=3)  # Ограничиваем размер кэша до 3 элементов
    chat_history = ChatHistory()
    chat = Chat(llm_client, cache, chat_history)

    # Симулируем взаимодействие пользователя
    user_id = 'user123'
    chat_id = 'chat456'

    # Пользователь отправляет сообщения
    messages = [
        "Как сегодня погода?",
        "Какая погода сегодня!",
        "Расскажи анекдот",
        "Как сегодня погода?"
    ]

    for msg in messages:
        response = chat.send(msg, chat_id, user_id)
        print(f"Пользователь: {msg}\nБот: {response}\n")

    # Вывод истории чата
    print("История чата:")
    history = chat.get_history(chat_id, user_id)
    for line in history:
        print(line)

    # Проверка содержимого кэша
    print("\nСодержимое кэша:")
    for query in cache.cache:
        print(f"Запрос: '{query}' - Ответ: '{cache.cache[query]}'")


if __name__ == "__main__":
    main()