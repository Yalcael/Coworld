# 🐱🍽️ Coworld 🍽️🐱
Welcome to Coworld, the backend project for a restaurant application where Cowcow, the adorable cat with cow-like colors, presents various types of dishes from around the world. This project uses FastAPI, Pydantic, and SQLModel to provide a robust and efficient API for managing restaurant data. Pytest is used for testing to ensure reliability and stability.

# ✨ Features

    🚀 FastAPI: A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
    📏 Pydantic: Data validation and settings management using Python type annotations.
    🗄️ SQLModel: SQL databases in Python, designed to be intuitive, easy to use, and compatible with SQLAlchemy.
    🧪 Pytest: A testing framework that makes it easy to write simple and scalable test cases.
    💾 SQLite: A lightweight, disk-based database that doesn’t require a separate server process.

# 📦 Installation
  1. Clone the repository:
     ```bash
     git clone https://github.com/yourusername/coworld.git
     cd coworld
     ```
     
  2. Create and activate a virtual environment:
     ```bash
     python3 -m venv env
     source env/bin/activate  # On Windows use `env\Scripts\activate`
     ```
     
  3. Install the dependencies:
     ```
     pip install -r requirements.txt
     ```

  4. Set up the database:
     The project uses SQLite, so no additional database configuration is needed. The database file will be created automatically.
     ```
     # Create the database tables
     python main.py
     ```

# 🚀 Usage
To run the FastAPI application:
```bash
uvicorn main:app --reload
```
This will start the server on http://127.0.0.1:7000, and you can access the automatic interactive API documentation at http://127.0.0.1:7000/docs.

# 📂 Project Structure
```markdown
coworld/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── dish.py
│   │   └── ...
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── dishes.py
│   │   └── ...
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── dish.py
│   │   └── ...
│   ├── crud.py
│   ├── database.py
│   └── ...
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── ...
├── requirements.txt
├── README.md
└── ...
```

# 🧪 Testing
To run the tests using Pytest:
```bash
pytest
```

# 📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.




























