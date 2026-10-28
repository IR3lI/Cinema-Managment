import subprocess, time, urllib.request, re, os, sys

exe_path = os.path.abspath('publish/CineManagement.exe')
cwd_path = os.path.abspath('publish')
print(f"Launching {exe_path} in {cwd_path}")

proc = subprocess.Popen([exe_path, '--urls', 'http://127.0.0.1:5055'], cwd=cwd_path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# Wait for server ready
started = False
for _ in range(60):
    time.sleep(1)
    try:
        with urllib.request.urlopen('http://127.0.0.1:5055/', timeout=2) as resp:
            if resp.status == 200:
                started = True
                break
    except Exception:
        pass

if not started:
    print("Server failed to start in 60s")
    proc.terminate()
    sys.exit(1)

print("SERVER IS READY! Fetching Home page...")

try:
    with urllib.request.urlopen('http://127.0.0.1:5055/') as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    print(f"Home page loaded, length: {len(html)}")
    
    img_matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    print(f"Total img tags found: {len(img_matches)}")
    for src in img_matches:
        if any(k in src.lower() for k in ['poster', 'fnb', 'upload']):
            full_url = 'http://127.0.0.1:5055' + src if src.startswith('/') else src
            try:
                with urllib.request.urlopen(full_url) as img_resp:
                    data = img_resp.read()
                    print(f"[OK] {src} -> {img_resp.status} ({img_resp.headers.get('Content-Type')}) size={len(data)}")
            except Exception as e:
                print(f"[FAIL] {src} -> {e}")
                
    # Also test an FnB page
    print("\nTesting FnB page...")
    try:
        with urllib.request.urlopen('http://127.0.0.1:5055/Food') as resp:
            fnb_html = resp.read().decode('utf-8', errors='ignore')
        fnb_imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', fnb_html)
        print(f"Total FnB images found on /Food: {len(fnb_imgs)}")
        for src in fnb_imgs:
            if 'fnb' in src.lower() or 'upload' in src.lower():
                full_url = 'http://127.0.0.1:5055' + src if src.startswith('/') else src
                try:
                    with urllib.request.urlopen(full_url) as img_resp:
                        data = img_resp.read()
                        print(f"[OK FnB] {src} -> {img_resp.status} size={len(data)}")
                except Exception as e:
                    print(f"[FAIL FnB] {src} -> {e}")
    except Exception as e:
        print(f"Could not load /Food: {e}")

finally:
    proc.terminate()
    print("Process terminated.")
