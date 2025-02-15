from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langchain.agents import initialize_agent, AgentType


# 🔹 1. Tool untuk Mencari Informasi
@tool
def search_information(query: str) -> str:
    """Mencari informasi berdasarkan kata kunci yang diberikan."""
    search_results = {
        "AI": "Artificial Intelligence (AI) adalah teknologi yang memungkinkan komputer untuk berpikir dan belajar seperti manusia.",
        "Python": "Python adalah bahasa pemrograman populer yang digunakan untuk pengembangan web, data science, dan kecerdasan buatan.",
        "Blockchain": "Blockchain adalah teknologi yang digunakan untuk mencatat transaksi secara terdesentralisasi."
    }
    return search_results.get(query, "Informasi tidak ditemukan.")


# 🔹 2. Tool untuk Menganalisis dan Merangkum Informasi
@tool
def summarize_information(info: str) -> str:
    """Meringkas informasi utama dari hasil pencarian."""
    if "AI" in info:
        return "AI memungkinkan komputer untuk berpikir dan belajar layaknya manusia."
    elif "Python" in info:
        return "Python adalah bahasa pemrograman serbaguna yang digunakan dalam berbagai bidang."
    elif "Blockchain" in info:
        return "Blockchain adalah sistem pencatatan transaksi yang terdesentralisasi dan aman."
    else:
        return "Informasi tidak tersedia untuk diringkas."


# 🔹 3. Tool untuk Membuat Laporan
@tool
def generate_report(topic: str, summary: str) -> str:
    """Membuat laporan singkat berdasarkan hasil ringkasan."""
    report = f"📌 Laporan tentang {topic}\n"
    report += f"📖 Ringkasan: {summary}\n"
    report += "🔍 Sumber: Data diperoleh dari pencarian AI.\n"
    return report


# 🔹 4. Inisialisasi Model OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0)


# 🔹 5. Chain: Pencarian → Ringkasan → Laporan
def run_agent(topic: str):
    agent = initialize_agent(
        tools=[search_information, summarize_information, generate_report],
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    # 1️⃣ Cari informasi berdasarkan topik
    info = agent.run(f"Cari informasi tentang {topic}")

    # 2️⃣ Ringkas informasi yang ditemukan
    summary = agent.run(f"Ringkas informasi berikut: {info}")

    # 3️⃣ Buat laporan akhir
    report = agent.run(f"Buat laporan berdasarkan topik {topic} dan ringkasan {summary}")

    print("\n✅ **Laporan Akhir:**\n", report)


# 🔹 6. Contoh Penggunaan
run_agent("Python")
