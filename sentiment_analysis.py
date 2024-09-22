from transformers import pipeline

class SentimentAnalyzer:
    def __init__(self):
        # Carga del pipeline de análisis de sentimientos
        self.analyzer = pipeline("sentiment-analysis")

    def analyze_sentiment(self, response):
        # Análisis de sentimiento de la respuesta
        result = self.analyzer(response)[0]
        return f"{result['label']} ({round(result['score'], 2)})"
