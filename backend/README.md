
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

## Build and Deployment

1.**Build the project for production**:
```bash
uvicorn main:app --reload
  ```
2. **Steps for deployment**:
- Update the environment file with production configurations.
- Use CI/CD pipelines for continuous integration and deployment.

## Note:
1. We have use Python 3.11.9 for development purposes so kindly use the same version for better compatibilty.## Note : 
1. This branch is for production environment, to run application locally kindly follow steps in the dev-frontend branch.
