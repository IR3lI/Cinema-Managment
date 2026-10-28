import urllib.request, os

os.makedirs('CineManagement/wwwroot/uploads/posters', exist_ok=True)
os.makedirs('publish/wwwroot/uploads/posters', exist_ok=True)

# Candidate URLs for the 15 movies
posters = {
    1: 'https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg', # Avengers Endgame
    2: 'https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg', # Spider-Man Across the Spider-Verse
    3: 'https://image.tmdb.org/t/p/w500/8Gxv8gSFCU0XGDykEGv7zR1n2ua.jpg', # Oppenheimer
    4: 'https://m.media-amazon.com/images/M/MV5BMjA5NzQ4MTEtYWM3NC00ODg1LWE5ZjItMDViN2FlNWJkYzk4XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', # Doraemon
    5: 'https://m.media-amazon.com/images/M/MV5BZmRhMjQ0OTgtZmUzMi00YmU0LWJmZjctYjAxYjE0YjBhZGY0XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', # Mai
    6: 'https://m.media-amazon.com/images/M/MV5BNTIxNDdhMWQtNjFhMC00Y2IxLWIxZWEtNTFhZGM0ZmI1ZTFmXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', # Exhuma
    7: 'https://image.tmdb.org/t/p/w500/fiVW06jE7z9YBoio5v3O3ZeAnY.jpg', # Fast X
    8: 'https://m.media-amazon.com/images/M/MV5BODg2MGY0YWYtNWVjYy00OGJjLWIyY2ItMTZkMzk2MjFkYjQ1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', # Cô Dâu Hào Môn
    9: 'https://image.tmdb.org/t/p/w500/1pdfLvkbY9ohJlCjQH2CZjjYVvJ.jpg', # Dune 2
    10: 'https://image.tmdb.org/t/p/w500/kDp1vUBnMpe8ak4rjgl3cLELqjU.jpg', # Kung Fu Panda 4
    11: 'https://image.tmdb.org/t/p/w500/8cdWjvZQUExUUTzyp4t6EDMubfO.jpg', # Deadpool & Wolverine
    12: 'https://image.tmdb.org/t/p/w500/vpnVM9B6NMmQpWeZvzLvDESb2QY.jpg', # Inside Out 2
    13: 'https://m.media-amazon.com/images/M/MV5BYzA2ZGVjMWEtODk4MS00MTFhLWEzZTUtYTI3MTU5N2YxNmE1XkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg', # Lật Mặt 7
    14: 'https://image.tmdb.org/t/p/w500/phmjv9hvYc2525nC18K960L5Y0P.jpg', # Godzilla x Kong
    15: 'https://image.tmdb.org/t/p/w500/pjnD08FlMAIXsfOLKQbvmO0f0MD.jpg'  # Twisters
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for mid, url in posters.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        
        path1 = f'CineManagement/wwwroot/uploads/posters/poster_{mid}.jpg'
        path2 = f'publish/wwwroot/uploads/posters/poster_{mid}.jpg'
        with open(path1, 'wb') as f: f.write(data)
        with open(path2, 'wb') as f: f.write(data)
        print(f'Movie {mid}: downloaded {len(data)} bytes')
    except Exception as e:
        print(f'Movie {mid} ERR: {e}')
