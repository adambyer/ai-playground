# Just getting aquainted with various AI concepts
- Models (Ollama - mistral, all-minilm)
- Vector Databases (ChromaDB)
    - Generate embeddings
    - Store previous prompts for cached response when prompt is similar

## Setup

#### Ollama
[Download and install](https://ollama.com/)

#### Python / FastAPI App

$ `python3 -m venv venv`

$ `source venv/bin/activate`

$ `pip install -r requirements.txt`

## Run

$ `python3 -m app.main`

## Usage

### Chat Endpoints

GET /chat

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

## Cleanup
Note: Ollama will automatically start/stop models as needed, but you can manually stop with this...

$ `ollama stop mistral`