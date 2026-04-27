import pytest
from app.validator import sql_validator

def test_valid_select_query():
    sql = "SELECT * FROM customers"
    is_valid, result = sql_validator.validate(sql)
    assert is_valid == True

def test_block_delete_query():
    sql = "DELETE FROM customers"
    is_valid, result = sql_validator.validate(sql)
    assert is_valid == False
    assert "DELETE" in result

def test_block_update_query():
    sql = "UPDATE customers SET name = 'test'"
    is_valid, result = sql_validator.validate(sql)
    assert is_valid == False
    assert "UPDATE" in result

def test_adds_limit():
    sql = "SELECT * FROM customers"
    is_valid, result = sql_validator.validate(sql)
    assert "LIMIT" in result.upper()
