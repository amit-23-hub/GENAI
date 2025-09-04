from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.types import interrupt, Command
import json

@tool()

def human_assistance(query: str) -> str:
    """this tool is used to get human assistance for complex queries"""
    
    human_response = interrupt({"query": query})  # this save the state in db and wait for human response
    return human_response['data']

tools = []

class State(TypedDict):
    messages: Annotated[list, add_messages] 
    
    
llm = init_chat_model(model_provider="openai", model="gpt-4.1")
# yaha tools ko bind kr denge llm k sath
llm_with_tools =llm.bind_tools(tools)   

def chatbot(state:State):
    # yaha pr llm_with_tools ko invoke krna hai
    message = llm_with_tools.invoke(state["messages"])
    return {"messages":[message]}


graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")

# conditional edge lagayenge chatbot se tools node k liye
graph_builder.add_conditional_edge("chatbot",  tools_condition)
# agr ouput dega "action_required":true to tools node pr jayega fir se result lane k liye agr false to direct end pr chala jayega
graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge("chatbot", END)  


def compile_graph_with_checkpointer(checkpointer):
    graph_with_checkpointer = graph_builder.compile(checkpointer=checkpointer)
    return graph_with_checkpointer





def user_chat():
    #   mongodb://<username>:<pass>@<host>:<port>
    DB_URI = "mongodb://admin:admin@mongodb:27017"
    config = {"configurable": {"thread_id": "1",}}
    
# mongodb k sath checkpointer bna diye and connect kr diye database se
    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:

        graph_with_mongo = compile_graph_with_checkpointer(mongo_checkpointer)

        query = input("> ")
        
        state = State(messages=[{"role":"user","content":query}])

        for event in graph_with_mongo.stream_invoke(
            state, config):

            if "messages" in event:
                (event["messages"][-1]["content"]).pretty_print()
                





def admin_call():
    DB_URI = "mongodb://admin:admin@mongodb:27017"
    config = {"configurable": {"thread_id": "21"}}

    with MongoDBSaver.from_conn_string(DB_URI) as mongo_checkpointer:
        graph_with_cp = create_chat_graph(mongo_checkpointer)

        state = graph_with_cp.get_state(config=config)
        last_message = state.values['messages'][-1]

        tool_calls = last_message.additional_kwargs.get("tool_calls", [])

        user_query = None

        for call in tool_calls:
            if call.get("function", {}).get("name") == "human_assistance":
                args = call["function"].get("arguments", "{}")
                try:
                    args_dict = json.loads(args)
                    user_query = args_dict.get("query")
                except json.JSONDecodeError:
                    print("Failed to decode function arguments.")

        print("User Has a Query", user_query)
        solution = input("> ")

        resume_command = Command(resume={"data": solution})

        for event in graph_with_cp.stream(resume_command, config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print()


user_chat()
     