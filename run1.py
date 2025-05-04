import json
from dotenv import load_dotenv
from os import getenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
API_KEY = getenv("GOOGLE_GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=API_KEY
)

system_message = SystemMessage(
    content="\n".join([
        "You are a helpful AI agent that supports English and Filipino.",
        "You only answer product-related questions based on a provided list.",
        "Respond ONLY in JSON format using the following keys:",
        "- 'type': either 'object' or 'array'",
        "- 'message': a human-readable explanation",
        "- 'payload': a JSON object or array with full product details (id, product, price)",
        "Reject questions unrelated to product info.",
        "Use the currency symbol '₱'."
    ])
)

human_message = HumanMessage(
    content="Here is the product list:\n{product_list}\n\nQuestion: {question}"
)

prompt = ChatPromptTemplate.from_messages([
    system_message,
    human_message
])

parser = JsonOutputParser()

chain = prompt | llm | parser

def query_product_list(product_list: list, question: str):
    try:
        response = chain.invoke({
            "product_list": json.dumps(product_list, indent=2),
            "question": question
        })
        
        # Check if the response is valid and product-related
        if "error" in response or "payload" not in response:
            raise ValueError("The response is not valid or not related to product info.")
        
        # Check for any invalid responses that do not match product info format
        if response["type"] not in ["object", "array"] or not isinstance(response["payload"], (dict, list)):
            raise ValueError("The response payload does not follow the correct format.")
        
        return response
    
    except Exception as e:
        return {
            "error": "Failed to parse or process the response.",
            "details": str(e)
        }

# Main script for testing or CLI use
if __name__ == "__main__":
    test_db = [
        {"id": 1, "product": "Nike Shoe", "price": 100},
        {"id": 2, "product": "Adidas Shoe", "price": 200},
        {"id": 3, "product": "Puma T-Shirt", "price": 30}
    ]

    question = input("Ask a product-related question: ")
    result = query_product_list(test_db, question)
    print(json.dumps(result, indent=2, ensure_ascii=False))
