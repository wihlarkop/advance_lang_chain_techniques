import time
import random
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType


# 🔹 1. Tool untuk Mencari Informasi
@tool
def search_information(query: str) -> str:
    """Melakukan pencarian informasi terkait query yang diberikan."""
    if random.random() < 0.2:  # Simulasi kegagalan 20%
        raise ValueError("Search API Error: Gagal mendapatkan hasil pencarian.")
    return f"Hasil pencarian tentang '{query}': LangChain adalah framework AI untuk LLM."


# 🔹 2. Tool untuk Meringkas Hasil Pencarian
@tool
def summarize_text(text: str) -> str:
    """Meringkas teks panjang menjadi ringkasan singkat."""
    if "LangChain" not in text:
        raise ValueError("Summarization Error: Tidak ada informasi yang bisa diringkas.")
    return "Ringkasan: LangChain adalah framework AI untuk LLM."


# 🔹 3. Tool untuk Menerjemahkan Ringkasan
@tool
def translate_text(text: str, language: str) -> str:
    """Menerjemahkan teks ke bahasa yang dipilih."""
    translations = {
        "id": "Ringkasan: LangChain adalah kerangka kerja AI untuk model bahasa besar.",
        "es": "Resumen: LangChain es un framework de IA para modelos de lenguaje."
    }
    return translations.get(language, text)


# 🔹 4. Retry Wrapper untuk Error Handling
def retry_tool(tool_func, *args, retries=3, delay=2):
    for attempt in range(retries):
        try:
            return tool_func(*args)
        except Exception as e:
            print(f"⚠️ Error: {e}. Retrying ({attempt + 1}/{retries})...")
            time.sleep(delay)
    print("❌ Gagal setelah beberapa kali percobaan.")
    return "Error: Tool gagal setelah beberapa kali percobaan."


# 🔹 5. Inisialisasi Model OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# 🔹 6. Inisialisasi Agent dengan Multiple Tools
agent = initialize_agent(
    tools=[search_information, summarize_text, translate_text],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 🔹 7. Menjalankan Full Toolchain dengan Error Handling dan Retries
query = "LangChain"
search_result = retry_tool(search_information, query)
summary = retry_tool(summarize_text, search_result)
translation = retry_tool(translate_text, summary, "id")

print("\n✅ **Final Output:**", translation)
