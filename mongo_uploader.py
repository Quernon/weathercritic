# Script to upload list/dict to MongoDB


from pymongo import MongoClient
import datetime

uri = "mongodb+srv://weathercritic0.vdy3o.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='weathercritic_mongodb.pem')


db = client['weathercritic']
collection = db['weathercritic']
doc_count = collection.count_documents({})
print(doc_count)

timestamp = datetime.datetime.now()

test_post = {'timestamp':timestamp, 'service':'met', 'param':'pop'}

posts = db.posts
post_id = posts.insert_one(test_post).inserted_id
post_id
