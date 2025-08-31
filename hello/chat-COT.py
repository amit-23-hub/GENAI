
from openai import OpenAI
from dotenv import load_dotenv
client = OpenAI()
import json 

load_dotenv() 

# chain-of-thought prompting :  the model is encourage to think step by step before answering 
system_prompt = """
 
you are a very intelligent problem solver
you have to think step by step before answering any question
you should work on START , PLAN , ACTION  and OBSERVE  mode 

follow the steps in sequence that is "START -> PLAN -> ACTION -> OBSERVE ->VALIDATE  and repeat the process until you reach the final answer

Rules :
1. follow the strict json output as per schema .
2. always perform one step at a time and wait for next input from user.
3. always think step by step before answering any question
4. always follow the sequence of steps
5. always provide the final answer in the last step

output format :
    {{"step"} : "string" , "content" : "string"}}

example :
input : what is the sum of first 10 natural numbers ?
output : {{"step" : "START" , "content" : "I need to find the sum of first 10 natural numbers "}}
output: {{"step" : "PLAN" , "content" : "I will use the formula n(n+1)/2 to find the sum "} }
output :{{"step" : "ACTION" , "content" : "I will substitute n=10 in the formula "} }
output:{{"step" : "OBSERVE" , "content" : "the sum is
    10(10+1)/2 = 55 "}}
output :{{"step" : "VALIDATE" , "content" : "the sum of first 10 natural numbers is 55"}}
            {{"final_answer" : "55"}}


"""

# response  = client.chat.completions.create(
#     model = 'gpt-4.1-mini' ,
#     response_format={"type": "json_object"},
#     messages  = [
#         {"role" : "system" ,"content" :system_prompt},
    
#         ] ,

# ) 

# print(response.choices[0].message.content) 


# now i ahve to take output from terminal and pass it to next input of model

messages = [
    {"role" : "system" ,"content" :system_prompt},

]

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

# append the response to messages
    messages.append({"role":"assistant" , "content": response.choices[0].message.content})
        
    parsed_response = json.loads(response.choices[0].message.content) 
    
      # if step is validate then use gemini model to validate the operation
    if parsed_response.get("step") == "VALIDATE" :
            validation_prompt = f"""
            you are a very intelligent problem solver
            you have to validate the answer given by user 
            you have to check the answer step by step and if you find any mistake in any step then correct it and give the final answer
            if everything is correct then just confirm it 
    
            here is the solution given by user : 
            {parsed_response.get("content")}
    
            output format : 
            if everything is correct then just output 
            {{"get" : "final_answer" , "final_answer" : "string"}}
            
            if there is any mistake in any step then correct it and output 
            {{"get" : "not_final_answer" , "content" : "string"}}
    
            """
            
            validation_response  = client.chat.completions.create(
                model = 'gemini-1.5' ,
                messages  = [
                    {"role" : "system" ,"content" :validation_prompt},
                    {"role":"user" , "content": query}
                    ] ,
    
            ) 
    
            print("Validation response : " , validation_response.choices[0].message.content)
    
            # parse the validation response
            parsed_validation_response = json.loads(validation_response.choices[0].message.content) 
    
            # check if final answer is present in response
            if parsed_validation_response.get("get") != "final_answer" :
                print("thinking : " , parsed_validation_response.get("content"))
                messages.append({"role":"user" , "content": parsed_validation_response.get("content")})
                continue
            else :
                print("Final answer is : " , parsed_validation_response.get("final_answer"))
                break
      

    
