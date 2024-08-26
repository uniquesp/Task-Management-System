import unittest
from unittest.mock import patch, MagicMock
from internal.service.service import UserRegistration, UserLogin, CreateTask, FetchUserTasks, UpdateTask, DeleteTask
from internal.repository.repo import TaskRepository


class TestUserRegistration(unittest.TestCase):

    @patch('internal.repository.repo.UserRegistrationRepo')
    def test_user_registration_success(self, mock_user_registration_repo):
        mock_user_registration_repo.return_value = True
        database = MagicMock()
        username = "testuser"
        password = "testpassword"
        result = UserRegistration(database, username, password)
        self.assertTrue(result)

    @patch('internal.repository.repo.UserRegistrationRepo')
    def test_user_registration_fail(self, mock_user_registration_repo):
        mock_user_registration_repo.return_value = False
        database = MagicMock()
        username = "testuser"
        password = "testpassword"
        result = UserRegistration(database, username, password)
        self.assertFalse(result)


class TestUserLogin(unittest.TestCase):

    @patch('internal.repository.repo.UserLoginRepo')
    def test_user_login_success(self, mock_user_login_repo):
        mock_user = MagicMock()
        mock_user.password = b"hashedpassword"
        mock_user_login_repo.return_value = mock_user

        with patch('bcrypt.checkpw', return_value=True):
            database = MagicMock()
            username = "testuser"
            password = "testpassword"
            result = UserLogin(database, username, password)
            self.assertTrue(result)

    @patch('internal.repository.repo.UserLoginRepo')
    def test_user_login_fail(self, mock_user_login_repo):
        mock_user_login_repo.return_value = None
        database = MagicMock()
        username = "testuser"
        password = "testpassword"
        result = UserLogin(database, username, password)
        self.assertFalse(result)


class TestTaskManagement(unittest.TestCase):

    @patch.object(TaskRepository, 'create')
    def test_create_task(self, mock_create):
        mock_task = MagicMock()
        mock_create.return_value = mock_task
        database = MagicMock()
        title = "Test Task"
        description = "This is a test task"
        status = "TODO"
        priority = "LOW"
        due_date = "2024-08-20"
        user_id = 1
        result = CreateTask(database, title, description, status, priority, due_date, user_id)
        self.assertEqual(result, mock_task)

    @patch.object(TaskRepository, 'fetch_user_tasks')
    def test_fetch_user_tasks(self, mock_fetch_user_tasks):
        mock_tasks = [MagicMock(), MagicMock()]
        mock_fetch_user_tasks.return_value = mock_tasks
        database = MagicMock()
        user_id = 1
        tasks = FetchUserTasks(database, user_id)
        self.assertEqual(tasks, mock_fetch_user_tasks.return_value)

    @patch.object(TaskRepository, 'update')
    def test_update_task(self, mock_update):
        mock_task = MagicMock()
        mock_update.return_value = mock_task
        database = MagicMock()
        task_id = 1
        title = "Updated Task"
        description = "Updated description"
        status = "IN_PROGRESS"
        priority = "HIGH"
        due_date = "2024-08-21"
        user_id = 1
        result = UpdateTask(database, task_id, title, description, status, priority, due_date, user_id)
        self.assertEqual(result, mock_task)

    @patch.object(TaskRepository, 'delete')
    def test_delete_task(self, mock_delete):
        mock_task = MagicMock()
        mock_delete.return_value = mock_task
        database = MagicMock()
        task_id = 1
        user_id = 1
        result = DeleteTask(database, task_id, user_id)
        self.assertEqual(result, mock_task)


if __name__ == '__main__':
    unittest.main()
