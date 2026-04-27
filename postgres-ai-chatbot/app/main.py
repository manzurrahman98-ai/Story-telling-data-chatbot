from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from app.db import db_pool
from app.ai import ai_engine
from app.validator import sql_validator
from app.query_executor import query_executor
from app.config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="PostgreSQL AI Chatbot API",
    description="Natural language to SQL chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    question: str
    sql_query: str
    results: list
    explanation: str
    row_count: int
    execution_time_ms: float
    timestamp: str

class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: str

# Startup and Shutdown Events
@app.on_event("startup")
async def startup_event():
    """Initialize database connection pool on startup"""
    logger.info("Starting up API...")
    db_pool.create_pool()
    logger.info("API startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    logger.info("Shutting down API...")
    db_pool.close_all_connections()
    logger.info("API shutdown complete")

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "PostgreSQL AI Chatbot API",
        "version": "1.0.0",
        "endpoints": ["/chat", "/health", "/docs"]
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    db_status = "connected"
    try:
        with db_pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"

    return HealthResponse(
        status="healthy" if db_status == "connected" else "unhealthy",
        database=db_status,
        timestamp=datetime.now().isoformat()
    )

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Process natural language question and return SQL query results with explanation

    Flow:
    1. Generate SQL from question using AI
    2. Validate SQL is safe (SELECT only)
    3. Execute query on PostgreSQL
    4. Format results using AI
    5. Return response
    """
    import time

    start_time = time.time()

    try:
        # Step 1: Generate SQL from question
        logger.info(f"Processing question: {request.question}")
        sql_query = ai_engine.generate_sql(request.question)

        # Step 2: Validate SQL
        is_valid, result = sql_validator.validate(sql_query)
        if not is_valid:
            raise HTTPException(status_code=400, detail=result)
        sql_query = result  # This may have LIMIT added

        # Step 3: Execute query
        column_names, rows = query_executor.execute_query(sql_query)
        formatted_results = query_executor.format_results(column_names, rows)

        # Step 4: Format response using AI
        explanation = ai_engine.format_response(
            request.question,
            sql_query,
            formatted_results[:10]  # Send first 10 results for context
        )

        # Step 5: Calculate metrics
        execution_time_ms = (time.time() - start_time) * 1000

        return ChatResponse(
            question=request.question,
            sql_query=sql_query,
            results=formatted_results,
            explanation=explanation,
            row_count=len(formatted_results),
            execution_time_ms=round(execution_time_ms, 2),
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=Config.API_PORT,
        reload=True
    )
