# Pitch Deck Parser

The Pitch Deck Parser is an advanced language model built on GPT-3.5 Turbo by OpenAI. It utilizes AI to answer in-depth questions about a startup, based on information from a pitch deck provided in a PDF file.

## Installation
First, ensure that you have the necessary dependencies installed. This includes tiktoken, langchain, argparse, os, and openai. You can install these using pip:

pip install tiktoken langchain argparse openai
## Usage
This program accepts a path to a PDF file of a pitch deck, a path to save the output, and the choice of model to use. The default model is 'gpt-3.5-turbo'. To use the program, run it with the -i, -o, and -m options.

For example:
python pitch_deck_parser.py -i 'SmartKart-1.pdf' -o './responses/' -m 'gpt-3.5-turbo'

### Program Description
The program operates in the following steps:

Parses the input arguments to retrieve the paths and model to use.
Loads the provided PDF document.
Tokenizes the loaded document and a set prompt.
Sends the tokenized document and prompt to the OpenAI API to generate a set of answers to the questions in the prompt.
Retrieves a further detailed overview from the OpenAI API based on the provided document, prompt, and generated answers.
Compiles the answers and overview into a Markdown file.
Saves the output Markdown file in the specified output path.
The program will print progress updates to the console during its operation.

## Error Handling
The program contains exception handling for errors that can occur during the process of generating the answers and overview. This includes handling for invalid requests to the OpenAI API, other OpenAI API errors, and other unexpected errors.

## Output
The output is a Markdown file saved in the specified output path. It includes an overview of the startup based on the information from the pitch deck, as well as answers to in-depth questions about the startup.

### NOTE: This program does not provide investment advice or make any investment decisions. It simply generates information based on the provided pitch deck.