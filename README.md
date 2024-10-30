# Arukachan
A Raspberry Pi LLM project step by step build follow https://towardsdatascience.com/a-weekend-ai-project-running-speech-recognition-and-a-llama-2-gpt-on-a-raspberry-pi-5298d6edf812 which article written by Dmitrii Eliuseev.

To use this project. You need to:

Step 1. Navigate to Arukachan directory in Terminal.

Step 2. Use "python3 setup.py" then it gonna be:
    First. Use "python3 -m venv venv" to create a virtual environment. And "source venv/bin/activate" to activate the virtual environment;
    Second. Use "pip install -r requirements.txt" to install required libraries;
    Third. Use "huggingface-cli download TheBloke/Llama-2-7b-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False" to download the LLM model;
    Fourth. Use "python3 Arukachan_v1.0.py" to run Arukachan script;

Step 3. Use "deactivate" to deactivate the virtual environment.

Tips: When you add some new required libraries in your project. You should use "pip freeze > requirements.txt" to save your changes in virtual environment.
