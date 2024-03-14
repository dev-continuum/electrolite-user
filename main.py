import uvicorn
from app import app
from config import Settings

settings = Settings()

if __name__ == "__main__":
    uvicorn.run(app, host=settings.WEBAPP, port=settings.PORT)