import pymongo

username = "integral2003"
cluster = 'ssergcluster0.x9eezvr.mongodb.net'
database = "SSDatabase"
p1 = "HPT8X"
p2 = "7Eyit"
p3 = "9JqjrY"

def get_mongobd(): 
    uri = f"mongodb+srv://{username}:{p2+p3+p1}@{cluster}/{database}?retryWrites=true&w=majority"
    try:
      client = pymongo.MongoClient(uri)
    except pymongo.errors.ConfigurationError:
      print("An Invalid URI host error was received.")
      return None
    db = client.SSDatabase
    return db
