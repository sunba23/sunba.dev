import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    webhook_secret: str
    jenkins_user: str
    jenkins_api_token: str
    base_dir: str = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../webfs")
    )

    model_config = {"env_file": ".env"}


settings = Settings()
