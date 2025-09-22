from fastapi import FastAPI

app = FastAPI(title="Week 1 - Hello Tasks")

@app.get("/health")
def health():
    return {"status": "ok"}