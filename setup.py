import os
import subprocess
import sys

def run_command(command):
    """Run a command in the terminal."""
    process = subprocess.run(command, shell=True, check=True)
    return process

def main():
    # Step 1: Create a virtual environment
    print("Creating a virtual environment...")
    run_command("python3 -m venv venv")

    # Step 2: Activate the virtual environment
    # Note: Activation is a shell-specific command and won't work directly in subprocess.
    # Instead, we'll guide the user to activate it after the script finishes.
    print("Virtual environment created. Please activate it using:")
    print("source venv/bin/activate")
    
    # Step 3: Install required libraries
    print("Installing required libraries...")
    run_command("venv/bin/pip install -r requirements.txt")

    # Step 4: Import LLM
    #print("Importing the LLM...")
    #run_command("venv/bin/python ImportLLM.py")

    # Step 5: Run the Arukachan script
    print("Running the Arukachan script...")
    run_command("venv/bin/python Arukachan_v1.0.py")

if __name__ == "__main__":
    main()
