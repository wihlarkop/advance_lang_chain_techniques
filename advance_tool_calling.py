from langchain.chat_models import ChatOpenAI
from langchain_core.messages import HumanMessage
import json


class CurrencyConverter:
    def __init__(self, api_key: str):
        # Definisi fungsi konversi mata uang
        self.functions = [{
            "name": "convert_currency",
            "description": "Mengkonversi IDR ke USD atau sebaliknya",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "Jumlah uang yang akan dikonversi"
                    },
                    "from_currency": {
                        "type": "string",
                        "enum": ["IDR", "USD"],
                        "description": "Mata uang asal"
                    },
                    "to_currency": {
                        "type": "string",
                        "enum": ["IDR", "USD"],
                        "description": "Mata uang tujuan"
                    }
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }]

        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo-0125",
            openai_api_key=api_key,
            temperature=0
        ).bind(functions=self.functions)

        # Rate konversi sederhana
        self.rates = {
            "IDR_TO_USD": 1 / 15500,  # 1 IDR = 1/15500 USD
            "USD_TO_IDR": 15500  # 1 USD = 15500 IDR
        }

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """Melakukan konversi mata uang"""
        if from_currency == "IDR" and to_currency == "USD":
            return amount * self.rates["IDR_TO_USD"]
        elif from_currency == "USD" and to_currency == "IDR":
            return amount * self.rates["USD_TO_IDR"]
        return amount

    def process_query(self, query: str) -> str:
        """Memproses pertanyaan pengguna"""
        messages = [HumanMessage(content=query)]

        response = self.llm.invoke(messages)

        # Jika tidak ada function call, kembalikan jawaban langsung
        if not response.additional_kwargs.get("function_call"):
            return response.content

        # Proses function call
        function_call = response.additional_kwargs["function_call"]
        arguments = json.loads(function_call["arguments"])

        # Lakukan konversi
        result = self.convert_currency(
            arguments["amount"],
            arguments["from_currency"],
            arguments["to_currency"]
        )

        # Format hasil
        return f"{arguments['amount']} {arguments['from_currency']} = {result:.2f} {arguments['to_currency']}"


# Contoh penggunaan
if __name__ == "__main__":
    OPENAI_API_KEY = "your-api-key"
    converter = CurrencyConverter(OPENAI_API_KEY)

    # Contoh queries
    queries = [
        "Berapa 100 USD dalam rupiah?",
        "Tolong konversikan 1500000 rupiah ke dollar",
        "Berapa nilai 50 dollar AS dalam IDR?"
    ]

    for query in queries:
        result = converter.process_query(query)
        print(f"\nQ: {query}")
        print(f"A: {result}")