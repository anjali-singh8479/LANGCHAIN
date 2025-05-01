from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_openai import ChatOpenAI
# from langchain.output_parsers import StrOutputParser

from langchain_core.output_parsers import StrOutputParser

# from langchain.schema.output_parsers import StrOutputParserpip show langchain

from dotenv import load_dotenv
load_dotenv()
open_ai_model=ChatOpenAI(model="gpt-4o-mini")

template="Hi, I will help to get the {language} word for given english word.what is a {language} word for {word}"
# message=[{"system", "I want to learn {language}."},
# {"human", {template}}]
message=[
    SystemMessagePromptTemplate.from_template("I want to learn {language}."),
    HumanMessagePromptTemplate.from_template(template)
]
while True:
    word=input("Enter the english word:")
    if (word=="exit"):
        print("Exiting the program.")
        break
    language=input("Enter the language:")
    prompt=ChatPromptTemplate.from_messages(message)
    # "|" operator is used to chain the prompt and the model together
    # stroutputparser is used to parse the output of the model
    chains= prompt|open_ai_model|StrOutputParser()
    promp=chains.invoke({"word":word, "language":language})
    print(promp)
