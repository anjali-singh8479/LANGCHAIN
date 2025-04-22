from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
# these are the ai models are we are importing class from these

from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
from dotenv import load_dotenv
load_dotenv()
#creating openchat ai model
openai_model=ChatOpenAI(model="gpt-4o-mini")

#creating a anthropic model
anthropic_model=ChatAnthropic(model="claude-3-7-sonnet-20250219")

#creating a google chat model
google_model=ChatGoogleGenerativeAI(model="gemini-1.5-flash")

message=[
    SystemMessage(content="Roadmap for langchain"),
    HumanMessage(content="I am a developer and want to learn langchain , provide me a roadmap for this"),
]

# same process to invoke for all models
response=openai_model.invoke(message)
response=anthropic_model.invoke(message)
response=google_model.invoke(message)