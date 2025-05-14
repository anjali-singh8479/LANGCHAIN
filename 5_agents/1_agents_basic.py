from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain.agents import create_react_agent,AgentExecutor
from langchain.tools import tool
import requests
import datetime
load_dotenv()
 
#@ tool points that this is the tool passes, description is necessary to identify which tool to use
@tool
def get_exchange_rate(query: str) -> str:
    """ Get current currency exchange rate."""
    try:
        from_currency, to_currency = query.upper().split(" TO ")
        url = f"https://api.frankfurter.app/latest?amount=1&from={from_currency}&to={to_currency}"
        response = requests.get(url)
        data = response.json()
        # print(data)
        rate = data["rates"].get(to_currency)
        if rate:
            return f"1 {from_currency} = {rate:.2f} {to_currency}"  
        else: 
            return "Exchange rate not found"
    except Exception as e:
        return f"Error: {str(e)}"
    
@tool
def get_current_time(format:str="%y-"
"%m-%d %H:%M:%S"):
    """ returns current time in specified format"""
    try:
        current_time=datetime.datetime.now()
        formatted_time=current_time.strftime(format)
        if(formatted_time):
            return formatted_time
        else:
            return "current time not found"
    except Exception as e:
        return e
   
openai_model=ChatOpenAI(model="gpt-4o-mini")

query="how many yen are there in rupees?"
# query="what time it is now in london(you are in india)?"


# prompt=PromptTemplate.from_template("{input}")
# chain=prompt|openai_model|StrOutputParser()
# response=chain.invoke({"input":query})
# print(response)


# pip install langchainhub- this allows you to use other people's 
# template on internet intead of creating your own(no need to use prompt template now)
# we will be using reACT template for this(this is not a frontend framework)

prompt=hub.pull("hwchase17/react")

# agent will be require some tools out of those he will find out the suitable 
# one to fetch the response like to email sending tool, or google search or a fucntion etc.
tools=[get_exchange_rate,get_current_time]

# after tools we need to create a agent 
agent=create_react_agent(openai_model,tools,prompt)

# after creating agent setup agent executor
agent_executor=AgentExecutor(agent=agent,tools=tools,verbose=True)
# setting verbose true gives out the each step agent is performing

# next invoke agent_executor
response=agent_executor.invoke({"input":query})



""" response received here is that- it cannot fetch real time data 
here comes agents and tools into picture where agents can provide 
response using their own reasoning to figure out the most suitable tool for the query
"""
