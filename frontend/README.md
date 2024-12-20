<samp>

# LLM-IT



## Description

The LLM-it is a web application developed using Angular. This project showcases a scalable architecture and includes essential features like state management, reusable components, and advanced functionalities to interact seamlessly with backend APIs.

## Architecture

Modular Design: Organized by features (e.g., authentication, Home, shared modules).

Three-Layer Structure:
1. **Components**: Manages UI and user interactions.
2. **Services**: Handles business logic and API communication.
3. **Models**: Defines data schemas for type safety and consistency.

## Startup Commands
To set up and run the LLM-it Frontend locally, execute the following:

1.**Install dependencies**:
```bash
npm install  
```

2. **Start the development server**:
```bash
ng serve --port 4200  
 ```


## Technology Stack
- Frontend Framework: Angular
- Styling: SCSS

## API Documentation
The application is fully integrated with the backend APIs of LLM-it, documented with tools like Swagger.

## Build and Deployment
1.**Build the project for production:**
```bash
ng build --prod  
  ```
2. **Steps for deployment:**
- Update the environment file with production configurations.
- Use CI/CD pipelines for continuous integration and deployment.

## Note:
1. Use This Branch If you want to run this application locally
2. If you are running fast-api backend on any other port, kindly update the port number in the following file path.

```bash
src -> app -> utilities -> services -> rest.service.ts -> baseUrl (line 12)
```




</samp>
