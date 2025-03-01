from fastapi import FastAPI
from router import auth, todos, admin, users
import model.models as models
from database import engine
import uvicorn


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
