import unittest
import json
from app import app, InitializeDatabase
from flask_jwt_extended import create_access_token


class IntegrationTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.db_session = InitializeDatabase()
        self.username = "testuser"
        self.password = "testpassword"

    def tearDown(self):
        self.db_session.close()

    def register_user(self):
        return self.app.post('/api/register', data=json.dumps({
            "username": self.username,
            "password": self.password
        }), content_type='application/json')

    def login_user(self):
        return self.app.post('/api/login', data=json.dumps({
            "username": self.username,
            "password": self.password
        }), content_type='application/json')

    def test_register_user(self):
        response = self.register_user()
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully!", str(response.data))

    def test_login_user(self):
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, 201)
        self.assertIn("User logged in successfully!", str(response.data))
        token = json.loads(response.data)['token']
        self.assertIsNotNone(token)

    def test_add_task(self):
        self.register_user()
        login_response = self.login_user()
        token = json.loads(login_response.data)['token']

        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.post('/api/tasks', data=json.dumps({
            "title": "Test Task",
            "description": "This is a test task",
            "status": "TODO",
            "priority": "LOW",
            "due_date": "2024-08-20"
        }), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, 201)
        self.assertIn("Task created successfully!", str(response.data))

    def test_fetch_tasks(self):
        self.register_user()
        login_response = self.login_user()
        token = json.loads(login_response.data)['token']

        headers = {'Authorization': f'Bearer {token}'}
        self.app.post('/api/tasks', data=json.dumps({
            "title": "Test Task",
            "description": "This is a test task",
            "status": "TODO",
            "priority": "LOW",
            "due_date": "2024-08-20"
        }), content_type='application/json', headers=headers)

        response = self.app.get('/api/tasks', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Tasks retrieved successfully!", str(response.data))

    def test_update_task(self):
        self.register_user()
        login_response = self.login_user()
        token = json.loads(login_response.data)['token']

        headers = {'Authorization': f'Bearer {token}'}
        post_response = self.app.post('/api/tasks', data=json.dumps({
            "title": "Test Task",
            "description": "This is a test task",
            "status": "TODO",
            "priority": "LOW",
            "due_date": "2024-08-20"
        }), content_type='application/json', headers=headers)

        task_id = json.loads(post_response.data)['task']['id']
        response = self.app.put(f'/api/tasks/{task_id}', data=json.dumps({
            "title": "Updated Task",
            "description": "Updated description",
            "status": "IN_PROGRESS",
            "priority": "HIGH",
            "due_date": "2024-08-21"
        }), content_type='application/json', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Task updated successfully!", str(response.data))

    def test_delete_task(self):
        self.register_user()
        login_response = self.login_user()
        token = json.loads(login_response.data)['token']

        headers = {'Authorization': f'Bearer {token}'}
        post_response = self.app.post('/api/tasks', data=json.dumps({
            "title": "Test Task",
            "description": "This is a test task",
            "status": "TODO",
            "priority": "LOW",
            "due_date": "2024-08-20"
        }), content_type='application/json', headers=headers)

        task_id = json.loads(post_response.data)['task']['id']
        response = self.app.delete(f'/api/tasks/{task_id}', headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn("Task deleted successfully!", str(response.data))


if __name__ == '__main__':
    unittest.main()
