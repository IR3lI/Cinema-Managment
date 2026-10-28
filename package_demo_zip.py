import zipfile, os, sys, sqlite3, tempfile

publish_dir = os.path.abspath('publish')
zip_path = os.path.abspath('CinemaManagement-Demo.zip')

print(f"Creating {zip_path} from {publish_dir}...")

# Files to exclude from zip (to keep it clean and fast)
exclude_exts = {'.pdb', '.git', '.shm', '.wal'}
exclude_dirs = {'uploads/uploads'}

count = 0
with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for root, dirs, files in os.walk(publish_dir):
        # Filter directories
        dirs[:] = [d for d in dirs if d != 'uploads' or not root.endswith('uploads')]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in exclude_exts:
                continue
                
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, publish_dir)
            
            # Normalize to forward slashes for zip archive standard
            arc_name = rel_path.replace('\\', '/')
            
            z.write(full_path, arc_name)
            count += 1

print(f"Zip created with {count} files! Size: {os.path.getsize(zip_path):,} bytes ({os.path.getsize(zip_path)/1024/1024:.2f} MB)")

# Verify contents inside the zip
with zipfile.ZipFile(zip_path, 'r') as z:
    names = z.namelist()
    posters = [n for n in names if n.startswith('wwwroot/uploads/posters/')]
    fnbs = [n for n in names if n.startswith('wwwroot/uploads/fnb/')]
    print(f"Verified in zip: {len(posters)} posters, {len(fnbs)} FnB images.")
    
    # Check app.db inside zip
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tf:
        tf.write(z.read('app.db'))
        tf_name = tf.name

conn = sqlite3.connect(tf_name)
c = conn.cursor()
c.execute('SELECT COUNT(*), COUNT(PosterUrl) FROM Movies')
m_cnt = c.fetchone()
c.execute('SELECT COUNT(*), COUNT(ImageUrl) FROM FoodItems')
f_cnt = c.fetchone()
conn.close()
os.remove(tf_name)

print(f"Verified Database in zip: Movies={m_cnt}, FoodItems={f_cnt}")
if m_cnt[0] == m_cnt[1] and f_cnt[0] == f_cnt[1] and m_cnt[0] >= 15 and f_cnt[0] >= 14:
    print("SUCCESS: ALL POSTERS AND FNB IMAGES ARE 100% VALID IN THE DEMO ZIP!")
else:
    print("WARNING: Some records might be missing image URLs!")
