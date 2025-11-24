# main.py
import os
import asyncio
from dotenv import load_dotenv # Import the dotenv loader

# Load environment variables from.env file immediately
load_dotenv()

from google.adk.agents import SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agents import (
    researcher, evaluator, drafter, 
    fact_checker, humanizer, seo_agent, publisher
)

# Define the Sequential Pipeline
newsroom_pipeline = SequentialAgent(
    name="TechNewsroom",
    description="A fully autonomous tech news generation pipeline.",
    sub_agents=[
        researcher,
        evaluator,
        drafter,
        fact_checker,
        humanizer,
        seo_agent,
        publisher
    ]
)

def run_newsroom(topic: str):
    print(f"--- Starting Newsroom for topic: {topic} ---")
    
    # Ensure output folder exists
    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"✓ Created '{output_folder}' folder")
    
    # Initialize Session Service
    session_service = InMemorySessionService()
    
    # Create session with initial state containing user_input for template variable injection
    session = asyncio.run(
        session_service.create_session(
            app_name="agents",
            user_id="user_admin",
            session_id="session_news_001",
            state={"user_input": topic}
        )
    )
    
    # Initialize Runner with In-Memory Session
    # Use "agents" as app_name to match what ADK detects from the agent's module path
    runner = Runner(
        app_name="agents",
        agent=newsroom_pipeline,
        session_service=session_service
    )
    
    # Create User Input Trigger
    user_input = types.Content(
        role="user",
        parts=[types.Part.from_text(text=topic)]
    )
    
    # Execute the Pipeline
    try:
        results = runner.run(
            user_id="user_admin", 
            session_id="session_news_001", 
            new_message=user_input
        )
        
        # Loop through the results and print the agent's responses
        for event in results:
            # Check if the event contains a text response from the model
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"\n[Agent Output]: {part.text}")
    except Exception as e:
        print(f"\n[ERROR] Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Check if output folder exists and list files
    if os.path.exists(output_folder):
        files = os.listdir(output_folder)
        if files:
            print(f"\n--- Pipeline Complete. Found {len(files)} file(s) in '{output_folder}' folder: ---")
            for file in files:
                filepath = os.path.join(output_folder, file)
                print(f"  ✓ {filepath}")
        else:
            print(f"\n--- Pipeline Complete. '{output_folder}' folder exists but is empty. ---")
    else:
        print(f"\n--- Pipeline Complete. '{output_folder}' folder was not created. The publisher agent may not have run successfully. ---")

if __name__ == "__main__":
    # Example Trigger
    run_newsroom("Meet the new Chinese vibe coding app that's so popular, one of its tools crashed")