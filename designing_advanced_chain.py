import os

from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import SequentialChain, LLMChain
import json

# API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inisialisasi model
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)

# 1. Chain pertama: Analisis permintaan perjalanan
analyze_prompt = ChatPromptTemplate.from_template(
    """Analisis permintaan perjalanan berikut dan ekstrak informasi kunci:

    Permintaan pengguna: {user_input}

    Berikan informasi berikut dalam format JSON:
    - destination: tujuan perjalanan
    - duration: durasi perjalanan dalam hari (angka)
    - purpose: tujuan perjalanan (bisnis/liburan/lainnya)
    - num_travelers: jumlah orang (angka)

    Jika informasi tidak disebutkan, gunakan nilai default yang masuk akal.
    """
)

analysis_chain = LLMChain(
    llm=llm,
    prompt=analyze_prompt,
    output_key="travel_analysis"
)

# 2. Chain kedua: Rekomendasi hotel berdasarkan analisis
hotel_prompt = ChatPromptTemplate.from_template(
    """Berdasarkan analisis perjalanan berikut:

    {travel_analysis}

    Berikan rekomendasi hotel yang sesuai. 
    Sertakan:
    - nama hotel
    - jenis kamar
    - perkiraan harga
    - fasilitas utama
    """
)

hotel_chain = LLMChain(
    llm=llm,
    prompt=hotel_prompt,
    output_key="hotel_recommendation"
)

# 3. Chain ketiga: Rekomendasi aktivitas
activity_prompt = ChatPromptTemplate.from_template(
    """Berdasarkan analisis perjalanan:

    {travel_analysis}

    Dan rekomendasi hotel:

    {hotel_recommendation}

    Berikan 3 rekomendasi aktivitas yang dapat dilakukan selama perjalanan.
    """
)

activity_chain = LLMChain(
    llm=llm,
    prompt=activity_prompt,
    output_key="activity_recommendations"
)

# Menggabungkan semua chain secara berurutan
travel_chain = SequentialChain(
    chains=[analysis_chain, hotel_chain, activity_chain],
    input_variables=["user_input"],
    output_variables=["travel_analysis", "hotel_recommendation", "activity_recommendations"],
    verbose=True
)


def format_final_response(chain_output):
    """Format output dari chain menjadi respons yang mudah dibaca"""
    try:
        analysis = json.loads(chain_output["travel_analysis"])
        formatted_analysis = (
            f"📍 Tujuan: {analysis['destination']}\n"
            f"⏱️ Durasi: {analysis['duration']} hari\n"
            f"🎯 Tujuan: {analysis['purpose']}\n"
            f"👥 Jumlah orang: {analysis['num_travelers']}"
        )
    except:
        formatted_analysis = chain_output["travel_analysis"]

    return (
        "=== ANALISIS PERJALANAN ===\n"
        f"{formatted_analysis}\n\n"
        "=== REKOMENDASI HOTEL ===\n"
        f"{chain_output['hotel_recommendation']}\n\n"
        "=== AKTIVITAS YANG DIREKOMENDASIKAN ===\n"
        f"{chain_output['activity_recommendations']}"
    )


# Fungsi utama untuk menjalankan chain
def plan_travel(user_input):
    # Jalankan chain
    results = travel_chain({"user_input": user_input})

    # Format hasil
    final_response = format_final_response(results)

    return final_response


# Contoh penggunaan
if __name__ == "__main__":
    user_query = "Saya ingin liburan ke Bali selama 5 hari dengan keluarga (4 orang)"
    response = plan_travel(user_query)
    print(response)

    print("\n" + "=" * 50 + "\n")

    another_query = "Saya perlu menghadiri konferensi di Jakarta selama 3 hari"
    response = plan_travel(another_query)
    print(response)