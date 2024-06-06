import unittest
from flask import json
from models import storage
from models.state import State
from api.v1.app import app


class TestStatesAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        storage.reload()

    def test_get_states(self):
        response = self.app.get('/api/v1/states/')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_get_state(self):
        state = State(name='California')
        storage.new(state)
        storage.save()
        response = self.app.get(f'/api/v1/states/{state.id}')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'California')

    def test_get_state_not_found(self):
        response = self.app.get('/api/v1/states/12345')
        self.assertEqual(response.status_code, 404)

    def test_delete_state(self):
        state = State(name='New York')
        storage.new(state)
        storage.save()
        response = self.app.delete(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), '{}')

    def test_delete_state_not_found(self):
        response = self.app.delete('/api/v1/states/12345')
        self.assertEqual(response.status_code, 404)

    def test_add_state(self):
        data = {'name': 'Texas'}
        response = self.app.post('/api/v1/states/', json=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'Texas')

    def test_add_state_missing_name(self):
        data = {}
        response = self.app.post('/api/v1/states/', json=data)
        self.assertEqual(response.status_code, 400)

    def test_update_state(self):
        state = State(name='Florida')
        storage.new(state)
        storage.save()
        data = {'name': 'Florida Updated'}
        response = self.app.put(f'/api/v1/states/{state.id}', json=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Florida Updated')

    def test_update_state_not_found(self):
        data = {'name': 'Florida Updated'}
        response = self.app.put('/api/v1/states/12345', json=data)
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
