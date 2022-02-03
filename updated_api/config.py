from os import environ, getcwd, path

port = 8082

url = f"http://localhost:{port}/"

class Config:
    """Set Flask configuration from .env file."""

    # General Config
    # SECRET_KEY = environ.get('SECRET_KEY') DEAL WITH THIS LATER

    # Database
    
    directory = getcwd()
    
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{directory}/UpAndDownTheRiverMultiplayer.db"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False