# Script to upload list/dict to MongoDB


from pymongo import MongoClient
import datetime

uri = "mongodb+srv://weathercritic0.vdy3o.mongodb.net/myFirstDatabase?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
client = MongoClient(uri,
                     tls=True,
                     tlsCertificateKeyFile='weathercritic_mongodb.pem')

def append_list(service, param, data):
    db = client['weathercritic']
    collection = db['forecasts']
    timestamp = datetime.datetime.now()
    test_post = {'timestamp':timestamp, 'service':service, 'param':param, 'data':data}
    posts = collection.posts
    post_id = posts.insert_one(test_post).inserted_id



if __name__ == '__main__':
    append_list('met', 'pop', 'test')