from nltk.sentiment.vader import SentimentIntensityAnalyzer


class VaderSentimentAnalyzer:
    """

    """
    sia = SentimentIntensityAnalyzer()

    def __init__(self, text_body):
        self.text_body = text_body

    @staticmethod
    def analyze_sentence(sentence: str, sentiment_analyzer=sia) -> dict:
        return sentiment_analyzer.polarity_scores(sentence)

    def analyze_whole_text(self, sentiment_analyzer=sia) -> dict:
        return sentiment_analyzer.polarity_scores(self.text_body)
