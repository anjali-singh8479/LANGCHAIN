from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder,SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables import RunnableLambda, RunnableSequence, RunnableParallel, RunnableBranch
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

chathistory=[]

open_ai_model=ChatOpenAI(model="gpt-4o-mini",temperature=0.7)

message=[
    SystemMessagePromptTemplate.from_template("Hi i am playing a quiz game based on the movie {movie_name}"),
    HumanMessagePromptTemplate.from_template("provide me with a quiz question based on the movie {movie_name}."),
]  

global_info={"enter_answer":"","correct_answer":"","question":""}


# result=open_ai_model.invoke(format)

next_question=ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("continue playing a quiz game based on the movie {movie_name}"),
            HumanMessagePromptTemplate.from_template("provide a next question based on the movie {movie_name} with 4 options and correct answer.Avoid question which are there in {asked_questions} and also which have similar answer and meaning as there are in {asked_questions}")
        ])  

hint_needed=ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template("need a hint for question {question}  based on the movie {movie_name}"),
            HumanMessagePromptTemplate.from_template("provide me a hint for the question {question} based on the movie {movie_name}. Do not change the question. give a hint so that it can help me out to guess the answer for question {question}.")
        ]) 
    

def get_question(x):
    index = x.find("**Question:**")
    if index != -1:
        if(x.__contains__("**Answer**")):
            answer_index=x.find("Answer:**")
        else:    
           answer_index=x.find("Answer:**")
        question=StrOutputParser().parse(x[index:answer_index])
        correct_answer=StrOutputParser().parse(x[answer_index:])
        print("Correct Answer: ",correct_answer)
        print(question)
        chathistory.append(question)
        enter_answer=input("Enter the answer: ")
        global_info.__setitem__("enter_answer",enter_answer)
        global_info.__setitem__("correct_answer",correct_answer)
        global_info.__setitem__("question",question)
        return {"enter_answer":enter_answer,"correct_answer":correct_answer,"question":question}
    return {"enter_answer":"","correct_answer":"","question":""}

def check_answer(x):
    if(x["correct_answer"].lower().__contains__(x["enter_answer"].lower()+")")):
        print("Yeah !! you got it correct")
        return {"details":x,"answer_is":"Correct Answer"}
    else:
        print("ooh !! its wrong answer")
        return {"details":x,"answer_is":"Wrong Answer"}
    

def hint(x):
    hint_index=x.find("**Hint:**")
    hint=x[hint_index:]
    print("here is a hint -------- "+hint)
    enter_answer=input("Enter Your answer again ")
    correct_answer=global_info.get("correct_answer").lower()
    is_correct = correct_answer.__contains__(enter_answer.lower() + ")")
    updated_data = {
        "enter_answer": enter_answer,
        "correct_answer": correct_answer,
        "question": global_info.get("question", "")
    }
    if is_correct:
        print("Now correct!")
        return {"details": updated_data, "answer_is": "Correct Answer"}
    else:
        print("Still wrong.")
        return {"details": updated_data, "answer_is": "Correct Answer"}
     




prompt=ChatPromptTemplate.from_messages(message)
# format=prompt.invoke({"movie_name","stranger things"})
format=RunnableLambda(lambda x: prompt.invoke(x))
Rpenai=RunnableLambda(lambda x: open_ai_model.invoke(x))
output=RunnableLambda(lambda x: StrOutputParser().parse(x.content))


hint_chain = RunnableBranch(
    (lambda x: "Correct Answer" in x["answer_is"],
     RunnableLambda(lambda x: {
         "question": x["details"]["question"],
         "movie_name": "stranger things",
         "asked_questions":chathistory
     })|next_question | format | Rpenai | output | get_question | check_answer
    ),
    (lambda x: "Wrong Answer" in x["answer_is"],
 RunnableLambda(lambda x: {
     "question": x["details"]["question"],
     "movie_name": "stranger things",
     "correct_answer": x["details"]["correct_answer"]  # Pass it forward
 }) | hint_needed 
   | format 
   | Rpenai 
   | output 
   |hint
),
lambda x: print("default_chain")
)

branches = RunnableBranch(
    (lambda x: "Correct Answer" in x["answer_is"],
     RunnableLambda(lambda x: {
         "question": x["details"]["question"],
         "movie_name": "stranger things",
         "asked_questions":chathistory
     })|next_question | format | Rpenai | output | get_question | check_answer
    ),
    (lambda x: "Wrong Answer" in x["answer_is"],
 RunnableLambda(lambda x: {
     "question": x["details"]["question"],
     "movie_name": "stranger things",
     "correct_answer": x["details"]["correct_answer"]  # Pass it forward
 }) | hint_needed 
   | format 
   | Rpenai 
   | output 
   |hint|hint_chain
),
lambda x: print("default_chain")
)


while True:
    print("flow started")
    main_chain=format|Rpenai|output|get_question|check_answer
    chain=main_chain|branches
    open_ai=chain.invoke({"movie_name":"stranger things"})
    
#   print("Final Result: ",open_ai)