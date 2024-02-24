from fastapi import FastAPI
from routes import contacts, users #, notes, tags
import uvicorn

app = FastAPI()

app.include_router(users.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
# app.include_router(admin.router, prefix='/api')
# app.include_router(notes.router, prefix='/api')


@app.get("/")
def read_root():
    return {"root message": "FastAPI hw12 started!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

