from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter
import os

current_dir=os.path.dirname(os.path.abspath(__file__))
book_dir=os.path.join(current_dir,"documents")
db_dir=os.path.join(current_dir,"db","chroma_db_with_metadata")
if( not os.path.exists(book_dir)):
    print(" db file does not exists")
all_books=os.listdir(book_dir)

documents=[]
for i, book in enumerate(all_books):
    if(book.endswith(".txt")):
        file_path=os.path.join(book_dir,book)
        loader=TextLoader(file_path)
        document=loader.load()
        for doc in document:
            doc.metadata={"source":file_path,"book_name":book}
            documents.append(doc)

text_splitter=CharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
docs=text_splitter.split_documents(documents)

embedding_model=HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)  
vector_store=FAISS.from_documents(docs,embedding_model)
# vector_store.save_local(db_dir)

query="who is atlas?"

similar_chunks=vector_store.similarity_search(query,k=3)
for i, doc in enumerate(similar_chunks):
    print(f"document {i}\n {doc.page_content}\n{doc.metadata}\n")

    
