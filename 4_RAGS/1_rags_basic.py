# rags are used to help the llm to get data from external sources like files or databases
# rags basically doesn't search for exact words but for similar meaning
# for this first files are divided into number of chunks (all equal sizes) of token size of your choice
#tokens are the units of chunks it can be a character or a word
# after creating chunks, these are embedded into vector representation
# database "vector db" is used to store these vectors
# when user sends the prompt , the "retrival" will reterive chunks with meaning same as prompt and return it to the llm
import os
# getting the absolute path of current dir which is rags folder

current_dir=os.path.dirname(os.path.abspath(__file__))

# created a new dir in working dir
# os.mkdir("documnets")

# path for document folder from 1_rags_basic both are under current dir
# file_path=os.path.join(current_dir,"documents")

# changing the dir from rags_basic to documents to as to create a new file there
# os.chdir(file_path)

#creating a new file with write+read permissions
# with open("stranger_things.txt", 'w+') as fp:
#     pass
os.chdir(current_dir)
# os.mkdir("vectors")

#rename the dir
# os.rename(os.path.join(current_dir,"vectors"),"db")


os.chdir(os.path.join(current_dir,"db"))
with open("chroma_db" ,"w+") as fp:
   pass

