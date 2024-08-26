
# 📝 Task Management System

This project is a Flask-based API that provides user authentication using JSON Web Tokens (JWT). The API allows users to register and log in, returning a JWT token upon successful authentication. The token can be used to access protected endpoints in the application.

## ✨ Features

- 🛡️ **User registration with validation**
- 🔐 **User login with JWT token generation**
- 🔒 **Protected endpoints accessible only with a valid JWT**
- ⚠️ **Error handling and response formatting**

## 🛠️ Technologies Used

- 🐍 **Python 3**
- 🌐 **Flask**
- 🔑 **Flask-JWT-Extended**
- 🗃️ **SQLAlchemy** (for ORM)
- 🗄️ **SQLite** (default database)

## 💡 Assumptions and Approach

### Assumptions
- The user must provide a valid username and password for registration. The username must be at least 3 characters long, and the password must be at least 6 characters long.
- The registration and login endpoints are the only public endpoints; all others require a valid JWT token in the request header.
- The SQLite database is used for simplicity, but this can be replaced with any other relational database.

### Approach
- **Registration Validation**: The registration payload is validated to ensure that the username and password meet the specified criteria. The validation is done using the `ValidateRegistrationPayload` function, which checks for the presence of both username and password and ensures they meet the length requirements.
- **JWT Authentication**: Upon successful login, a JWT token is generated and returned to the client. This token must be included in the Authorization header of subsequent requests to access protected endpoints.
- **Token Protection**: Endpoints that require authentication are protected using the `@jwt_required()` decorator from `Flask-JWT-Extended`. This ensures that only requests with a valid JWT token can access these endpoints.

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   ```

2. Navigate to the project directory:

   ```bash
   cd your-repo-name
   ```

3. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Set up the environment variables:

   Create a `.env` file in the root of the project and add the following variables:

   ```bash
   SECRET_KEY=your_secret_key
   ```

6. Initialize the database:

   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

7. Run the application:

   ```bash
   flask run
   ```

   The API will be available at `http://127.0.0.1:5000/`.

## 📋 Usage

### Endpoints

- **POST /register** - Register a new user.
  - Request body: `{ "username": "your_username", "password": "your_password" }`
  - Response: `{ "message": "User registered successfully" }`

- **POST /login** - Log in and get a JWT token.
  - Request body: `{ "username": "your_username", "password": "your_password" }`
  - Response: `{ "access_token": "your_jwt_token" }`

- **GET /protected** - Access a protected endpoint.
  - Header: `Authorization: Bearer your_jwt_token`
  - Response: `{ "message": "Protected endpoint accessed" }`

## 🧪 Running Tests

To run the tests for this project:

1. Make sure the virtual environment is activated.

2. Run the tests:

   ```bash
   pytest
   ```

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for review.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

