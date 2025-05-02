from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, RunnableMap, RunnableSequence, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from dotenv import load_dotenv
load_dotenv()

#There are 3 types of chaining in langchain- sequnetial,parallel and conditional
#pipe operator and runnable lambda are used to execute the chain in sequential manner
#runnable parallel is used to execute the chain in parallel manner and combine the output
#This code is a example of parallel chaining using runnable lambda and runnable parallel
#previous code is a example of sequential chaining using runnable lambda and runnable sequence
# In this we are getting various info of stranger things under chain parlallely and then finally combining the output


open_ai_model=ChatOpenAI(model="gpt-4o-mini",temperature=0.7)
template="Hi, I want to know the characters, number of episodes and plot of stranger things {season} what is the plot of {season} chapter of stranger things?"
message=[
    SystemMessagePromptTemplate.from_template("I am a stranger things huge fan and I want to know about the {season} season."),
    HumanMessagePromptTemplate.from_template("I am a stranger things huge fan and I want a certain information about the {season} season")
]
prompt=ChatPromptTemplate.from_messages(message)
prints=RunnableLambda(lambda x: print(x))
season=input("Enter the season: ") 
def get_episodes(season):
    
    template="Hi, I want to know the number of episode in chapter {season}"
    return ChatPromptTemplate.from_template(template)


def get_funfacts(season):
   template="tell me 2 behind the scenes fun facts about the plot of chapter {season} in brief"
   return ChatPromptTemplate.from_template(template)

def get_rating(season):
   template="rating of chapter {season} of in brief" 
   return ChatPromptTemplate.from_template(template)

def get_cast(season):
    template="list of the cast of chapter {season} "
    return ChatPromptTemplate.from_template(template)


def combine(x):
    return "Hi this is the information about the season of stranger things"+"\n"+"\n"+"number of episodes are "+x["episodes"]+"\n\n"+"Hey Fun facta here "+x["funfacts"]+"\n\n"+x["cast"]+"\n\n"+x["rating"]
    

format=RunnableLambda(lambda x: prompt.invoke(x))
Rpenai=RunnableLambda(lambda x: open_ai_model.invoke(x))
output=RunnableLambda(lambda x: StrOutputParser())

chain= format|Rpenai| output|RunnableParallel(branches={"episodes":get_episodes|Rpenai|output, "funfacts":get_funfacts|Rpenai|output, "cast":get_cast|Rpenai|output,"rating":get_rating|Rpenai|output})|RunnableLambda(lambda x: combine(x["branches"]))|prints
result=chain.invoke({"season":season})
