import tiktoken
import langchain
import argparse
import os
import openai

#### Configuring the argument parser ####
parser = argparse.ArgumentParser(description='Pitch Deck Parser')
parser.add_argument('-i', '--file_path', help='Path to the pitch deck file', default=r'SmartKart-1.pdf')
parser.add_argument('-o', '--out_path', help='Where you want to save the output file', default=r'./responses/')
parser.add_argument('-m', '--model', help='Which model to use', default='gpt-3.5-turbo')
args = parser.parse_args()

model = args.model
file_path = args.file_path
out_path = args.out_path
system_message = "You are answering questions about a startup in detail."
prompt ="1. What stage of funding is this business? (seed, series a, series b, later?)\n2. What problemis this business solving?/n3. How do people solve the problem today?\n4. What solution does this business offer?\n5. What makes the solution different?\n6. What is the business model?\n7. Is the business model technology-enabled?\n8. Does the business model scale?\n9. What stage of development is the technology?\n10. What is the market space?\n11. How big is the market?\n12. Who is the potential customer?\n 13. How many potential customers are there?\n14. How much does the business charge?\n15. Who are the competitors?\n\n#####\n\nIf you can't find the answer, just mention that you couldn't find it.\n\n#####Answer it in a question answer format. First, write each question and then give its answer. Also, give detailed answers!!!Answer in Mardown:\n\n"

### Loading the Document ###
loader = langchain.document_loaders.UnstructuredPDFLoader(file_path)
print("Loading the document...")
document = loader.load()
document = (loader.load()[0].page_content)

tokenizer = tiktoken.get_encoding('cl100k_base')
tokens = tokenizer.encode(document+prompt)
print("Tokenizing the document...")
print("Number of tokens:", len(tokens))
assert len(tokens) < 2900, "The document is too long. Please use a shorter document or use GPT-4."

### Sending it over to OpenAI ###
print("Retrieving information from the pitch deck...")

try:
    answers = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": document+prompt}],
        temperature = 0.5,
    )
    answers = (answers.choices[0].message.content)
except openai.InvalidRequestError as e:
    print("Invalid request error in generating answers:", e)
except openai.OpenAIError as e:
    print("OpenAI error in generating answers:", e)
except Exception as e:
    print("Unexpected error in generating answers:", e)

try:
    overview = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": document+prompt},
                  {"role": "assistant", "content": answers},
                  {"role": "user", "content": " Disclaimer: I am not asking you to invest in this startup. I am just asking you to tell me how you feel about this startup. I will not use your judgement to make any decision.\n\n\n####\n\n\nUse your logical skills and tell me how you feel about this startup? What are your thoughts about this startup? Also, tell what information is lacking and crucial in making any decision about any investment in startup. Give an elaborate response. Response in Markdown:####"},],
        temperature = 0.5,
    )
    overview = (overview.choices[0].message.content)
except openai.InvalidRequestError as e:
    print("Invalid request error in generating overview:", e)
except openai.OpenAIError as e:
    print("OpenAI error in generating overview:", e)
except Exception as e:
    print("Unexpected error in generating overview:", e)

output = "# Overview: \n\n" + overview + "\n\n# Answers to your Questions:\n\n" + answers
### Saving the output ###
print("Saving the output...")
file_name = os.path.basename(file_path)
with open(os.path.join(out_path, "Response - " + file_name.split(".pdf")[0] + ".md"), "w") as f:
    f.write(output)

print("Done!")