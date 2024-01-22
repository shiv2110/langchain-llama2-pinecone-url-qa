from langchain_community.document_loaders import UnstructuredURLLoader
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Pinecone
from pinecone import Pinecone as Pc
from langchain.docstore.document import Document
from dotenv import load_dotenv
import os
load_dotenv()


root_url = 'https://brainlox.com/courses/category/technical'
reqs = requests.get(root_url)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
urls = [root_url]
for link in soup.find_all('a'):
    sub_link = link.get('href')
    if "courses" in sub_link and "-" in sub_link:
        if "https://brainlox.com" + sub_link not in urls:
            urls.append("https://brainlox.com" + sub_link)


data = []
for url in urls:
    loader = UnstructuredURLLoader(urls = [url])
    page_data = loader.load()
    content = " ".join([e.page_content for e in page_data])
    doc_obj = Document(
        page_content = content,
        metadata = {"source" : url}
    )
    data.append(doc_obj)


text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 20)
docs = text_splitter.split_documents(data)
# print(len(docs))
# print(docs[2])

embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENV = os.getenv('PINECONE_API_ENV')

Pc(
    api_key = PINECONE_API_KEY,  
    environment = PINECONE_ENV  
)
index_name = os.getenv('PINECONE_INDEX')

docsearch = Pinecone.from_documents( docs, embeddings, index_name = index_name )
