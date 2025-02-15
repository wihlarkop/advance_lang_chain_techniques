from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool

# 🔹 Memory untuk menyimpan percakapan sebelumnya
memory = ConversationBufferMemory(memory_key="chat_history")


# 🔹 Tool untuk pemesanan tiket pesawat
@tool
def book_flight(destination: str, date: str) -> str:
    """Melakukan pemesanan tiket pesawat berdasarkan tujuan dan tanggal."""
    if not destination or not date:
        return "ERROR: Informasi tujuan dan tanggal diperlukan."
    return f"✅ Tiket pesawat ke {destination} untuk tanggal {date} telah dipesan!"


# 🔹 Tool untuk pemesanan hotel
@tool
def book_hotel(city: str, nights: int) -> str:
    """Melakukan pemesanan hotel berdasarkan kota dan jumlah malam."""
    if not city or nights <= 0:
        return "ERROR: Informasi kota dan jumlah malam diperlukan."
    return f"✅ Hotel di {city} untuk {nights} malam telah dipesan!"


# 🔹 Tool untuk menangani fallback jika terjadi kesalahan
@tool
def fallback_handler(error_message: str) -> str:
    """Menangani error jika terjadi kesalahan dalam proses pemesanan."""
    return f"⚠️ Terjadi kesalahan: {error_message}. Silakan coba lagi dengan informasi yang benar."


# 🔹 Inisialisasi model dan agent
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

tools = [book_flight, book_hotel, fallback_handler]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# 🔹 Menjalankan agen dengan input pengguna
user_input = "Saya ingin memesan tiket ke Bali untuk tanggal 20 Maret"
response = agent.run(user_input)
print(response)

# 🔹 Contoh input dengan error
error_input = "Saya ingin memesan hotel tapi saya lupa di mana dan berapa malam"
response = agent.run(error_input)
print(response)
