from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)

# Prompt template for multiple questions
multi_template = """Answer the following questions one at a time.

Questions:
{questions}

Answer:
"""

long_prompt = PromptTemplate(
    template=multi_template,
    input_variables=["questions"]
)

# Create chain
llm_chain = long_prompt | llm

# Multiple questions
qs_str = (
    "Which NFL team won the Super Bowl in the 2010 season?\n"
    "If I am 6 ft and 4 inches, how tall am I in centimeters?\n"
    "Who was the 12th person on the Moon?\n"
    "How many eyes does a blade of grass have?"
)

# Run the chain
response = llm_chain.invoke({"questions": qs_str})

print(response.text)