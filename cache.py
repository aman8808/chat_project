import re
from collections import deque


class Cache:
    def __init__(self, max_size=100):
        self.cache = {}
        self.order = deque()
        self.max_size = max_size

    def normalize_query(self, query):
        # Приводим к нижнему регистру и удаляем знаки препинания
        query = query.lower()
        query = re.sub(r'[^\w\s]', '', query)
        return query.strip()

    def get(self, query):
        normalized_query = self.normalize_query(query)
        return self.cache.get(normalized_query)

    def add(self, query, response):
        normalized_query = self.normalize_query(query)
        if normalized_query not in self.cache:
            if len(self.cache) >= self.max_size:
                # Удаляем самый старый элемент
                oldest_query = self.order.popleft()
                del self.cache[oldest_query]
            self.cache[normalized_query] = response
            self.order.append(normalized_query)