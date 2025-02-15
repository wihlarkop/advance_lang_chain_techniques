from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool


#  Buat Custom Tool untuk Konversi Mata Uang
@tool
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Mengonversi jumlah uang dari satu mata uang ke mata uang lain dengan nilai tukar tetap."""
    exchange_rates = {
        ("USD", "EUR"): 0.85,
        ("EUR", "USD"): 1.18,
        ("USD", "IDR"): 15000,
        ("IDR", "USD"): 0.000067
    }

    rate = exchange_rates.get((from_currency, to_currency), None)
    if rate is None:
        return f"Konversi dari {from_currency} ke {to_currency} tidak tersedia."

    converted_amount = amount * rate
    return f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"


# Inisialisasi Model OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Inisialisasi Agent dengan Tool
agent = initialize_agent(
    tools=[convert_currency],  # Menggunakan custom tool
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

#  Menjalankan Agent untuk Konversi Mata Uang
response = agent.run("Konversikan 200 USD ke IDR.")
print(response)
