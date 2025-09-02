from langchain.embeddings import OpenAIEmbeddings
from langchain_qudrant import QdrantVectorStore

from openai import OpenAI
from dotenv import load_dotenv
#vector embedding and storing in vector db (qdrant)

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")      # using openAI embedding model


# connect to existing collection in qdrant mltb jo pdf se banaya gya tha use yaha pr lana hoga
vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333", 
    embedding=embeddings,
    collection_name="learnig_vector_store",
)


# take user query 

query = input("Enter your query: ")

# vector simillarity search (query) in vector db (qdrant)
search_result = vector_store.similarity_search(query=query) 


# jaha jaha pdf me match mila hoga uska content, page number and file location ko context me store krna hoga

context = "\n\n".join([f"page content :f{result.page_content} \n Page Number : {result.metadata['page_label']} \n file Location : f{result.metadata['source']}" for result in search_result])



system_prompt = """You are a helpful assistant that helps people find information about Node.js from the provided context. 

you should only provide answers based on the context below. If the context does not contain the answer, respond with "I don't know".

Context: {context}



"""



client = OpenAI()
load_dotenv()



response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt.format(context=context)},
        {"role": "user", "content": query},
    ],
    temperature=0.2,
    max_tokens=500,
)
print(response.choices[0].message.content)





