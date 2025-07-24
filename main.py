from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

app = FastAPI()

@app.get("/hello")
def get_hello(request: Request):
    accept_headers = request.headers.get("Accept")
    if accept_headers != "text/html" and accept_headers != "text/plain":
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
    with open("hello.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    return Response(content=html_content, status_code=200, media_type="text/html")

@app.get("/welcome")
def read_hello(request: Request, name: str= None):
    accept_headers = request.headers.get("Accept")
    if accept_headers != "text/plain":
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=400)
    if name:
        return JSONResponse({"message": f"Welcome {name}"}, status_code=200)
    else:
        return JSONResponse({"message": f"{name} is undefined"}, status_code=400)

class PlayersModel(BaseModel):
    number: int
    name: str

players_store: List[PlayersModel] = []

def serialized_stored_players():
    players_converted = []
    for player in players_store:
        players_converted.append(player.model_dump())
    return players_converted

@app.post("/players")
def create_post(player_payload: List[PlayersModel]):
    players_store.extend(player_payload)
    return JSONResponse({"player information": serialized_stored_players()}, status_code=201)

@app.get("/players")
def list_players():
    return {"players": serialized_stored_players()}

@app.put("/")
def update_or_create_players(player_payload: List[PlayersModel]):
    global players_store

    for new_player in player_load:
        found = False
        for i, existing_player in enumerate(players_store):
            if new_player.number == existing_player.number:
                players_store[i] = new_player
                found = True
                break
        if not found:
            players_store.append(new_player)
    return {"players": serialized_stored_players()}