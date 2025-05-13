# in part 1 we have created chunks then embeddings and then stored the vectors in db folder
# in part 2 we have to get the most specific vector related to the query and then print the output
# pip install sentence-transformers
# pip install langchain langchain-community
# (using google claud instaed of open ai in rags)

import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

current_dir=os.path.dirname(os.path.abspath(__file__))
persistent_dir=os.path.join(current_dir,"db")
file_path=os.path.join(current_dir,"documents","stranger_things.txt")

loader=TextLoader(file_path=file_path)
document=loader.load()

text_spliter=CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
docs=text_spliter.split_documents(document)

embedding_model=HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vector_store=FAISS.from_documents(docs,embedding_model)
query="where does stranger things took place?"

# similar_chunks=vector_store.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs={'k': 2, 'score_threshold': 0.1}
# )
# this invoke has to be done only while using as retervier and not with similarity_search
# retervial_doc=similar_chunks.invoke(query)

# threshold score ranges from 0 to 1 means how much accurate chunks need to be fetched
similar_chunks=vector_store.similarity_search(query, k=3)

for i, doc in enumerate(similar_chunks):
    print(f"\n document {i}\n-{doc.page_content}\n\n")



