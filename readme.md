# Stock Price AI Assistant using pydantic-AI, Gradio, and Groq

inspired by:
https://www.youtube.com/watch?v=1lBpIbRafvI


https://github.com/pleabargain/pydantic-AI-finance-tool

https://www.gradio.app/

https://groq.com/

A web application built with Gradio that provides real-time stock price information using natural language queries.

## Features

- User-friendly web interface powered by Gradio
- Natural language processing for stock queries
- Real-time stock price data via yfinance
- Comprehensive logging system
- AI-powered responses using Groq LLM
- Clean and informative output format

## Requirements

- Python packages listed in requirements.txt:
  - pydantic-ai
  - yfinance
  - gradio
  - groq api key 

## Installation

1. Clone this repository or download the source code

2. Set up environment variables:
   - Create a GROQ_API_KEY environment variable with your Groq API key

3. Install the required packages:

For Windows:

this code assumes that the user has a groq api key and it's set in the environment variables.

if you have venv installed, you can create a new environment and install the packages with the following command:
uv pip install -r requirements.txt

or 

pip install -r requirements.txt   



# To run this Gradio app:
# Windows: python main.py
# Linux/Mac: python3 main.py
#
# The web interface will be available at:
# http://127.0.0.1:7860 (local)
# or if specified:
# http://0.0.0.0:7860 (network)