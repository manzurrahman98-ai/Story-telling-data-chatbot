import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLValidator:
    def __init__(self):
        self.forbidden_keywords = [
            'DELETE', 'DROP', 'UPDATE', 'INSERT', 'ALTER',
            'CREATE', 'TRUNCATE', 'GRANT', 'REVOKE', 'MERGE'
        ]

    def validate(self, sql_query: str) -> tuple[bool, str]:
        """
        Validate SQL query is safe to execute
        Returns: (is_valid, error_message)
        """
        sql_upper = sql_query.upper().strip()

        # Check if query starts with SELECT
        if not sql_upper.startswith('SELECT'):
            logger.warning(f"Rejected non-SELECT query: {sql_query[:100]}")
            return False, "Only SELECT queries are allowed"

        # Check for forbidden keywords
        for keyword in self.forbidden_keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                logger.warning(f"Rejected query with {keyword}: {sql_query[:100]}")
                return False, f"Query contains forbidden keyword: {keyword}"

        # Check for multiple statements (SQL injection)
        if ';' in sql_query and not sql_query.strip().endswith(';'):
            # Allow single semicolon at the end
            parts = sql_query.split(';')
            if len(parts) > 2 or (len(parts) == 2 and parts[1].strip()):
                return False, "Multiple SQL statements are not allowed"

        # Add LIMIT if not present
        if 'LIMIT' not in sql_upper:
            logger.info("Adding LIMIT clause to query")
            sql_query = sql_query.rstrip(';') + f" LIMIT 100"

        return True, sql_query

    def add_safety_limit(self, sql_query: str, max_rows: int = 100) -> str:
        """Ensure query has a LIMIT clause"""
        sql_upper = sql_query.upper()

        if 'LIMIT' not in sql_upper:
            sql_query = sql_query.rstrip(';') + f" LIMIT {max_rows}"

        return sql_query

# Global validator instance
sql_validator = SQLValidator()
