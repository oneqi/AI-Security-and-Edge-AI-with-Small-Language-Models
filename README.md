# AI-Security-and-Edge-AI-with-Small-Language-Models
AI Security and Edge AI (Security implications with Small Language Models in IoT)

## Intro
This simple lab illustrates the security implications around
- Data
- AI Models
Using `docker compose` and `Dockerfile` to create
- Chroma (backend / local database)
- Gradio (web front end)
- Ollama (middleware to manage `small language model`)

## Pre-Requisites
Docker
Docker Compose

## Images Used
ghcr.io/chroma-core/chroma:1.5.9
ollama/ollama:0.23.3

## Steps
### Terminal 1
```bash
cd ./AI-Security-and-Edge-AI-with-Small-Language-Models 
docker compose up --build
```
You should see the following output
![Alt text](images/t1.png)

### Terminal 2
```bash
docker exec -it ollama ollama pull phi4-mini:latest
```
You should see the following output
![Alt text](images/t2.png)

### Web Browser
Open a browser and with the following URL
```bash
http://127.0.0.1:7860
```
example
You should see the following output
![Alt text](images/t3.png)

### Terminal 1
To destroy
```bash
CRTL + C
docker compose down
```



