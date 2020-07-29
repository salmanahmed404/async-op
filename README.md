# atlan-collect-task

## Description
Atlan Collect​ is a data collection platform that is being used by customers in 50+ countries in more than 200 organizations. Its features include team management, multilingual forms, and offline data collection. Atlan Collect has a variety of long-running tasks that require time and resources on the servers. As it stands now, once we have triggered off a long-running task, there is no way to tap into it and pause/stop/terminate the task. The aim was to create RESTful API(s) to solve this problem.

## Technology Stack Used
- DjangoREST framework (APIs)
- Redis (Message broker)
- Celery (Task scheduler)
- PostgreSQL (Database)
- Docker and Docker-Compose (Containerizing the application)

## Endpoints
1. File upload
    `http://localhost:8000/api/upload-file/`
    Handles POST data containing the uploaded file

2. Task revoke
    `http://localhost:8000/api/revoke/{task_id}/`
    Revoked the task specified by task_id

3. Task pause
    `http://localhost:8000/api/pause/{task_id}/`
    Pauses the task specified by task_id
    Task gets revoked if not resumed within 5 mins

4. Task resume
    `http://localhost:8000/api/resume/{task_id}/`
    Resumes the paused task specified by task_id

5. CSV Export
    `http://localhost:8000/api/export/?from_date={}&to_date={}/`
    Exports the database instances (i.e. form responses in the collect app context)
    in the range of from_date and to_date into csv

6. Documentation
    `http://localhost:8000/docs/`
    Auto generated API documentation

## Running Locally (Development)
1. **Clone the repository**
    `git clone [repository_url]`

2. **Create and activate virtual environment**
    `virtualenv --python=python3 venv` (or any name)
    `source venv/bin/activate`

3. **Navigate to project code**
    `cd project`

4. **Install packages**
    `pip install -r requirements.txt`

5. **Database setup**
    - Ensure you have postgres installed otherwise install using package manager
        `sudo apt-get install postgresql` (for Ubuntu)
    - Create database under the default postgres user
        `sudo su postgres`
        `psql`
        `CREATE DATABASE atlan_collect;`

6. **Run the migrations**
    `python manage.py migrate

7. **Prepare test data** (optional)
    `mkdir data`
    `python generate_dummy_data.py`
    The script accepts command line arguments specifying the number of records in the resulting csv file.
    If not provided it defaults to 20000

8. **Make directory** (for storing the exported csv files)
    `mkdir exports`

9. **Run the development server**
    `python manage.py runserver`

## Building and running the docker container
    `docker-compose up --build`