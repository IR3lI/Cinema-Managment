import urllib.request, re

movie_ids = {
    'godzilla_x_kong': 823464,
    'furiosa': 786892,
    'mai': 1234821,
    'lat_mat_7': 1251978,
    'exhuma': 1017163,
    'co_dau_hao_mon': 1341395,
    'dat_rung_phuong_nam': 1092898,
    'doraemon': 1147400
}

posters = {}
for name, mid in movie_ids.items():
    try:
        url = f'https://www.themoviedb.org/movie/{mid}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        m = re.search(r'https://image\.tmdb\.org/t/p/w500/[^"]+\.jpg', html)
        if m:
            posters[name] = m.group(0)
            print(f'{name}: {m.group(0)}')
        else:
            print(f'{name}: not found')
    except Exception as e:
        print(f'{name} ERR: {e}')
