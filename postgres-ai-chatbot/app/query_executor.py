from app.db import db_pool
from app.config import Config
import logging
import signal
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TimeoutException(Exception):
    pass

@contextmanager
def timeout(seconds):
    """Context manager for query timeout"""
    def timeout_handler(signum, frame):
        raise TimeoutException("Query timed out")

    # Set timeout handler
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(seconds)

    try:
        yield
    finally:
        signal.alarm(0)

class QueryExecutor:
    def __init__(self):
        self.max_rows = Config.MAX_ROWS_LIMIT
        self.timeout_seconds = Config.QUERY_TIMEOUT_SECONDS

    def execute_query(self, sql_query: str) -> tuple[list, list]:
        """
        Execute SQL query and return results
        Returns: (column_names, rows)
        """
        with db_pool.get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    with timeout(self.timeout_seconds):
                        logger.info(f"Executing query: {sql_query[:200]}")
                        cursor.execute(sql_query)

                        # Get column names
                        column_names = [desc[0] for desc in cursor.description] if cursor.description else []

                        # Fetch results
                        rows = cursor.fetchall()

                        logger.info(f"Query returned {len(rows)} rows")
                        return column_names, rows

                except TimeoutException as e:
                    logger.error(f"Query timeout after {self.timeout_seconds} seconds")
                    raise Exception(f"Query took too long (> {self.timeout_seconds} seconds)")
                except Exception as e:
                    logger.error(f"Query execution failed: {e}")
                    raise

    def format_results(self, column_names: list, rows: list) -> list:
        """Convert results to list of dictionaries"""
        if not column_names:
            return []

        result = []
        for row in rows:
            row_dict = {}
            for i, col_name in enumerate(column_names):
                row_dict[col_name] = row[i]
            result.append(row_dict)

        return result

# Global query executor instance
query_executor = QueryExecutor()
