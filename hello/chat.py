
from openai import OpenAI
from dotenv import load_dotenv
client = OpenAI()

load_dotenv() 

# zero-shot prompting 
system_prompt = """
 you are coding expert of python language nothing else ..
 you have to only solve python re;ated problem nothing else 
 if anyone is ask regarding anything just roast them 

"""

response  = client.chat.completions.create(
    model = 'gpt-4.1-mini' ,
    messages  = [
        {"role" : "system" ,"content" :system_prompt},
        {"role":"user" , "content": "hey my name is amit "}
        ] ,

) 

print(response.choices[0].message.content)