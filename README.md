# Just getting aquainted with various AI concepts
- Models from Anthropic, Ollama, OpenAI
- Vector Databases: ChromaDB
- RAG (retrieval augmented generation)
- LangChain

## Setup
Create a `.env` file in the root with:
```
OLLAMA_ROOT=ollama
```

## Run

#### Option 1 - run everything in Docker:

$ `docker compose up`

Note that on Mac, Docker will not have access to the GPU which means model responses will be very slow.

#### Option 2 - run the FastAPI app in Docker and Ollama on the host machine:

Install [Ollama](https://ollama.com/)

$ `ollama pull all-minilm`

$ `ollama pull mistral`

$ `ollama serve`

`OLLAMA_ROOT=host.docker.internal`

$ `docker compose -f compose-no-ollama.yaml up`

#### Option 3 - run both the FastAPI app and Ollama on the host machine:

Install and run Ollama as per Option 2.

`OLLAMA_ROOT=localhost`

$ `python3 -m venv venv`

$ `source venv/bin/activate`

$ `pip install -r requirements.txt`

Note that --env-file .env makes uvicorn auto load env vars so that load_dotenv() is not needed.  
$ `uvicorn app.main:app --env-file .env --reload`

## Usage

Endpoints are accessible at http://0.0.0.0:8000

### Chat Endpoints

GET /chat or /chat/langchain
JSON body:
```
{
    "prompt": "Who are you?"
}
```

### Admin Endpoints

POST /admin/collection/document/add  
JSON body:
```
{
    "content": "This is a document"
}
```

GET /admin/collection/count

GET /admin/collection/reset

## Deploy

$ `cd infra`

$ `terraform apply`

$ `cd ../`

$ `./deploy.sh`

Get app URI:  
$ `kubectl get svc`

## Un-deploy

$ `kubectl delete svc --all`

$ `kubectl delete deployment --all`

Wait a few minutes, then...

$ `cd infra`

$ `terraform destroy`