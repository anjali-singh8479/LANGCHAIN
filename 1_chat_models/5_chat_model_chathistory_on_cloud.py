#First login to firebase and create a database & project and get the project id
#install google cloud cli and then login
# run pip install langchain-google-firestore

from google.cloud import firestore
# this connects langchain with firebase firestore

from langchain_google_firestore import FirestoreChatMessageHistory
# this is used to store and reterive chat to & from firestore
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()



ProjectID="langchain-aa644"
Session_ID="User_chat_session_"+ strhi(datetime.now()) # this can be a user name or any thing unique
Collection_name="Langchain_user_chats"
client=firestore.Client(project=ProjectID)

chathistory=FirestoreChatMessageHistory(
   session_id=Session_ID,
   collection=Collection_name,
   client=client,
)
collection_ref=client.collection(Collection_name)
print("Chat History messages")
print(chathistory.messages)
openai_model=ChatOpenAI(model="gpt-4o-mini")


while True:
    question=input("You :")
    if(question == "end"):
        break
    chathistory.add_user_message(question)
    response=openai_model.invoke(chathistory.messages)
    chathistory.add_ai_message(response.content)
    print("AI : "+response.content)