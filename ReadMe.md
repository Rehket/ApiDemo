# Demo App for learning some Docker and Python

- Uses An API build on the FastAPI Framework
- Database Backend is postgres.
- Nginx Revers Proxy with Self-signed certificates.

## Warning:
This is a demo project for learning only! If you decide to use some of it in production, please change the certs and read up on the different tools being used. 

## Running With Docker
Use `docker-compose up` to bring up the services. By default, the nginx proxy is exposed 
on port 443 and the database port is exposed on port 5500 

## Local Installation
1. Create a virtual Environment
2. Install the requirements with `python -m pip install -r req.txt`
3. Setup the environment variables in the env.ps1 script.
4. Run `python scripts/setup_initial_user.py` to create the initial users. 
5. Start the service with `uvicorn app.main:app`