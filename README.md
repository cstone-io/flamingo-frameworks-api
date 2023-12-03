# flamingo-frameworks-api

## Table of Contents
Introduction
Prerequisites
Installation
Getting Started
Usage
API Routes
Seeding The Database

## 1. Introduction
Flamingo Frameworks API is a FastAPI-based microservice designed to facilitate an AI application that utilizes the Retrieval-Augmented Generation (RAG) model to interact with a Large Language Model (LLM) and a vector database called ChromaDB, which is an open-source vector database.

This microservice follows a route-controller-service model to provide a scalable and efficient framework for your AI application. It allows seamless communication between the RAG model, LLM, and ChromaDB while maintaining containerization for easy deployment using Docker and Docker Compose.

## 2. Prerequisites
Before getting started with Flamingo Frameworks API, ensure you have the following prerequisites:

Python 3.7 or higher
Docker and Docker Compose installed (for containerized services). Mac users can
install these via homebrew.

For Mac OS users running Docker via colima is highly recommended.

## 3. Installation
To set up and run the Flamingo Frameworks API, follow these steps:

Clone the repository:

```bash
git clone https://github.com/cstone-io/flamingo-frameworks-api.git
cd flamingo-frameworks-api
```
Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

## 4. Getting Started
Before running the application, make sure you have configured your environment variables, including database connection details and API keys. You can set these in a .env file.

Make sure to copy the .env.template and use that as a baseline to create your
own .env file.

Once the services are built via Docker Compose , you can get started.

```bash
docker-compose -f docker-compose.yml up -d --build
```

## 5. Usage
The Flamingo Frameworks API provides several endpoints to interact with the RAG model, LLM, and ChromaDB. Detailed API documentation can be accessed at http://localhost:3011/docs when the application is running.

## 6. API Routes
Here are some of the key API routes provided by the application:

/api/chat: send a query to the RAG chain and receive a response.

Please refer to the API documentation for more details on each route's usage and parameters.

## 7. Seeding The Database
Once the vector database is up, we will need to seed it with data in order for
it to be useful to us in our queries.

We can easily do this using seed data included in the repo as well as
a population script, both of which are located in the `/chroma` directory.

```bash
cd chroma/
python script.py
cd ..
```
