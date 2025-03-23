# Just getting aquainted with various AI concepts
- Models
    - Ollama - mistral for chat
    - Ollama - all-minilm for embeddings
- Vector Databases (ChromaDB)
    - Generate embeddings
    - Store relevant documents for RAG (retrieval augmented generation)

## Run

$ `docker compose up`

Endpoints are accessible at http://0.0.0.0:8000

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

## Deploy

$ `cd infra`

$ `terraform apply`

$ `cd ../`

$ `./deploy.sh`

Get app URI:  
$ `kubectl get svc`

## Un-deploy

$ `cd infra`

$ `terraform destroy`