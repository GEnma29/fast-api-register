from pydantic import BaseSettings


class Settings(BaseSettings):
    # default value if env variable does not exist
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_COLLETION_USER: str   # default value if env variable does not exist

# specify .env file location as Config attribute
    class Config:
        env_file = ".env"


settings = Settings()
