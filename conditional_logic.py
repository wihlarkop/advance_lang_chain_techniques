import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
import re


# untuk Mendapatkan Cuaca
@tool
def get_weather(location: str) -> str:
    """Mengambil data cuaca berdasarkan lokasi."""
    weather_data = {
        "Jakarta": "Cerah, 32°C",
        "Tokyo": "Hujan, 18°C",
        "New York": "Bersalju, -2°C"
    }
    return weather_data.get(location, "Lokasi tidak ditemukan.")


# Tool untuk Menghitung Ekspresi Matematika
@tool
def calculate(expression: str) -> str:
    """Menghitung ekspresi matematika yang diberikan."""
    try:
        # Membatasi operasi yang diperbolehkan untuk keamanan
        allowed_chars = set("0123456789+-*/().")
        if not all(c in allowed_chars for c in expression):
            return "Ekspresi tidak valid. Hanya boleh menggunakan angka dan operator +, -, *, /, (, )."

        result = eval(expression)
        return f"Hasil perhitungan: {result}"
    except Exception as e:
        return f"Terjadi kesalahan dalam perhitungan: {str(e)}"


# Tool fallback untuk menangani kasus lainnya
@tool
def general_info(query: str) -> str:
    """Memberikan informasi umum atau jawaban untuk pertanyaan yang tidak memerlukan tool khusus."""
    return "Ini adalah respon default. LLM akan menjawab pertanyaan ini secara langsung."


# Dynamic Routing: Memilih Tool Berdasarkan Input
def select_tool(user_input: str):
    if "cuaca" in user_input.lower() or "suhu" in user_input.lower():
        return [get_weather]
    elif re.search(r'\d+[\+\-\*/]\d+', user_input):  # Mendeteksi ekspresi matematika
        return [calculate]
    else:
        # Selalu sertakan general_info sebagai fallback
        return [general_info]


# Eksekusi Agent dengan Routing Dinamis
def run_agent(user_input: str):
    load_dotenv()
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Inisialisasi Model OpenAI
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
    selected_tools = select_tool(user_input)

    agent = initialize_agent(
        tools=selected_tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    try:
        response = agent.run(user_input)
        print("\n✅ **Final Output:**", response)
    except Exception as e:
        print(f"\n❌ **Error:** {str(e)}")


if __name__ == "__main__":
    print("=== Example 1: Weather Query ===")
    run_agent("Bagaimana cuaca di Jakarta hari ini?")

    print("\n=== Example 2: Math Calculation ===")
    run_agent("Hitung 25 * 4 + 10")

    print("\n=== Example 3: General Question ===")
    run_agent("Ceritakan tentang apa itu large language model?")
