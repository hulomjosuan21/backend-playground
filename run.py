import json
from dotenv import load_dotenv
from os import getenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import SystemMessage

load_dotenv()
API_KEY = getenv("GOOGLE_GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=API_KEY)

system_message = SystemMessage(
    content="\n".join([
        "You are a friendly and helpful AI agent that can assist users in both English and Filipino.",
        "Your task is to answer product-related questions based on the list provided below.",
        "Please respond ONLY in JSON format using the following keys:",
        "- 'type': This will be either 'object' or 'array' depending on the response format.",
        "- 'message': A clear, easy-to-understand explanation that answers the user's query.",
        "- 'payload': A JSON object or array containing the full product details (id, product, and price) for the relevant results.",
        "If the question is not related to the product information, kindly inform the user that you only handle product-related inquiries.",
        "Always display prices using the currency symbol '₱'.",
        "Your tone should be friendly, professional, and helpful."
    ])
)

prompt = ChatPromptTemplate.from_messages([
    system_message,
    ("human", "Here is the product list:\n{product_list}\n\nQuestion: {question}")
])

parser = JsonOutputParser()

chain = prompt | llm | parser

def query_product_list(product_list: list, question: str):
    try:
        response = chain.invoke({
            "product_list": json.dumps(product_list, indent=2),
            "question": question
        })
        return response
    except Exception as e:
        return {
            "error": "Failed to parse or process the response.",
            "details": str(e)
        }

if __name__ == "__main__":
    test_db = [
        {"id": 1, "product": "Nike Shoe", "price": 100},
        {"id": 2, "product": "Addidas Shoe", "price": 200},
        {"id": 3, "product": "Puma T-Shirt", "price": 30}
    ]

    question1 = input("Ask a product-related question: ")
    result = query_product_list(test_db, question1)
    print(json.dumps(result, indent=2, ensure_ascii=False))
