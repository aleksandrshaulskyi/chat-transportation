from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    #BASE
    default_datetime_format: str = '%Y-%m-%dT%H:%M:%S.%fZ'
    standard_unauthenticated_code: int = 4401
    #SECURITY
    key: str = Field(validation_alias='KEY')
    algorithm: str = Field(validation_alias='ALGORITHM')
    connection_pass_length: str = Field(validation_alias='CONNECTION_PASS_LENGTH')
    connection_pass_expiration_time: str = Field(validation_alias='CONNECTION_PASS_EXPIRATION_TIME')
    #REDIS
    redis_url: str = Field(validation_alias='REDIS_URL')
    connected_users_name: str = 'connected_users'
    #RABBITMQ
    rabbitmq_url: str = Field(validation_alias='RABBITMQ_URL')
    websockets_exchange_name: str = Field(validation_alias='WEBSOCKETS_EXCHANGE_NAME')
    database_exchange_name: str = Field(validation_alias='DATABASE_EXCHANGE_NAME')
    channel_prefetch_messages_count: int = 16
    #CORS
    cors_origins: list = ['http://localhost:3000']

    model_config = {
        'env_file': './env',
        'extra': 'allow',
    }

settings = Settings()
