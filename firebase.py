import pyrebase

config = {
    "apiKey": "AIzaSyDdmlolGTVHtLn9uajIvp_H8lJIQarppxo",
    "authDomain": "helloudacity-1195.firebaseapp.com",
    "databaseURL": "https://helloudacity-1195.firebaseio.com/",
    "storageBucket": "helloudacity-1195.appspot.com"
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