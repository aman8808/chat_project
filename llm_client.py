class LLMClient:
    def __init__(self, model_params):
        self.model_params = model_params

    def __call__(self, msg, **model_kwargs):
        # Симуляция генерации ответа
        response = f"Симулированный ответ на '{msg}' с параметрами {self.model_params}"
        return response