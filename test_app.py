import pytest
import requests

base_url = 'http://localhost:8083/service/library/'

# Test cases for authors
def test_create_author():
    payload = {
        'name': 'Test Author',
        'bio': 'Test bio',
        'birth_date': '2000-01-01'
    }
    response = requests.post(base_url + 'authors', json=payload)
    assert response.status_code == 200
    assert response.json()['message'] == 'Success'

def test_get_all_authors():
    response = requests.get(base_url + 'authors')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_author():
    response = requests.get(base_url + 'authors/6')
    assert response.status_code == 200
    assert 'id' in response.json()

def test_update_author():
    payload = {
        'id': 6,
        'name': 'Updated Test Author',
        'bio': 'Updated test bio',
        'birth_date': '2000-01-01'
    }
    response = requests.put(base_url + 'authors/update', json=payload)
    assert response.status_code == 200
    assert response.json()['message'] == 'Success'

def test_delete_author():
    response = requests.delete(base_url + 'authors/delete/6')
    assert response.status_code == 200
    assert response.json()['message'] == 'Success'

# Test cases for books
def test_create_book():
    payload = {
        'title': 'Test Book',
        'description': 'Test description',
        'publish_date': '2023-01-01',
        'author_id': 1
    }
    response = requests.post(base_url + 'books', json=payload)
    assert response.status_code == 200
    assert response.json()['message'] == 'Success'

def test_get_all_books():
    response = requests.get(base_url + 'books')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_book():
    response = requests.get(base_url + 'books/1')
    assert response.status_code == 200
    assert 'id' in response.json()

def test_update_book():
    payload = {
        'id': 11,
        'title': 'Updated Test Book',
        'description': 'Updated test description',
        'publish_date': '2023-01-01',
        'author_id': 1
    }
    response = requests.put(base_url + 'books/update', json=payload)
    assert response.status_code == 200
    assert response.json()['message'] == 'Success'

def test_delete_book():
    response = requests.delete(base_url + 'books/delete/11')
    assert response.status_code == 200
    assert response.json()['message'] == 'Success'

# Run the tests
if __name__ == '__main__':
    pytest.main()
