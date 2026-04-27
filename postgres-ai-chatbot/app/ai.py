# from openai import OpenAI
# from app.config import Config
# from app.schemas import SCHEMA_DESCRIPTION
# import logging
# from tenacity import retry, stop_after_attempt, wait_exponential

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class AIEngine:
#     def __init__(self):
#         self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
#         self.model = Config.OPENAI_MODEL

#     @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
#     def generate_sql(self, user_question: str) -> str:
#         """Convert natural language to SQL query"""

#         system_prompt = f"""
# You are a PostgreSQL expert. Convert user questions into SQL queries.

# Database Schema:
# {SCHEMA_DESCRIPTION}

# Rules:
# - ONLY generate SELECT queries (no INSERT, UPDATE, DELETE, DROP, ALTER)
# - Use proper JOINs when accessing multiple tables
# - NEVER hallucinate column names - only use columns from schema
# - Add LIMIT clause for queries that might return many rows
# - Use COALESCE for NULL handling when appropriate
# - Format SQL with proper indentation
# - Return ONLY the SQL query, no explanations

# Examples:
# User: "Show me all customers"
# SQL: SELECT id, name, email FROM customers ORDER BY created_at DESC LIMIT 100;

# User: "Top 5 products by sales"
# SQL: SELECT p.name, SUM(oi.quantity) as total_units_sold, SUM(oi.quantity * oi.price) as total_revenue FROM order_items oi JOIN products p ON oi.product_id = p.id GROUP BY p.id, p.name ORDER BY total_revenue DESC LIMIT 5;
# """

#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": user_question}
#                 ],
#                 temperature=0.1,
#                 max_tokens=500
#             )

#             sql_query = response.choices[0].message.content.strip()
#             # Remove markdown code blocks if present
#             sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
#             logger.info(f"Generated SQL: {sql_query}")
#             return sql_query

#         except Exception as e:
#             logger.error(f"Error generating SQL: {e}")
#             raise

#     @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
#     def format_response(self, user_question: str, sql_query: str, query_result: list) -> str:
#         """Format SQL results into natural language response"""

#         system_prompt = f"""
# You are a helpful data analyst. Convert the SQL query results into a natural, conversational response.

# User Question: {user_question}
# SQL Query Used: {sql_query}
# Query Results: {query_result}

# Instructions:
# - Explain the results in simple, clear language
# - If there are no results, explain that no data matches the query
# - If results are large, summarize key insights
# - Highlight important numbers and trends
# - Keep response concise but informative
# - Be helpful and conversational
# """

#         try:
#             response = self.client.chat.completions.create(
#                 model=self.model,
#                 messages=[
#                     {"role": "system", "content": system_prompt},
#                     {"role": "user", "content": f"Please explain these results: {query_result}"}
#                 ],
#                 temperature=0.3,
#                 max_tokens=300
#             )

#             formatted_response = response.choices[0].message.content.strip()
#             logger.info(f"Formatted response: {formatted_response}")
#             return formatted_response

#         except Exception as e:
#             logger.error(f"Error formatting response: {e}")
#             return f"Query executed successfully. Found {len(query_result)} results."

# # Global AI engine instance
# ai_engine = AIEngine()



import logging
from google import genai  # The modern 2026 SDK
from app.config import Config
from app.schemas import SCHEMA_DESCRIPTION
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIEngine:
    def __init__(self):
        # The new SDK uses a Client object
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = Config.GEMINI_MODEL

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_sql(self, user_question: str) -> str:
        """Convert natural language to SQL query using Gemini 3"""

        system_prompt = f"""
You are a PostgreSQL expert. Convert user questions into SQL queries.

Database Schema:
{SCHEMA_DESCRIPTION}

Rules:
- ONLY generate SELECT queries (no INSERT, UPDATE, DELETE, DROP, ALTER)
- Use proper JOINs when accessing multiple tables
- NEVER hallucinate column names - only use columns from schema
- Add LIMIT clause for queries that might return many rows
- Return ONLY the SQL query, no explanations or markdown blocks
"""

        try:
            # New syntax: models.generate_content
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=f"{system_prompt}\n\nUser Question: {user_question}"
            )

            # Use .text to get the string result
            sql_query = response.text.strip()

            # Thoroughly strip markdown backticks
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

            logger.info(f"Generated SQL: {sql_query}")
            return sql_query

        except Exception as e:
            logger.error(f"Error generating SQL with Gemini: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def format_response(self, user_question: str, sql_query: str, query_result: list) -> str:
        """Format SQL results into natural language response"""

        prompt = f"""
Convert the following data into a natural, conversational response.
User Question: {user_question}
SQL Query: {sql_query}
Results: {query_result}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            formatted_response = response.text.strip()
            logger.info(f"Formatted response: {formatted_response}")
            return formatted_response

        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return f"Found {len(query_result)} results for your request."

# Global AI engine instance
ai_engine = AIEngine()
