from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Use package-style imports without leading dot so the module can be run as a script from the
# backend directory (python main.py) without triggering relative-import-with-no-parent errors.
from db.session import engine, Base
from api.router import router as api_router
from auth.router import router as auth_router

app = FastAPI(title="Guilt Eater Backend")

# minimal CORS for frontend during oauth redirect
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
	# create DB tables
	Base.metadata.create_all(bind=engine)

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def root():
	return {"message": "Guilt Eater Backend - schema initialized"}
