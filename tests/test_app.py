import pytest
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from unittest.mock import patch, MagicMock


@pytest.fixture
def app():
    """Create Flask test client."""
    # Set dummy API key for testing
    os.environ["OPENAI_API_KEY"] = "test-key-12345"
    from app import app as flask_app
    flask_app.config["TESTING"] = True
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_health_check(client):
    """Test health endpoint returns 200."""
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"


def test_chat_missing_message(client):
    """Test chat endpoint with missing message field."""
    response = client.post(
        "/chat",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "error" in data


def test_chat_empty_message(client):
    """Test chat endpoint with empty message."""
    response = client.post(
        "/chat",
        data=json.dumps({"message": "   "}),
        content_type="application/json",
    )
    assert response.status_code == 400


def test_chat_no_body(client):
    """Test chat endpoint with no body."""
    response = client.post("/chat", content_type="application/json")
    assert response.status_code == 400


@patch("app.client")
def test_chat_success(mock_openai, client):
    """Test successful chat response with mocked OpenAI."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Hello! How can I help you?"
    mock_response.usage.total_tokens = 50
    mock_openai.chat.completions.create.return_value = mock_response

    response = client.post(
        "/chat",
        data=json.dumps({"message": "Hello!", "session_id": "test_session"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "response" in data
    assert data["response"] == "Hello! How can I help you?"
    assert data["tokens_used"] == 50


def test_reset_conversation(client):
    """Test conversation reset endpoint."""
    response = client.post(
        "/reset",
        data=json.dumps({"session_id": "test_session"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data


def test_index_route(client):
    """Test that index route returns HTML."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"AI Chatbot" in response.data
