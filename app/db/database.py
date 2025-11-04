import os 
from dotenv import load_dotenv 
import motor.motor_asyncio

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
db_name = os.getenv('DB_NAME')


client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
db = client.get_database(db_name)





