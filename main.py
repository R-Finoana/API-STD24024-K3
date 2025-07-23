from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

app = FastAPI()

@app.get("/")
def get_info(request: Request):
    accept_headers = request.headers.get("Accept")
    if accept_headers != "text/html" or accept_headers != "text/html":
        return JSONResponse({"message": "Unsupported Media Type"}, status_code=415)
    return JSONResponse(content="HELLO WORLD", status_code=200)

@app.post("/")
def create_post():
    return {"message":f"Hello"}

@app.put("/")
def put_update():
    return Response({"message": "Update recorded successfully !"}, status_code=200)
