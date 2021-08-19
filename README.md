to run the api locally, ensure all dependencies are installed

change this line in app/main.py

```uri = os.environ.get('MONGO_URI')```

to the equivalent of this for your user

```uri = 'mongodb+srv://username:password@weathercritic0.vdy3o.mongodb.net/weathercritic?retryWrites=true&w=majority'```

run the following command

```FLASK_ENV=development flask run```

you can then hit the following routes in your browser

http://localhost:5000/forecasts
http://localhost:5000/accuracy
http://localhost:5000/leaguetable