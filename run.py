from main import AutomaticContentCreator

credentials = {
    "username": "crazyoutside3f@gmail.com",
    "password": "@Facriz3f",
    "cookies": None  # Tambahkan cookies jika diperlukan
}

creator = AutomaticContentCreator(credentials)
creator.create_and_upload_video()