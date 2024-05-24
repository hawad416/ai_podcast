from langchain_openai import ChatOpenAI
from llama_index.core import Prompt, Document, VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import openai
from llama_parse import LlamaParse
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.llms.openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import os
import json
import streamlit as st

st.set_page_config(layout="wide")
st.sidebar.header("🍭 p o d s 🍭")
st.sidebar.page_link("main.py", label="🎙️ Create New Podcast")
st.sidebar.page_link("./pages/another.py", label="▶️ My Episodes")



# Initialize OpenAI language model with specific parameters
llm = OpenAI(temperature=0.1, model="gpt-4-0125-preview")
client = OpenAI(llm="gpt-4-0125-preview")

# get the uploaded essay
parser = LlamaParse(
        api_key=os.environ.get("LLAMA_PARSER_KEY"),
        result_type="markdown",
        verbose=True,
)
file_extractor = {".pdf": parser}
essay = SimpleDirectoryReader(input_files=["sammvl.pdf"], file_extractor=file_extractor).load_data()

print(essay)

complete_doc =""
for doc in essay:
    complete_doc+=doc.text
        
print(complete_doc)

st.title("🍭 Hawa's Creative Studio 🍭")
st.subheader("podcast generator🎙️")

#st.image("st.png", width=200)

    # User input: Name
name = st.text_input("Name:")

        # User input: Podcast title
podcast_title = st.text_input("Podcast Title Name:")

        # User input: Episode title
episode_title = st.text_input("Episode Title Name:")

# Article content
article = st.text_area("Paste your writing here!")


        # User input: Call to action email or contact info
call_to_action = st.text_input("Call to Action Email / Contact Info:")




def generate_podcast(name, podcast_title, episode_title, call_to_action):
    # Your function to generate the podcast
    # You can use the provided information to create the podcast
    # For example, generate an audio file and display a success message

    # Placeholder example for generating a podcast
    st.success("Podcast generated successfully!")

    script = generate_script(article, name, podcast_title, episode_title, call_to_action)
    cleaned_script = clean_script(script)
    create_audio_podcast(cleaned_script)
    # Define the input directory and output file
    input_directory = 'clips'  # Specify the path to the directory containing MP3 files
    output_file = 'final_podcast.mp3'  # Specify the path and name for the output MP3 file

    # Combine the MP3 files and save the result
    combine_mp3_files(input_directory, output_file)
    st.audio(output_file)



def generate_script(essay, name, podcast_title, episode_title, call_to_action) -> str:
        """
        Generates Podcast Scipt.
        """
        print(podcast_title)
        # Convert the list of dictionaries (JSON flight data) to a single string for input
        input_data = essay
        name = name
        podcast_title = podcast_title
        episode_title=episode_title
        call_to_action=call_to_action
        
        system_prompt = (
             f"""

             Task: Your task is to develop a 5 minute script for a podcast episode based on the given essay. 
             The podcast only has one host named {name}.
             The podcast name is  {podcast_title}
             The name of the episode is {episode_title}
       
            Follow the instructions below:

            Input:

            Essay: Analyze the essay provided, focusing on its key themes, arguments, evidence, and conclusions.
            Podcast Details: Create a script suitable for a podcast episode that is engaging, informative, and suitable for a general audience.
            Requirements:

            Introduction: Begin with a compelling introduction that hooks the listeners and provides an overview of the episode's content.
            Main Content: Summarize the main points from the essay, breaking them down into segments that flow logically and cover the major themes and arguments. Provide context and examples where necessary.
            Additional Insights: Add any relevant additional insights, anecdotes, or examples to make the content more engaging and relatable to the audience.
            Dialogue and Transitions: Include smooth transitions between segments and points. Utilize natural language and conversational style to maintain the listener’s interest.
            Conclusion: Summarize the key takeaways and end with a thought-provoking statement or question to encourage further reflection or discussion.
            Call to Action: If applicable, provide a call to action for the listeners at the end of the episode. Here is the contact: {call_to_action}
            """ )
            
        messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_data}
            ]
            # Create a completion request to OpenAI
        completion = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
            )
        preferences = completion.choices[0].message.content
        print(preferences)
            
        return preferences

