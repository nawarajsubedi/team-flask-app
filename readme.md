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

## Team Generation Logic
Team Formation Logic
Identify Members: Gather a list of potential team members, each with a defined skill level. Skill levels can range from 1 (beginner) to 5 (expert).
Group by Team: Divide members into teams. Each team can have a mix of different skill levels to ensure balance and collaboration.
Calculate Total Skill Level: For each team, calculate the total skill level by adding up the skill levels of all members in that team. This helps assess the overall capability of the team.
Compare Teams: Once the total skill levels for each team are calculated, compare these totals. This allows you to understand which teams have higher or lower skill levels.
Determine Team Strengths: The team with the highest total skill level might be more suited for complex tasks, while teams with a mix of skill levels can foster learning and growth.
## Example
For instance, if Team A has members with skill levels of 5, 4, and 3, the total skill level is 12. If Team B has members with skill levels of 4, 3, and 2, the total skill level is 9.
In this example, Team A would be considered stronger based on skill level, but Team B might still excel due to other factors like teamwork or communication skills.


