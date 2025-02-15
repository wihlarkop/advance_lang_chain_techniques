from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

# Set API Key
OPENAI_API_KEY = "your-api-key"

# Inisialisasi model OpenAI
llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY)


# Tool: Fetch cuaca dari API
def get_weather(city):
    fake_weather_data = {"Jakarta": "32°C, cerah", "Tokyo": "18°C, berawan"}
    return fake_weather_data.get(city, "Data tidak tersedia")


# Tool: Kalkulator sederhana
def calculator(expression):
    try:
        return eval(expression)
    except Exception:
        return "Ekspresi tidak valid"


# Routing berdasarkan input
def dynamic_router(user_input):
    if "cuaca" in user_input:
        city = user_input.split("cuaca di")[-1].strip()
        return f"Cuaca di {city}: {get_weather(city)}"

    elif any(op in user_input for op in ["+", "-", "*", "/"]):
        return f"Hasil: {calculator(user_input)}"

    else:
        messages = [HumanMessage(content=user_input)]
        return llm(messages).content


# Contoh penggunaan
inputs = ["Berapa cuaca di Jakarta?", "12 + 5 * 2", "Ceritakan tentang sejarah AI."]
for user_input in inputs:
    print(f"Input: {user_input}")
    print(f"Output: {dynamic_router(user_input)}\n")
