import os

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    webhook_secret: str = 'mocksecret123'
    jenkins_user: str = 'mockuser123'
    jenkins_api_token: str = 'mockapitoken123'
    base_dir: str = os.path.abspath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "webfs")
    )

    model_config = {"env_file": ".env"}


settings = Settings()
