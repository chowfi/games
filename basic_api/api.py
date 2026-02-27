from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory state for the message
current_message = "hello world"
messages = []


class MessageUpdate(BaseModel):
    message: str

# GET /message
@app.get("/message")
def read_root():
    return {"message": current_message}

# PUT /message
# Accepts a body
@app.put("/message")
def update_message(update: MessageUpdate):
    global current_message
    current_message = update.message
    return {"message": current_message}

# GET /messages 
# return all of the message
@app.get("/messages")
def read_root():
    return {"messages": messages}

# POST /messages
# create new message and add it to the "messages" list
@app.post("/messages")
def create_message(update: MessageUpdate):
    global messages
    messages.append(update.message)
    return {"messages": messages}