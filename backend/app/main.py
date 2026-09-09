"""Main FastAPI application with all routes"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import subjects, formulas, exercises, solutions
from app import __version__

# Create FastAPI app
app = FastAPI(
    title="Engineering Study App API",
    description="API para aplicativo de estudos de engenharia com disciplinas, fórmulas, exercícios e resoluções",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(subjects.router)
app.include_router(formulas.router)
app.include_router(exercises.router)
app.include_router(solutions.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Engineering Study App API",
        "version": __version__,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "subjects": "/subjects",
            "formulas": "/formulas",
            "exercises": "/exercises",
            "solutions": "/solutions"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
