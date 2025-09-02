from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
client = OpenAI()
from langchain.embeddings import OpenAIEmbeddings
from langchain_qudrant import QdrantVectorStore



pdf_path = Path(__file__).parent / "nodejs.pdf"

loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# print(docs[5])  # print first 500 chars

# chunking

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
)
texts = text_splitter.split_documents(docs)

# embedding  using openAI embedding model and storing in vector db (qdrant)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")      # using openAI embedding model


vector_store = QdrantVectorStore.from_documents(
    texts,
    embeddings,
    collection_name="learnig_vector_store",
    url="http://localhost:6333",  # Qdrant URL

)





