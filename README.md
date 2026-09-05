```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.index:app --reload --port 3001
```

### FIX:

Nothing to fix in the app — `http://192.168.1.12:3001` is correct. `192.168.1.12` **is** your Mac; that's just its address on your Wi-Fi instead of its self-address. Same machine, same server.

The problem is uvicorn. By default it binds to `127.0.0.1`, which only accepts connections that originate on the Mac itself. Your phone's request arrives on the Wi-Fi interface and nothing is listening there.

Restart the backend with:

```bash
uvicorn api.index:app --reload --host 0.0.0.0 --port 3001
```

`--host 0.0.0.0` = listen on every interface, including Wi-Fi. `localhost:3001` keeps working exactly as before.

Verify it took, from your Mac's browser:

```
http://192.168.1.12:3001/api/health
```

If that returns `{"status":"ok","service":"utooload-backend"}`, the phone will reach it too.

If it still hangs after that, it's one of these:
- Phone on cellular or a guest network instead of the same Wi-Fi
- macOS firewall prompting for incoming connections to Python — allow it