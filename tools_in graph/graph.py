from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain.tools import BaseTool, tool
import requests
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode , tools_condition 

load_dotenv()

# jo function hm agentic ai wale me bnaye the same usi ko use krna hai and usme thoda modification krna hai
# tool ko define krne k liye hm langchain ka tool use krenge usme hm ek decorator use krenge @tool jo fuctnion ko tool me convert kr dega
@tool()
def get_current_weather(location: str) -> str:
    
    # yaha pr description dena mandtory hota hai tabhi graph pehchan payega ki ye tools ka work kya hai
    """ this tools is used to get the current weather of a location """
    
    url = f"https://api.weatherapi.com/v1/current.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"The current weather in {location} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data at the moment."

@tool()
def run_command(cmd : str) : 
    result = os.system(cmd)
    return result   

# jitne tools hai usko ek array me rakh denge
tools = [get_current_weather , run_command]

class State(TypedDict):
    messages: Annotated[list, add_messages] 

llm = init_chat_model(model_provider="openai", model="gpt-4.1")
# yaha tools ko bind kr denge llm k sath
llm_with_tools =llm.bind_tools(tools)    
    
def chatbot(state:State):
    # yaha pr llm_with_tools ko invoke krna hai
    message = llm_with_tools.invoke(state["messages"])
    return {"messages":[message]}


tool_node = ToolNode(tools=[get_current_weather , run_command])
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

# tools_node ko bhi add kr denge graph me
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")

# conditional edge lagayenge chatbot se tools node k liye
graph_builder.add_conditional_edge("chatbot",  tools_condition)
# agr ouput dega "action_required":true to tools node pr jayega fir se result lane k liye agr false to direct end pr chala jayega
graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge("chatbot", END)    

graph = graph_builder.compile()    
    
def main():
    user_query = input("ask something")
    
    state = State(messages=[{"role":"user","content":user_query}])
    
    result = graph.invoke(state)
    print(result)    