def clean_script(script):
      
        # Convert the list of dictionaries (JSON flight data) to a single string for input
        input_data = script
        
        system_prompt = (
             """ take the given script and remove anything indicating its a script such as 
             - Anything in brackets : []
             - Indication of the person speaking ex Host1: or Hawa: 
             Return the cleaned script with just the talking points. 
             """
        )
            
        messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": script}
            ]
            # Create a completion request to OpenAI
        completion = openai.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages,
            )
        preferences = completion.choices[0].message.content
        print(preferences)
            
        return preferences

# tts = gTTS(text=cleaned_script, lang='en')
# tts.save('ogpodcast.mp3')


from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

def create_audio_podcast(cleaned_script):

    SPEAK_OPTIONS = {"text": cleaned_script}
    filename = "hawa_podcast.mp3"

    import requests

    from more_itertools import sliced
    text_chunks = list(sliced(cleaned_script, 2000))

   # aura-arcas-en

   # aura-luna-en

    url = "https://api.deepgram.com/v1/speak?model=aura-arcas-en"
    headers = {
        "Authorization": "Token 0c6380718c35414124f53ac15e04b40939eae806",
        "Content-Type": "application/json"
    }

    for i, chunk in enumerate(text_chunks):
                print(f"\nProcessing chunk {i + 1}...{chunk}\n")
                filename = f"clips/podcast_chunk_{i + 1}.mp3"

            # SPEAK_OPTIONS = {"text": chunk}
            
                payload = {
                    "text": chunk
                }

                response = requests.post(url, headers=headers, json=payload)

                if response.status_code == 200:
                    with open(filename, "wb") as f:
                        f.write(response.content)
                    print("File saved successfully.")
                else:
                    print(f"Error: {response.status_code} - {response.text}")


from pydub import AudioSegment

def combine_mp3_files(input_directory, output_file):
    """
    Combine all MP3 files in the specified input directory and save as a single MP3 file.
    
    Parameters:
    - input_directory (str): The directory containing MP3 files to combine.
    - output_file (str): The file path for the combined output MP3 file.
    """
    # Initialize an empty AudioSegment for combining
    combined_audio = AudioSegment.empty()
    
    # Get a list of MP3 files in the input directory
    mp3_files = [f for f in os.listdir(input_directory) if f.endswith('.mp3')]
    
    # Sort the MP3 files if necessary (e.g., based on file name)
    mp3_files.sort()
    
    # Iterate over the sorted list of MP3 files
    for mp3_file in mp3_files:
        # Load each MP3 file using Pydub
        audio_segment = AudioSegment.from_file(os.path.join(input_directory, mp3_file))
        
        # Append the current audio segment to the combined audio
        combined_audio += audio_segment
        
        print(f"Appended {mp3_file}")
    
    # Export the combined audio as a new MP3 file
    combined_audio.export(output_file, format='mp3')
    print(f"Combined MP3 file saved as {output_file}")





    # If the user has filled out all the inputs, show the information
if st.button("Generate Podcast"):
        if name and podcast_title and episode_title and call_to_action:
            # Show the user the information they entered
            st.subheader("Information Entered:")
            st.write(f"Name: {name}")
            st.write(f"Podcast Title: {podcast_title}")
            st.write(f"Episode Title: {episode_title}")
            st.write(f"Call to Action Email / Contact Info: {call_to_action}")

              # Display a loading spinner while generating the podcast
            with st.spinner("Generating podcast..."):
                # Call your function to generate the podcast based on the information provided
                # Replace `generate_podcast` with your function that handles the podcast creation
                generate_podcast(name, podcast_title, episode_title, call_to_action)

            # Inform the user that the podcast was generated successfully
            st.success("Podcast generated successfully!")

        else:
            st.warning("Please fill out all fields before generating the podcast.")


st.subheader("made with <3 by pods | hawa")
 