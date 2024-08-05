import os
from groq import Groq
import json
import duckdb
import sqlparse
import numpy as np
import pandas as pd

def chat_with_groq(client, prompt, model, response_format):
  completion = client.chat.completions.create(
  model=model,
  messages=[
      {
          "role": "user",
          "content": prompt
      }
  ],
  response_format=response_format
  )

  return completion.choices[0].message.content

def execute_duckdb_query(query):
  original_cwd = os.getcwd()
  os.chdir('data')

  try:
      conn = duckdb.connect(database=':memory:', read_only=False)
      query_result = conn.execute(query).fetchdf().reset_index(drop=True)
  finally:
      os.chdir(original_cwd)

  return query_result

def get_summarization(client, user_question, df, model):
    """
    This function generates a summarization prompt based on the user's question and the resulting data. 
    It then sends this summarization prompt to the Groq API and retrieves the AI's response.

    Parameters:
    client (Groqcloud): The Groq API client.
    user_question (str): The user's question.
    df (DataFrame): The DataFrame resulting from the SQL query.
    model (str): The AI model to use for the response.

    Returns:
    str: The content of the AI's response to the summarization prompt.
    """
    prompt = '''
      A user asked the following question pertaining to local database tables:
    
      {user_question}
    
      To answer the question, a dataframe was returned:
    
      Dataframe:
      {df}

    In a few sentences, summarize the data in the table as it pertains to the original user question. Avoid qualifiers like "based on the data" and do not comment on the structure or metadata of the table itself
  '''.format(user_question = user_question, df = df)

    # Response format is set to 'None'
    return chat_with_groq(client,prompt,model,None)

# Use the Llama3 70b model
model = "llama3-70b-8192"

# Get the Groq API key and create a Groq client
groq_api_key = ""
client = Groq(
  api_key=groq_api_key
)

print("Welcome to the DuckDB Query Generator!")
print("You can ask questions about the data in the 'employees.csv' and 'purchases.csv' files.")

# Load the base prompt
with open('prompts/base_prompt.txt', 'r') as file:
  base_prompt = file.read()

while True:
  # Get the user's question
  user_question = input("Ask a question: ")

  if user_question:
      # Generate the full prompt for the AI
      full_prompt = base_prompt.format(user_question=user_question)

      # Get the AI's response. Call with '{"type": "json_object"}' to use JSON mode
      llm_response = chat_with_groq(client, full_prompt, model, {"type": "json_object"})

      result_json = json.loads(llm_response)
      if 'sql' in result_json:
          sql_query = result_json['sql']
          results_df = execute_duckdb_query(sql_query)

          formatted_sql_query = sqlparse.format(sql_query, reindent=True, keyword_case='upper')

          print("```sql\n" + formatted_sql_query + "\n```")
          print(results_df.to_markdown(index=False))

          summarization = get_summarization(client,user_question,results_df,model)
          print(summarization)
      elif 'error' in result_json:
          print("ERROR:", 'Could not generate valid SQL for this question')
          print(result_json['error'])



