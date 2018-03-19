import pyrebase

from local_settings import *

# use your credentials here
config = {
    "apiKey": apiKey,
    "authDomain": authDomain,
    "databaseURL": databaseURL,
    "storageBucket": storageBucket
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

if __name__ == '__main__':
    # data to save
    data = {
        "name": "Mortimer 'Morty' Smith"
    }

    # Pass the user's idToken to the push method
    results = db.child("sensors").get()
    print(results.val())
