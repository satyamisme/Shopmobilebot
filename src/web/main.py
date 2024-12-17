from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.services.auth_service import AuthService
from src.services.product_service import ProductService
from src.database.database import Database
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")
templates = Jinja2Templates(directory="src/web/templates")

db = Database()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.on_event("startup")
async def startup():
    await db.init_db()

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    session = await db.get_session()
    auth_service = AuthService(session)
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = auth_service.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def home(token: str = Depends(oauth2_scheme)):
    session = await db.get_session()
    auth_service = AuthService(session)
    user = await auth_service.get_current_user(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    product_service = ProductService(session)
    products = await product_service.get_all_products()
    
    return {"user": user.username, "products": products}

def run_web():
    uvicorn.run(app, host="0.0.0.0", port=8000)