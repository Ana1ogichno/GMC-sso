import uvicorn
from app.config.settings import settings


def run():
    uvicorn.run(
        "app.main:app",
        host=settings.project.HOST,
        port=settings.project.PORT,
        reload=True,
        use_colors=True,
    )


if __name__ == "__main__":
    run()
