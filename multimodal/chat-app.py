import os
from urllib.request import urlopen, Request
import base64

# Add references
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import (
   SystemMessage,
   UserMessage,
   TextContentItem,
   ImageContentItem,
   ImageUrl,
   AudioContentItem,
   InputAudio,
   AudioContentFormat,
)

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_connection = os.getenv("PROJECT_CONNECTION")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")
        
        # Initialize the project client

        project_client = AIProjectClient.from_connection_string(
            conn_str=project_connection,
            credential=DefaultAzureCredential())
                

        ## Get a chat client
        chat_client = project_client.inference.get_chat_completions_client(model=model_deployment)

        system_message = "You are an AI assistent in a grocery store that sells fruit."
         

        # Loop until the user types 'quit'
        while True:
            input_text = input("Choose a prompt type (or type 'quit' to exit):\n-1: Text\n-2: Image\n-3: Audio\n")
            if input_text.lower() == "quit":
                break
            elif input_text == "1":
                prompt = input("Enter the prompt: ")
                if len(prompt) == 0:
                    print("Please enter a prompt.")
                else:
                    print("Getting a response to your prompt...")

                    # Get a response to text input
                    response = chat_client.complete(
                    messages=[
                        SystemMessage(system_message),
                        UserMessage(content=[TextContentItem(text= prompt)])
                    ])
                    print(response.choices[0].message.content)

            elif input_text == "2":
                prompt = input("Enter the prompt to accompany the image: ")
                if len(prompt) == 0:
                    print("Please enter a prompt.")
                else:
                    print("Getting a response to your prompt...")

                    # Get a response to image input
                    image_url = "https://github.com/microsoftlearning/mslearn-ai-studio/raw/refs/heads/main/labfiles/multimodal/orange.jpg"
                    image_format = "jpeg"
                    request = Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
                    image_data = base64.b64encode(urlopen(request).read()).decode("utf-8")
                    data_url = f"data:image/{image_format};base64,{image_data}"

                    response = chat_client.complete(
                    messages=[
                        SystemMessage(system_message),
                        UserMessage(content=[
                            TextContentItem(text=prompt),
                            ImageContentItem(image_url=ImageUrl(url=data_url))
                        ]),
                    ]
                    )
                    print(response.choices[0].message.content)

            elif input_text == "3":
                prompt = input("Enter the prompt to accompany an audio recording of 'Me gustaría comprar 2 manzanas.': ")
                if len(prompt) == 0:
                    print("Please enter a prompt.")
                else:
                    print("Getting a response to your prompt...")

                    # Get a response to audio input
                    # Get a response to audio input
                    file_path="https://github.com/microsoftlearning/mslearn-ai-studio/raw/refs/heads/main/labfiles/multimodal/manzanas.mp3"
                    response = chat_client.complete(
                        messages=[
                            SystemMessage(system_message),
                            UserMessage(
                                [
                                    TextContentItem(text=prompt),
                                    {
                                        "type": "audio_url",
                                        "audio_url": {"url": file_path}
                                    }
                                ]
                            )
                        ]
                    )
                    print(response.choices[0].message.content)

            else:
                print("Please enter a valid value")
                continue


    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()