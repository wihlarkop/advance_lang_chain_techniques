import os

from dotenv import load_dotenv
from langchain.tools import tool
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent


# 🔹 Fungsi Custom dengan @tool
@tool
def hitung_luas_persegi(sisi: str) -> str:
    """Menghitung luas persegi berdasarkan panjang sisi."""
    try:
        sisi = float(sisi)  # Konversi string ke float
        if sisi <= 0:
            return "ERROR: Panjang sisi harus lebih besar dari 0."
        return f"✅ Luas persegi dengan sisi {sisi} adalah {sisi * sisi}."
    except ValueError:
        return "ERROR: Masukkan angka yang valid untuk sisi."


# 🔹 Inisialisasi Model
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# 🔹 Inisialisasi Agent
agent = initialize_agent(
    tools=[hitung_luas_persegi],  # Langsung gunakan fungsi yang didekorasi @tool
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

if __name__ == "__main__":
    # 🔹 Menjalankan Agent
    response = agent.run("Hitung luas persegi dengan sisi 5.")
    print(response)
