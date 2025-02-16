from langchain.tools import DuckDuckGoSearchRun, Tool
from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI

# Inisialisasi model LLM
OPENAI_API_KEY = "your-api-key"
llm = OpenAI(openai_api_key=OPENAI_API_KEY)

# Inisialisasi search tool
search_tool = DuckDuckGoSearchRun()


# Definisi kalkulator sebagai tool
def calculator(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid expression"


calculator_tool = Tool(name="Calculator", func=calculator, description="Solves math expressions.")

# Menggabungkan tools ke dalam agent
tools = [search_tool, calculator_tool]
agent = initialize_agent(
    tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

if __name__ == "__main__":

    # Menjalankan agent dengan input pengguna
    user_input = "Calculate 8 * 12 and search latest Python updates"
    response = agent.run(user_input)

    print("Agent Response:\n", response)
