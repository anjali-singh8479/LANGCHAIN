from langchain_core.runnables import RunnableLambda, RunnableMap, RunnableSequence
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from dotenv import load_dotenv
load_dotenv()   


open_ai_model=ChatOpenAI(model="gpt-4o-mini")
template="Hi, I will help to get the {language} word for given english word.what is a {language} word for {word}"
message=[
    SystemMessagePromptTemplate.from_template("I want to learn {language}."),
    HumanMessagePromptTemplate.from_template(template)
]

word=input("Enter the word: ")
language=input("Enter the language: ")
prompt=ChatPromptTemplate.from_messages(message)

# runnablelambda is a class in langchain to execute chain without pipe operator
format=RunnableLambda(lambda x: prompt.invoke(x))
Rpenai=RunnableLambda(lambda x: open_ai_model.invoke(x))
output=RunnableLambda(lambda x: StrOutputParser())
prints=RunnableLambda(lambda x: print(x))
#runnablesequence is a class in langchain to execute chain of runnables in sequence. middle is a list and first and last are one always

chain=RunnableSequence(
    first=format,middle=[Rpenai, output], last=prints
)
chain.invoke({"word":word, "language":language})
