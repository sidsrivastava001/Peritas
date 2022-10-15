import pyrebase

config = {
  "apiKey": "AIzaSyAoG2TvDcVQKhLyjJtjnMALdJlmC9DOsfk",
  "authDomain": "hackharvard-34fe9.firebaseapp.com",
  "databaseURL": "https://hackharvard-34fe9-default-rtdb.firebaseio.com",
  "storageBucket": "hackharvard-34fe9.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()