from fastapi import FastAPI,Depends,Form,HTTPException,status
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token") #looks for authorization headers, it makes it available for rest of the app,tokenurl only used for swagger UI

@app.post("/token")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "john" and password == "pass123":
        return {"token123":"valid_token","token_type":"bearer"} #doubt, generatre access token
    raise HTTPException(status_code=400, detail="Invaid Creditionals")

def decode_token(token: str):
    print("Token received by decode_token:", token) 
    if token == "valid_token":
        return {"name":"john"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Creditionals"
    )

def get_current_user(token:str = Depends(oauth2_scheme)):
    return decode_token(token)

@app.get("/profile")
def get_profile(user=Depends(get_current_user)):
    return {'username':user['name']}