# Python Data Engineering Backend

This is a data Engineering Test Backend

- Built in Python version 3.12.0
- Uses [Uses Flask](https://flask.palletsprojects.com/en/2.1.x/) as the server backend.
- Uses [Uses Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/) as the database ORM.
- Uses [HTML](https://en.wikipedia.org/wiki/HTML) for Landing Page development.
- Uses [Pessly Goose](https://pressly.github.io/goose/) for handling database migrations and versioning.
- Uses [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) for Task scheduling and Management
- Uses [Redis](https://redis.io/) as Task and Result Backend for Celery
- Uses [PyTest](https://docs.pytest.org/en/7.1.x/) as the testing framework.
- Uses [Docker and Docker Compose](https://docs.docker.com/compose/) for spinning up PostgreSQL, Redis, Redis Commander and PG Admin4 development instances.
- Uses [Makefile](https://makefiletutorial.com/) to execute commands.

# KEY Notes.
The commands are written in a `Makefile` to make it easier to execute commands. The commands work for Unix Based systems `(Linux and Mac)` to work on  windows machine some modifications maybe required.

There are two Scheduling mechanisms Deployed.
- Once without persistence UsinG `APSSchedular` library. Much simpler to setup but if somethig breaks no tasks are not recoverable.
- An improvement and one with persistence `Celery` with `Celery beat` with uses `Redis` as the broker and result backend.

Currenlty `APSSchedular` approach is commented out, but if you want to use it just comment out celery section and uncomment it, then restart the server.

To get started rename the `.env.sample` to `.env` and fill the required `API_ID` and `API_KEY`

Sometimes the `crontab` scheduler may hand on the terminal, so stopping the `celery beat` terminal and restarting it again may help.

To trigger the currency exchange manually after running the server navigate to `http://localhost:5080/v1/rates/update` and the currency api call will be triggered and the currencies populated to the database.

# Project Structure

## app
- The `app` contains the entry point for the Flask Application and Solution for `Problem 2`.
### task.py
- This file defines the schedules/tasks that will be executed once the crontab runs

## tests
- The `tests` folder contains the tests for the system.
  
## run.py
- This file is used as the entrypoint of the application.


## Dockerfile and docker-compose.yaml
- The `Dockerfile` and `docker-compose.yaml` are the files which containerizes the application.

## Running the project 
### Problem 1
- For `Problem 1` the solution is in `db/scripts` directory. All the data required for the test are in `db/scripts/data` directory and the resulting output in `result_output` directory inside scripts. The `ProblemSolution.sql` is the solution for the `Problem 1` QUESTION. 

To be able to solve problem one. The following steps must be followed.
- Startup the database environment using `make up`.
- Run the migrations to create the necessary tables in the database using `make migratedb` command.
- After the database migration are done, run the command `make populate` to populate the necessary tables for step `Problem 1`. (This step takes care of data preprocessing, cleaning and moving the data into the database from csv files, which are located in `data` directory)
- Once the data population is done successfully you can open the PGAdmin on the browser using url `http://localhost:5050/browser/` then on `Tools->Query Tool` window and copy paste the `Problem1Solution.sql` contents into the window and run to view the results.
- The results of this step can be viewed on `result_output/output_name.csv` file.

### Problem 2
The Database schema design for this problem is found on `db/migrations/20231210110802_currency_exchange_rates`. NOTE: When `make migratedb` is done these tables are created on the database. If you have not run the command in the step above Kindly re-run.
- Create a virtual environment, then install the package dependencies using command `pip install -r requirements.txt`
- Remember to update your `API_ID` and `API_KEY` as provided by the XE account on the `.env`
- After creating the virtual environment and installing the packages start `postgres` , `redis` and `pgadmin4` docker images using `make up` command. This will start the `postgres database` and `redis` used as the database and tasks backend for the application. (Ignore is already run in `Problem 1` above)
- To run the `application` run the command `make server`. This will start the flask app on port `5080` which can be accessed on the browser through `http://127.0.0.1:5080`. This page will bring a UI along with two api endpoints. `v1/rates` which are used to get rates from the database and `v1/rates/update` used to manually update the current rates from the XE account.
- Once the backend is started, `Celery` and `Celery Beat Scheduler` has be started in order to spin up a daily worker that runs twice a day and updates the currency echange rates.
- To start `Celery` run `make celery` command.
- To start `Celery Beat Scheduler` run `make beat` command.
- After accessing the website, create an account and run the scipts in `data.sql` to populate the database with sample data from `PGAdmin 4` web browser.
- To access the `PGAdmin 4` on the browser access the URL `http://localhost:5050/browser/` then create a server with the database credentials in `.env` file.
  
## Running the tests
- To run tests execute the command `make test`. Tests are run in an in-memory `SQLLite` database, this gives no persistence and is deleted once testing session is done.
