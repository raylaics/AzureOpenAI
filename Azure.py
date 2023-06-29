import os
import openai
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

openai.api_key = ""
openai.api_base = "changed"
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
deployment_name="chatgpt"

index_name = "azureblob-index"
endpoint = 'https://hcmschatbot.search.windows.net/'
key = ''

credential = AzureKeyCredential(key)
client = SearchClient(endpoint=endpoint,
                      index_name=index_name,
                      credential=credential)
                      
system_message = {"role": "system", "content": "You are a kindergarten teacher. Please answer for kids."}
max_response_tokens = 500
                      
print("\n"+f"== HCMS ChatBot ==")
user_input = ""
while user_input != 'quit':
    user_input = input("") 
    if user_input != 'quit':    
        results = client.search(search_text=user_input)
        openai_input = ""
        i=1
        for result in results:
            if i<=2:
                openai_input += result["content"]
                i += i
        
        openai_input = "Context information is below. \n---------------------\n" \
        +openai_input \
        +"---------------------\nGiven the context information and not prior knowledge, answer the question: " \
        +user_input
        
        conversation=[]
        conversation.append(system_message)        
        conversation.append({"role": "user", "content": openai_input})
            
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages = conversation,
            temperature=1,
            max_tokens=max_response_tokens,
        )

        print("\n" + response['choices'][0]['message']['content'])
        print("\n"+f"== HCMS ChatBot ==")
print(f"Bye!")
