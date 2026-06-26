# Deploy guide — Groq + Llama 3.3

## 1. Get a free Groq API key
1. Go to https://console.groq.com
2. Sign up (free, no credit card needed)
3. Click **API Keys → Create API Key**
4. Copy it — you'll use it in step 3 below

---

## 2. Run the backend

```bash
# Clone / unzip the project, then:
cd ai-watchdog/backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies (groq instead of anthropic now)
pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY=gsk_...     # Windows: set GROQ_API_KEY=gsk_...

# Start the server
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 3. Open the frontend

Just open `frontend/index.html` directly in your browser — no build step, no npm.

On Mac:
```bash
open ai-watchdog/frontend/index.html
```

On Windows: double-click the file in Explorer.

---

## 4. Run the demo

1. Click **Load sample policy** — loads the Project Atlas policy doc
2. Click **Start meeting** — the backend processes the policy and opens a WebSocket
3. Watch the transcript play out line by line
4. Three contradiction alerts will fire:
   - Budget bumped from $50k → $75k
   - Accessibility review skipped for internal tool
   - Third-party analytics (Mixpanel) wired in despite no-SDK policy
   - Vendor switched mid-meeting (Vendor A → Vendor B)
   - Marketing copy shipped without Legal sign-off

---

## Model used
**Llama 3.3 70B Versatile** via Groq  
Model string: `llama-3.3-70b-versatile`  
Free tier: 14,400 requests/day, 500,000 tokens/minute — more than enough for demos.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `CORS error` in browser console | Make sure backend is running on port 8000 |
| `groq.AuthenticationError` | Check your `GROQ_API_KEY` env var is set |
| `json.JSONDecodeError` | Llama occasionally adds preamble — the `_force_json()` helper strips it. If it persists, re-run the demo. |
| Alerts not firing | Open browser DevTools → Network → WS tab and check the WebSocket messages |
| Frontend shows blank | Open browser console — if you see a fetch error, the backend isn't running |
