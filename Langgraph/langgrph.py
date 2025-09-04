from typing_extensions import TypedDict

from langgraph.graph import StateGraph , START , END

from openai import OpenAI 
from dotenv import load_dotenv

load_dotenv() ; 
client = OpenAI() 
# creating a state usme query ko string bna diye and result jo hoga vo bhi string

class State(TypedDict):
    query : str 
    llm_result:str | None         
    
    
 # creating NOde of langgraph
 
def chat_bot(state:State):
    query = state['query']
    # query ko le liy e
    # llm call krenge thrn reuslt return kr denge 
    
    llm_response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [{"role": "user", "content": query},]
        
    )
    
    
    #eg
    result = llm_response.choices[0].message.content
    # update kr do purane sate k result ko
    state["llm_result"] = result
    
    # return lr denge state ko
    return state   




# abb hme edeges ko banani hai

graph_builder = StateGraph(State)

# graph builder me node ko add kr denge jitne bhi honge 
graph_builder.add_node("chat_bot", chat_bot)  #(name , function/module name)
graph_builder.add_edge(START ,"chat_bot")
graph_builder.add_edge("chat_bot" , END)


graph = graph_builder.compile()




def main():
    user = input("ask something")
    _state = {
        "query" : user , 
        "llm_result" : None
    }
    # abb jo graph hmne upar banya use invoke krna hai run krne k liye 
    
    graph_result = graph.invoke(_state);
    print("graph_result" , graph_result)
    
main()    
    