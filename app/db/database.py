import os 
from dotenv import load_dotenv 
import motor.motor_asyncio

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')

# Validate required environment variables
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable is not set")

if not db_name:
    raise ValueError("DB_NAME environment variable is not set")

client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
db = client.get_database(db_name)





