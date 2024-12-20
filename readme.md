
<samp>

# LLM-IT

## Description

The LLM-IT backend, developed using FastAPI, streamlines KYC processes with a scalable and secure architecture. Key features include efficient data gathering, regulatory compliance, and automated KYC verification, all seamlessly integrated with frontend applications. Using Langraph, we have created agents to collect information, gather documents, and compare data against KYC standards. Users can manually enter their information or upload a pre-filled KYC form, including handwritten documents. Langraph's human interrupts are utilized to integrate FastAPI, ensuring smooth interactions and state management. PostgreSQL is employed for checkpointing states and securely storing encrypted information, thereby maintaining data integrity and privacy.


## Architecture

1. Modular Design: The LLM-IT backend is organized by features, such as authentication, KYC, and shared modules, ensuring a scalable and maintainable codebase.

2. Three-Layer Structure:
- **Endpoints**: Manages API endpoints and user interactions, providing a seamless integration with frontend applications.
- **Services**: Handles business logic and external API communication, leveraging Langraph to create agents for information collection, document gathering, and data comparison against KYC standards.
- **Models**: Defines data schemas for type safety and consistency, utilizing PostgreSQL for checkpointing states and securely storing encrypted information.

## Startup Commands

To set up and run the LLM-it Backend locally, execute the following:

1.**Create a virtual environment**:
```bash
  python3 -m venv venv  
  source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt 
 ```

3. **Start the development server**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000   
  ```
## Technology Stack
- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **Authentication**: Okta
- **Agentic Framework**: Langgraph

## API Documentation
The application is fully integrated with the frontend APIs of LLM-IT, documented with tools like Swagger. Access the API documentation at http://127.0.0.1:8000/docs.

## Local Docker Setup

1.**Insert keys in backend directory**:
- Go to the backend directory and search for constants folder and inside __init__.py insert necessary KEYS where it is needed for running the backend server.
- Postgres db and redis setup will be done in docker.
- After inserting all necessary keys , please go to root directory  .
2. **Steps for docker setup**:
- Install Docker desktop for running docker engine.
- In root dirctory run the following command: docker-compose up -d in terminal. This command will run all necesary services and create images in docker desktop.
- Please go to http://localhost:4200/ for frontend to run the application.
- To check backend api please refer http://localhost:8000/docs
3. **DB Setup in pgadmin**
- Install pgadmin if not installed, for restoring the data and use it before hopping on to the applciation.
- [Pgadmin](https://pgadmin-archive.postgresql.org/pgadmin4/v7.8/windows/index.html)
- After installing please right click on server and register server. Inside give any name for server.
- In connection Hostname : localhost, port: 5432, Username : postgres, Password :root
### DB Connection for pgadmin
```ruby
Hostname = 'localhost'
Port = "5432"  
Username = "postgres"
Password = "root"
```
- Refresh and right click on LLM-IT db , click on restore. In restore first give llmt_schema.sql and second restore llm_data.sql. It will give error message due to pgadmin role but all data will be restored.
- After restoring go to http://localhost:4200/ and run the application.
4. **docker shutdown**
  - Use docker-compose down -v for shutting down all container if not in use.
  
## Note:
1. We have use Python 3.11.9 for development purposes so kindly use the same version for better compatibilty.## Note : 
2. This branch is for docker environment, to run application locally kindly follow steps in the dev-frontend branch.
3. After shutting down of docker container all recently added data in db will perish and again after running docker-compose up follow step 3 of local docker setup.
