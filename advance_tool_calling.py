import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
search_tool = DuckDuckGoSearchRun()


# Fungsi untuk melakukan pencarian dengan validasi
def search_articles(query):
    try:
        # Tambahkan kata kunci tambahan untuk memastikan hasil yang lebih relevan
        enhanced_query = f"{query} latest news articles"
        search_results = search_tool.run(enhanced_query)

        # Validasi hasil pencarian
        if len(search_results.strip()) < 50:  # Jika hasil terlalu pendek
            return None

        return search_results
    except Exception as e:
        print(f"Error dalam pencarian: {str(e)}")
        return None


# Template prompt untuk ringkasan dalam Bahasa Inggris
summary_template = """
Please provide a comprehensive summary in English of the following text about artificial intelligence developments:
{text}

Focus on the key points and recent developments. The summary should be at least 3-4 sentences long.

Summary:
"""
summary_prompt = PromptTemplate(template=summary_template, input_variables=["text"])
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

# Template prompt untuk terjemahan ke Bahasa Indonesia
translation_template = """
Translate the following English text to Indonesian accurately and naturally:
{text}

Indonesian translation:
"""
translation_prompt = PromptTemplate(template=translation_template, input_variables=["text"])
translation_chain = LLMChain(llm=llm, prompt=translation_prompt)

# Contoh penggunaan
if __name__ == "__main__":
    # 1. Cari artikel
    search_query = "artificial intelligence latest developments 2024"
    search_results = search_articles(search_query)

    if search_results and len(search_results.strip()) > 0:
        # 2. Buat ringkasan dalam Bahasa Inggris
        summary = summary_chain.run(text=search_results)
        print("\nSummary:")
        print(summary)

        # 3. Terjemahkan ringkasan ke Bahasa Indonesia
        translation = translation_chain.run(text=summary)
        print("\nTerjemahan:")
        print(translation)
    else:
        print(
            "\nMaaf, tidak dapat menemukan hasil pencarian yang memadai. Silakan coba dengan kata kunci yang berbeda.")
