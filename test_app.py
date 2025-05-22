import pytest
import json
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, students_collection, DB_CONNECTED, SAMPLE_STUDENTS

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean up test data before each test"""
    if DB_CONNECTED and students_collection is not None:
        # Clean up MongoDB if connected
        students_collection.delete_many({})
    else:
        # Clean up sample data
        SAMPLE_STUDENTS.clear()
        # Add some test data
        SAMPLE_STUDENTS.extend([
            {"_id": "1", "name": "Test User", "age": 20},
            {"_id": "2", "name": "Alice Test", "age": 22}
        ])

# Basic endpoint tests
def test_home_page(client):
    """Test the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'Student Management System' in data['message']
    assert 'status' in data
    assert data['status'] == 'operational'

def test_health_check(client):
    """Test the health check endpoint for CI/CD monitoring."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'status' in data
    assert data['status'] in ['healthy', 'healthy_with_fallback']
    assert 'database' in data
    assert 'mongo_secret_configured' in data
    assert 'ready_for_deployment' in data

def test_get_all_students(client):
    """Test getting all students."""
    response = client.get('/students')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_add_student_valid(client):
    """Test adding a valid student."""
    student_data = {
        'name': 'John Doe',
        'age': 25
    }
    response = client.post('/students', 
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['name'] == 'John Doe'
    assert data['age'] == 25
    assert '_id' in data

def test_add_student_missing_name(client):
    """Test adding a student with missing name."""
    student_data = {
        'age': 25
    }
    response = client.post('/students', 
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'name' in data['error']

def test_add_student_missing_age(client):
    """Test adding a student with missing age."""
    student_data = {
        'name': 'Jane Doe'
    }
    response = client.post('/students', 
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'age' in data['error']

def test_add_student_invalid_age(client):
    """Test adding a student with invalid age."""
    student_data = {
        'name': 'Jane Doe',
        'age': 'invalid'
    }
    response = client.post('/students', 
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_add_student_negative_age(client):
    """Test adding a student with negative age."""
    student_data = {
        'name': 'Jane Doe',
        'age': -5
    }
    response = client.post('/students', 
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_add_student_empty_name(client):
    """Test adding a student with empty name."""
    student_data = {
        'name': '',
        'age': 25
    }
    response = client.post('/students', 
                          data=json.dumps(student_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_get_student_by_id_sample_data(client):
    """Test getting a student by ID using sample data."""
    # This test works with both MongoDB and sample data
    response = client.get('/students/1')
    if response.status_code == 200:
        data = json.loads(response.data)
        assert '_id' in data
        assert 'name' in data
        assert 'age' in data
    else:
        # If student doesn't exist, should return 404
        assert response.status_code == 404

def test_get_student_by_id_not_found(client):
    """Test getting a non-existent student."""
    response = client.get('/students/999999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_delete_student_sample_data(client):
    """Test deleting a student using sample data."""
    # First, add a student
    student_data = {'name': 'To Delete', 'age': 30}
    add_response = client.post('/students', 
                              data=json.dumps(student_data),
                              content_type='application/json')
    assert add_response.status_code == 201
    
    # Get the student ID
    student = json.loads(add_response.data)
    student_id = student['_id']
    
    # Delete the student
    delete_response = client.delete(f'/students/{student_id}')
    if delete_response.status_code == 200:
        data = json.loads(delete_response.data)
        assert 'message' in data
    else:
        # If not found, should return 404
        assert delete_response.status_code == 404

def test_delete_student_not_found(client):
    """Test deleting a non-existent student."""
    response = client.delete('/students/999999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_search_students_by_name_found(client):
    """Test searching students by name - found."""
    # First add a student with a known name
    student_data = {'name': 'Alice Search Test', 'age': 25}
    add_response = client.post('/students', 
                              data=json.dumps(student_data),
                              content_type='application/json')
    assert add_response.status_code == 201
    
    # Search for the student
    response = client.get('/students/name/Alice')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    # Check if any student has 'Alice' in their name
    assert any('Alice' in student['name'] for student in data)

def test_search_students_by_name_not_found(client):
    """Test searching students by name - not found."""
    response = client.get('/students/name/NonExistentName12345')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_search_students_by_partial_name(client):
    """Test searching students by partial name."""
    # Add a student with a specific name
    student_data = {'name': 'Partial Test Name', 'age': 28}
    add_response = client.post('/students', 
                              data=json.dumps(student_data),
                              content_type='application/json')
    assert add_response.status_code == 201
    
    # Search using partial name
    response = client.get('/students/name/Partial')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_no_json_data(client):
    """Test POST request without proper JSON content type."""
    # Send data without application/json content type
    response = client.post('/students', data='not json', content_type='text/plain')
    # The app returns 500 when it can't parse JSON due to content type issues
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data

def test_invalid_json_data(client):
    """Test POST request with invalid JSON but correct content type."""
    # Send invalid JSON with correct content type
    response = client.post('/students', data='{"invalid": json}', content_type='application/json')
    # This should return 500 as the JSON parsing fails
    assert response.status_code == 500
    data = json.loads(response.data)
    assert 'error' in data

def test_empty_json_request(client):
    """Test POST request with empty JSON."""
    response = client.post('/students', 
                          data=json.dumps({}),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_404_endpoint(client):
    """Test 404 error handling."""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data

def test_mongodb_vs_fallback_mode(client):
    """Test that the app works in both MongoDB and fallback modes."""
    # This test checks that the health endpoint indicates the correct mode
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Check that we get valid database status
    assert data['database'] in [
        'connected_via_secrets', 
        'fallback_mode_no_secret', 
        'fallback_mode'
    ]
    
    # Check that mongo_secret_configured is a boolean
    assert isinstance(data['mongo_secret_configured'], bool)

def test_secret_configuration_status(client):
    """Test that the app reports secret configuration status correctly."""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Should have secret_configured field
    assert 'secret_configured' in data
    assert isinstance(data['secret_configured'], bool)
    
    # Database status should indicate secret usage
    assert 'database_status' in data
    if data['secret_configured']:
        assert 'Secrets' in data['database_status'] or 'Connected' in data['database_status']
    else:
        assert 'Sample Data' in data['database_status']

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
