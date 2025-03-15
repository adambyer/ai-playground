# Just getting aquainted with various AI concepts
- Models (Ollama)
- Vector Databases (ChromaDB)

## Setup

#### Ollama
[Download and install](https://ollama.com/)

#### Python / FastAPI App

$ `python3 -m venv venv`

$ `source venv/bin/activate`

$ `pip install -r requirements.txt`

## Run

$ `ollama run all-minilm`

$ `python3 -m app.main`

## Usage

### Chat

GET http://127.0.0.1:8000/chat

JSON body:
```
{
    "prompt": "Who are you?"
}
```