import unittest
from chat import Chat
from cache import Cache
from llm_client import LLMClient
from chat_history import ChatHistory


class TestChat(unittest.TestCase):
    def setUp(self):
        # Инициализируем компоненты перед каждым тестом
        self.llm_client = LLMClient(model_params={'temperature': 0.7})
        self.cache = Cache(max_size=3)
        self.chat_history = ChatHistory()
        self.chat = Chat(self.llm_client, self.cache, self.chat_history)
        self.user_id = 'user123'
        self.chat_id = 'chat456'

    def test_cache_retrieval(self):
        # Тестируем, что повторный запрос возвращает ответ из кэша

        # Отправляем первое сообщение
        msg1 = "Как сегодня погода?"
        response1 = self.chat.send(msg1, self.chat_id, self.user_id)
        self.assertIn("Симулированный ответ на 'Как сегодня погода?'", response1)
        self.assertNotIn("[Из кэша]", response1)

        # Отправляем похожее сообщение
        msg2 = "Какая погода сегодня!"
        response2 = self.chat.send(msg2, self.chat_id, self.user_id)
        self.assertIn("Симулированный ответ на 'Какая погода сегодня!'", response2)
        self.assertNotIn("[Из кэша]", response2)

        # Отправляем повторно первое сообщение
        response3 = self.chat.send(msg1, self.chat_id, self.user_id)
        self.assertIn("[Из кэша]", response3)
        self.assertIn("Симулированный ответ на 'Как сегодня погода?'", response3)

    def test_cache_limit(self):
        # Тестируем ограничение размера кэша

        # Отправляем три уникальных сообщения
        messages = ["Сообщение один", "Сообщение два", "Сообщение три"]
        for msg in messages:
            self.chat.send(msg, self.chat_id, self.user_id)

        # Кэш должен быть заполнен
        self.assertEqual(len(self.cache.cache), 3)

        # Добавляем новое сообщение, должно произойти удаление самого старого
        self.chat.send("Сообщение четыре", self.chat_id, self.user_id)
        self.assertEqual(len(self.cache.cache), 3)
        # Проверяем, что первого сообщения нет в кэше
        normalized_first_msg = self.cache.normalize_query("Сообщение один")
        self.assertNotIn(normalized_first_msg, self.cache.cache)

    def test_normalization(self):
        # Тестируем нормализацию запросов

        msg1 = "Привет!"
        msg2 = "привет"
        msg3 = "ПРИВЕТ!!!"

        response1 = self.chat.send(msg1, self.chat_id, self.user_id)
        response2 = self.chat.send(msg2, self.chat_id, self.user_id)
        response3 = self.chat.send(msg3, self.chat_id, self.user_id)

        # Второе и третье сообщения должны вернуть ответ из кэша
        self.assertIn("[Из кэша]", response2)
        self.assertIn("[Из кэша]", response3)

    def test_history(self):
        # Тестируем, что история чата корректно сохраняется

        messages = ["Привет", "Как дела?", "Что нового?"]
        for msg in messages:
            self.chat.send(msg, self.chat_id, self.user_id)

        history = self.chat.get_history(self.chat_id, self.user_id)
        expected_history_length = len(messages) * 2  # Каждое сообщение + ответ
        self.assertEqual(len(history), expected_history_length)

    def test_model_params(self):
        # Тестируем, что параметры модели могут влиять на ответы

        # Отправляем сообщение с исходными параметрами
        msg = "Расскажи анекдот"
        response1 = self.chat.send(msg, self.chat_id, self.user_id)

        # Отправляем то же сообщение с другими параметрами модели
        response2 = self.chat.send(msg, self.chat_id, self.user_id, temperature=0.9)

        # Проверяем, что ответы разные, поскольку параметры модели различаются
        self.assertNotEqual(response1, response2)

    def test_seed_parameter(self):
        # Тестируем, что при одинаковых входных данных ответы одинаковы

        # Очищаем кэш перед тестом
        self.cache.cache.clear()
        self.cache.order.clear()

        msg = "Как сегодня погода?"
        seed_value = 42

        # Отправляем сообщение первый раз
        response1 = self.chat.send(msg, self.chat_id, self.user_id, seed=seed_value)

        # Отправляем сообщение второй раз
        response2 = self.chat.send(msg, self.chat_id, self.user_id, seed=seed_value)

        # Извлекаем основной текст ответа без префикса "[Из кэша]"
        def strip_cache_prefix(response):
            if response.startswith("[Из кэша] "):
                return response[len("[Из кэша] "):]
            return response

        stripped_response1 = strip_cache_prefix(response1)
        stripped_response2 = strip_cache_prefix(response2)

        # Проверяем, что основные тексты ответов равны
        self.assertEqual(stripped_response1, stripped_response2)


if __name__ == '__main__':
    unittest.main()