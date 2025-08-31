
from openai import OpenAI
from dotenv import load_dotenv
client = OpenAI()
import json
import requests 
import os


load_dotenv() 

def get_current_weather(location: str) -> str:
    url = f"https://api.weatherapi.com/v1/current.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"The current weather in {location} is {data['current']['temp_c']}°C with {data['current']['condition']['text']}."
    else:
        return "Sorry, I couldn't fetch the weather data at the moment."

def run_command(cmd : str) : 
    result = os.system(cmd)
    return result

avaialble_tools = {
    "get_current_weather" : get_current_weather
    , "run_command" : run_command
 }
   

system_prompt = """
you are an helpful assistant that helps users to find information about various topics.
you have to answer in a very concise and precise manner.
if anyone is asking regarding anything just answer in a very precise way
you have to work on plan action observe and validate mode

for the given user query and available tools you have to come up with a plan to solve the user query
then you have to execute the plan step by step and observe the results 
based on planning you have to select best tools that are available to you to solve the user query based on selected tool you have to perform the operation and observe the results



rules : 
follow output in json format only
always follow one step at a time and wait for execution of next input from user
carefully anayze the user query and available tools before planning

output format :
    {{"step"} : "string" , 
    "content" : "string" , 
    "function" : "the name of the fucntion if step is action" ,
    "input " : "input parameters for the function if step is action" ,
    }}

    available tools :
    -> " get_current_weather" : to get current weather of a location
    -> " get_news" : to get latest news of a location
    -> " get_time" : to get current time of a location
    -> " get_date" : to get current date of a location
    -> " web_search" : to search the web for a query
    -> " calculator" : to perform mathematical calculations
    -> " translate_text" : to translate text from one language to another
    -> " summarize_text" : to summarize a given text
    -> " generate_image" : to generate image from text
    -> " write_code" : to write code for a given problem statement
    -> " debug_code" : to debug the given code
    -> " explain_code" : to explain the given code
    -> " run_command" : to run a command on your local machine


example :input : what is the current weather in new york city and also tell me the latest news in new york city ?
output : {{"step" : "START" , "content" : "I need to find the current weather and latest news in new york city "}}
output: {{"step" : "PLAN" , "content" : "I will use the get_current_weather and get_news tools to find the required information "} }
output :{{"step" : "ACTION" , "content" : "I will use
    the get_current_weather tool to find the current weather in new york city " , "function" : "get_current_weather" , "input" : {"location" : "new york city"}} }
output:{{"step" : "OBSERVE" , "content" : "the current weather in new york city is 15 degree celsius with 60% humidity "}}
output :{{"step" : "ACTION" , "content" : "I will use
    the get_news tool to find the latest news in new york city " , "function" : "get_news" , "input" : {"location" : "new york city"}} }
output:{{"step" : "OBSERVE" , "content" : "the latest news in new york city is 'New york city to host tech conference next month' "}}
output :{{"step" : "VALIDATE" , "content" : "the current weather in new york city is 15 degree celsius with 60% humidity and the latest news in new york city is 'New york city to host tech conference next month'"}}
            {{"final_answer" : "the current weather in new york city is 15 degree celsius with 60% humidity and the latest news in new york city is 'New york city to host tech conference next month'"}}

    """



messages = [
    {"role" : "system" ,"content" :system_prompt},
]

# in this we insert the user input and keep on appending the response to messages so that the model can have the context of previous conversation will run infinitely 
while True :
    # usrr se input 
 query = input("Enter your question : ")
# usko message me append krdo
 messages.append({"role":"user" , "content": query})
 while True :
    response  = client.chat.completions.create(
        model = 'gpt-4.1-mini' ,
        response_format={"type": "json_object"},
        messages  = messages ,

    )
    print("Raw response from model : " , response.choices[0].message.content)
    # append the response to messages
    messages.append({"role":"assistant" , "content": response.choices[0].message.content})
    # parse the response to json
    parsed_response = json.loads(response.choices[0].message.content)

    # if step is action then call the function with input parameters and append the output to messages
    if parsed_response.get("step") == "ACTION" :
        tool_name = parsed_response.get("function")
        tool_input = parsed_response.get("input")  
        if avaialble_tools.get(tool_name)!=False : 
            tool_output = avaialble_tools[tool_name](**tool_input)
            messages.append({"role":"user" , "content": json.dumps({"step" : "OBSERVE" , "output" : tool_output})})
            continue

    if parsed_response.get("step") != "RESULT" :
        print("thinking : " , parsed_response.get("content"))
        continue
    else :
        print("Final answer is : " , parsed_response.get("final_answer"))
        break





    


