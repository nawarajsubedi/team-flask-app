Create a web application that generates random teams from a list of players based on their skill levels.
## Prerequisites

- Python 3.9
- PostgreSQL
- Flask

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nawarajsubedi/team-flask-app
   cd team-flask-app
   ```

2. Create a virtual environment and activate it:
    ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use venv\Scripts\activate\
    ```

3.Install the required dependencies:
   ```bash
    pip install -r requirements.txt
   ```

4.Set up environment variables: Create a .env file with the following:
  ```bash
      DATABASE_URL=postgresql://<user>:<password>@localhost/<database_name>
  ```
4.Set up environment variables: Create a .env file with the following:
  ```bash
  DATABASE_URL=postgresql://<user>:<password>@localhost/<database_name>
```
5.Running the Application
  ```bash
- Initialize the database (if necessary):
flask db upgrade
- Start the Flask development server:
flask --app main --debug run --port 5001

```
6.Run Unit Test
  ```bash
  - python -m unittest discover -s app/tests -p "*.py"
  ```

## Features
- Player Management(Add, Edit, Delete).
- Team Management(Add, Edit, Delete).
- Team Generation
