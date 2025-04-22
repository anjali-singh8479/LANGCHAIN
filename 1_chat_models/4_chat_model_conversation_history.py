from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from dotenv import load_dotenv
load_dotenv()
#creating openchat ai model
openai_model=ChatOpenAI(model="gpt-4o-mini")
chat_history=[]
chat_history.append(SystemMessage(content="Hi, How can i help you"))
while True:
   question=input("You : ")
   if(question=="end"):
      break
   chat_history.append(HumanMessage(content=question))
   response=openai_model.invoke(chat_history)
   print("AI :"+response.content)
   chat_history.append(AIMessage(content=response.content))
