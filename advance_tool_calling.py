from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

OPENAI_API_KEY = ""

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)
search_tool = DuckDuckGoSearchRun()


# Fungsi untuk melakukan pencarian
def search_articles(query):
    try:
        search_results = search_tool.run(query)
        return search_results
    except Exception as e:
        print(f"Error dalam pencarian: {str(e)}")
        return None


# Template prompt untuk ringkasan dalam Bahasa Inggris
summary_template = """
Please provide a summary of the following text in English:
{text}

Summary:
"""
summary_prompt = PromptTemplate(template=summary_template, input_variables=["text"])
summary_chain = LLMChain(llm=llm, prompt=summary_prompt)

# Template prompt untuk terjemahan
translation_template = """
Terjemahkan teks berikut ke dalam Bahasa Indonesia:
{text}

Terjemahan:
"""
translation_prompt = PromptTemplate(template=translation_template, input_variables=["text"])
translation_chain = LLMChain(llm=llm, prompt=translation_prompt)

# Contoh penggunaan
if __name__ == "__main__":
    # 1. Cari artikel
    search_query = "Latest developments in artificial intelligence"
    search_results = search_articles(search_query)

    if search_results:
        # 2. Buat ringkasan
        summary = summary_chain.run(text=search_results)
        print("\nRingkasan:")
        print(summary)

        # 3. Terjemahkan ringkasan
        translation = translation_chain.run(text=summary)
        print("\nTerjemahan:")
        print(translation)
