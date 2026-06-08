# Windows

# py -m venv env
# .\env\Scripts\activate
# pip install "fastapi[all]" "uvicorn[standard]"

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# uvicorn main:app --reload