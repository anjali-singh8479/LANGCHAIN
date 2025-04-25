from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from dotenv import load_dotenv

load_dotenv()
open_ai_model=ChatOpenAI(model="gpt-4o-mini")
# open_ai_model=ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=1000)
template="Hi, I will help to get the {language} word for given english word.what is a {language} word for {word}"
message=[
    SystemMessagePromptTemplate.from_template("I want to learn {language}."),
    HumanMessagePromptTemplate.from_template(template)
]

while True:
    word=input("Enter the word: ")
    if(word == "exit"):
        print("Exiting the program.")
        break
    language=input("Enter the language: ")
    # prompt=ChatPromptTemplate.from_template(template)
    prompt=ChatPromptTemplate.from_messages(message)
    question=prompt.invoke({"word":word, "language":language})
    response=open_ai_model.invoke(question)
    print("AI : "+response.content)