from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

client = MongoClient("mongodb://mongo:HzgBbyZNanVOoXfZmwLjiuUJfuxdwspb@autorack.proxy.rlwy.net:50948")

try:
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connected successfully!!!")
except ConnectionFailure as e:
    print(f"Could not connect to MongoDB: {e}")
    exit(1)

db = client["AIVALD"]
accounts = db["ACCOUNTS"]
datadb = db["DATA"]


async def handle_register(data):
    email = data["email"]
    password = data["password"]
    account = accounts.find_one({"email":email,"password":password})
    if account is None:
        accounts.insert_one({"email":email,"password":password})
        return True
    else:
        return False
    
async def handle_login(data):
    email = data["email"]
    password = data["password"]
    account = accounts.find_one({"email":email,"password":password})
    if account is not None:
        token = str(uuid.uuid4())
        return True,token
    else:
        return False,None
