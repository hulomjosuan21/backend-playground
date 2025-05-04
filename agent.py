import json
from dotenv import load_dotenv
from os import getenv
from typing import Union
from pydantic import BaseModel

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from langchain_core.messages import SystemMessage

load_dotenv()
API_KEY = getenv("GOOGLE_GEMINI_API_KEY")

class Response(BaseModel):
    type: str
    message: str
    payload: Union[dict, list]

def product_database():
    return [
        {"id": 1, "product": "Nike Shoe", "price": "100"},
        {"id": 2, "product": "Adidas Shoe", "price": "200"},
        {"id": 3, "product": "Puma T-Shirt", "price": "30"},
        {"id": 4, "product": "Reebok Shorts", "price": "60"},
        {"id": 5, "product": "New Balance Cap", "price": "25"},
        {"id": 6, "product": "Fila Jacket", "price": "120"}
    ]

db_tool = Tool(
    name="product_database",
    func=product_database,
    description="Returns a list of products (id, product, price). Use this tool to retrieve product data when asked about any item or price."
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=API_KEY
)

system_message = SystemMessage(
    content="\n".join([
        "You are a helpful AI agent that answers product-related questions from the list provided below.",
        "Your task is to respond directly with the product's price if the product name is mentioned.",
        "Please respond ONLY in JSON format using the following keys:",
        "- 'type': This will be either 'object' or 'array' depending on the response format.",
        "- 'message': A clear, easy-to-understand explanation that answers the user's query.",
        "- 'payload': A JSON object or array containing the full product details (id, product, price) for the relevant results.",
        "If the product is not found, say that the product could not be located.",
        "Always display prices using the currency symbol '₱'.",
        "Your tone should be friendly, professional, and helpful."
    ])
)

prompt = ChatPromptTemplate.from_messages([
    system_message,
    ("human", "Here is the product list:\n{product_list}\n\nQuestion: {question}"),
    ("placeholder", "{agent_scratchpad}")
])

parser = PydanticOutputParser(pydantic_object=Response)

tools = [db_tool]

agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)

if __name__ == "__main__":
    try:
        user_query = input("Ask AI: ")

        product_list = product_database()
        raw_response = agent_executor.invoke({
            "product_list": product_list,
            "question": user_query,
            "agent_scratchpad": ""
        })

        parsed = parser.parse(raw_response["output"])
        if not parsed.payload or (isinstance(parsed.payload, dict) and not parsed.payload):
            raise ValueError("❌ Invalid request: Only product-related questions are allowed.")

        if isinstance(parsed.payload, dict):
            parsed.payload["price"] = f"{parsed.payload['price']}"
        elif isinstance(parsed.payload, list):
            for item in parsed.payload:
                item["price"] = f"{item['price']}"

        print("\n✅ Response:")
        print(json.dumps(dict(parsed), indent=2, ensure_ascii=False))
    except Exception as e:
        print("\n❌ Error occurred:")
        print(str(e))
