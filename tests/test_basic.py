import os
import tempfile
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test if the index page loads correctly"""
    rv = client.get('/')
    assert rv.status_code == 200
    assert b"LLiMage MVP" in rv.data

def test_upload_no_file(client):
    """Test upload endpoint with no file"""
    rv = client.post('/process')
    assert rv.status_code == 400
    assert b"No file uploaded" in rv.data

def test_upload_empty_filename(client):
    """Test upload endpoint with empty filename"""
    rv = client.post('/process', data={
        'file': (None, '')
    })
    assert rv.status_code == 400
    assert b"No file selected" in rv.data
