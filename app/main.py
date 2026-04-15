from fastapi import FastAPI
from app.core.database import Base, engine

from app.models import user, team, membership, project

from app.api.routes import auth, users, teams, tasks, projects, analytics


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Workflow Management API")

@app.get("/")
def root():
    return {"message": "Workflow API running"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(teams.router)
app.include_router(tasks.router)
app.include_router(projects.router)
app.include_router(analytics.router)