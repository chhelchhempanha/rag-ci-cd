from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import requests
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

load_dotenv()


class AIService:
    def __init__(self):
        self.model = init_chat_model("llama-3.1-8b-instant", model_provider="groq")
        self.bitcoin_data = None

    def fetch_bitcoin_data(self):
        """Fetch and analyze Bitcoin market data"""
        print("Fetching Bitcoin data...")
        data = requests.get(
            "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30"
        ).json()
        prices = data['prices']

        # Prepare data for training
        X = np.array([[i] for i in range(len(prices))])
        y = np.array([price[1] for price in prices])

        # Train model
        model_ml = LinearRegression()
        model_ml.fit(X, y)

        # Predict next 7 days
        future_days = 7
        future_X = np.array([[len(prices) + i] for i in range(future_days)])
        predictions = model_ml.predict(future_X)

        # Current price and prediction summary
        current_price = y[-1]
        predicted_price = predictions[-1]
        price_change = ((predicted_price - current_price) / current_price) * 100

        self.bitcoin_data = {
            "current_price": current_price,
            "predicted_price": predicted_price,
            "price_change": price_change,
            "current_date": datetime.now().strftime("%B %d, %Y"),
            "prediction_date": (datetime.now() + timedelta(days=7)).strftime("%B %d, %Y"),
            "trend": "Bullish" if price_change > 0 else "Bearish"
        }

        return self.bitcoin_data

