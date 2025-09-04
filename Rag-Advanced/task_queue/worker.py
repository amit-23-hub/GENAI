
from langchain_qudrant import QdrantVectorStore

from langchain_openai import OpenEmbeddings 

from openai import OpenAI



# RQ polling krta rahata hai jaise hi koi query aayegi to usko iss file k top me la dega 
# fir usko hm ebmedding bna kr qdrant me search krke context nikalenge
# fir us context ko openai k model me dalenge or answer nikalenge


client = OpenAI()

embeddings = OpenEmbeddings(model="text-embedding-3-small")      # using openAI embedding model

# connect to existing collection in qdrant mltb jo pdf se banaya gya tha use yaha pr lana hoga jo indexing.py me bna tha
# and usme url me localhost ki jagah vector-db use krna hoga kyuki ab ye docker compose me h to waha pr ye service ka name h

vector_store = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333", 
    embedding=embeddings,
    collection_name="learnig_vector_store",
)

# serach krna hai  ye to jo queue k through aayega use krnge 


async def process_query(query: str):
    print(f"searching  query: {query}")
    search_result = vector_store.similarity_search(query=query)
    
    context = "\n\n".join([f"page content :f{result.page_content} \n Page Number : {result.metadata['page_label']} \n file Location : f{result.metadata['source']}" for result in search_result])
    
    system_prompt = f"""You are a helpful assistant that helps people find information about Node.js from the provided context. 

    you should only provide answers based on the context below. If the context does not contain the answer, respond with "I don't know".

    Context:{context}



    """    
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_prompt.format(context=context)},
        {"role": "user", "content": query},
    ],
    temperature=0.2,
    max_tokens=500,
    )
    
    # save to  db
    print(f" {query}" , response.choices[0].message.content)

    
    
    