
#flake8:noqa
from typing_extensions import TypedDict

from langgraph.graph import StateGraph , START , END

from openai import OpenAI 
from dotenv import load_dotenv

from pydantic import BaseModel
load_dotenv() ; 
client = OpenAI() 

# output ko boolena me lane k liye use hua hai                 77 pydentice ek validation model hai  
class ClassifyMessageResponse(BaseModel):
    is_coding_problrm:bool


# design state 

class State(TypedDict):
    user_query : str
    llm_res : str | None
    accuracy_percentage: str | None
    is_coding_problrm : bool | None

 
# design nodes
def classify_message(state:State):
    query = state["user_query"]   
    SYSTEM_PROMPT = """ 
    you are ai assiaant your job is to classify the user query is coding question or not , return reponse in spacified json boolean only 
    """ 
    
    
    # structure response k liye hm ek function bnaye hai jo json me dega ouput usiko response+fromat me pas kr denge 
    # isem beta use hota to create k jagah parse use krtehai 
    llm_reponse = client.beta.chat.completions.parse(
        model="gpt-3.5-turbo",
        response_format = ClassifyMessageResponse , 
        messages = [{"role": "system", "content": SYSTEM_PROMPT},{"role": "user", "content": query}]
    )
    is_coding_problrm = llm_reponse.choices[0].message.parsed.is_coding_problrm
    
    # state update kr do 
    state["is_coding_problrm"] = is_coding_problrm
    return state 


# abb yaha decide ho jayega ki query kaisa hai uske basis pr hm next step choose krenge ki kaun sa hoga 

# simply hm routing krenge yaha

def route_query(state:State):
    pass 


# non coding node

def non_coding(state:State):
    pass


def coding(state:State):
    pass

def coding_validate(state:State):
    pass



#crating graph 

graph_builder = StateGraph(State)

# graph builder me node ko add kr denge jitne bhi honge i.e node define 
graph_builder.add_node("classify_message", classify_message) 
graph_builder.add_node("route_query", route_query) 
graph_builder.add_node("non_coding", non_coding) graph_builder.add_node("coding", coding) graph_builder.add_node("coding_validate", coding_validate) 


# linking nodes 
graph_builder.add_edge(START ,"classify_message")
graph_builder.add_conditional_edges("classify_message", route_query)
graph_builder.add_edge( "non_coding",END)
graph_builder.add_edge( "coding","coding_validate")
graph_builder.add_edge( "coding_validate",END)


