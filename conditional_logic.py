from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType
import re


# 🔹 1. Tool untuk Mendapatkan Cuaca
@tool
def get_weather(location: str) -> str:
    """Mengambil data cuaca berdasarkan lokasi."""
    weather_data = {
        "Jakarta": "Cerah, 32°C",
        "Tokyo": "Hujan, 18°C",
        "New York": "Bersalju, -2°C"
    }
    return weather_data.get(location, "Lokasi tidak ditemukan.")


# 🔹 2. Tool untuk Menghitung Ekspresi Matematika
@tool
def calculate(expression: str) -> str:
    """Menghitung ekspresi matematika yang diberikan."""
    try:
        result = eval(expression)
        return f"Hasil perhitungan: {result}"
    except Exception:
        return "Terjadi kesalahan dalam perhitungan."


# 🔹 3. Inisialisasi Model OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)


# 🔹 4. Dynamic Routing: Memilih Tool Berdasarkan Input
def select_tool(user_input: str):
    if "cuaca" in user_input.lower() or "suhu" in user_input.lower():
        return [get_weather]
    elif re.search(r'\d+[\+\-\*/]\d+', user_input):  # Mendeteksi ekspresi matematika
        return [calculate]
    else:
        return []  # Tidak menggunakan tool, hanya LLM


# 🔹 5. Eksekusi Agent dengan Routing Dinamis
def run_agent(user_input: str):
    selected_tools = select_tool(user_input)

    agent = initialize_agent(
        tools=selected_tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    response = agent.run(user_input)
    print("\n✅ **Final Output:**", response)


# 🔹 6. Contoh Penggunaan
run_agent("Bagaimana cuaca di Jakarta hari ini?")
run_agent("Hitung 25 * 4 + 10")
run_agent("Ceritakan tentang sejarah Jepang.")
