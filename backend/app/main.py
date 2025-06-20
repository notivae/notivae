import fastapi
from config import settings


app = fastapi.FastAPI(
    debug=True,
    title="Notivae",
)

@app.get("/health")
def health():
    return { "status": "ok" }


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host=settings.APP_HOST, port=settings.APP_PORT)
