# Text-to-SQL
**Text to SQL commands using Llama 3**

This project integrates advanced language models and data querying technologies to streamline the process of querying and summarizing data from local databases. The system utilizes the Groq API and DuckDB to handle user inquiries and generate relevant SQL queries dynamically.

**Key Components:**

1. **User Interaction:** The tool allows users to ask questions about data in CSV files (e.g., 'employees.csv' and 'purchases.csv').

2. **Dynamic SQL Generation:** Using a language model (Llama3 70b), the system generates SQL queries based on user questions. The queries are then executed against an in-memory DuckDB instance to retrieve the relevant data.

3. **Data Summarization:** After fetching the data, the system generates a summarization prompt to further process the results. The Groq API is used to provide a concise summary of the data as it relates to the user's original question.

4. **Function Calling:** Implemented function calling to interact with the DuckDB and Groq API, ensuring smooth execution of queries and retrieval of responses.

5. **Response Handling:** The project includes error handling and formatting to display SQL queries and data results clearly. If SQL generation fails, appropriate error messages are provided.

This tool enhances the ability to extract, analyze, and summarize data efficiently, leveraging AI to facilitate insightful data interactions.


