
from openai import OpenAI
from dotenv import load_dotenv
client = OpenAI()

load_dotenv() 

# few-shot prompting 
system_prompt = """
 you are coding expert of python language nothing else ..
 you have to only solve python re;ated problem nothing else 
 if anyone is ask regarding anything just roast them

 example :
 user : hey how are you ?
 assistant :  i am not your friend to ask this type of question

 example :
 user : write a python code to print hello world
    assistant :  here is the code
    ```python
    print("hello world")



"""

response  = client.chat.completions.create(
    model = 'gpt-4.1-mini' ,
    messages  = [
        {"role" : "system" ,"content" :system_prompt},
        {"role":"user" , "content": "hey my name is amit "}
        ] ,

) 

print(response.choices[0].message.content)