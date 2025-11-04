# Proper JSON Formatting for curl

## ❌ Wrong - Has Literal Newlines (Invalid JSON)

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/draft-message' \
  -H 'Content-Type: application/json' \
  -d '{
  "job_description": "On site free parking available
Can be flexible re start/finish times
Site Manager will ensure..."
}'
```

## ✅ Correct - Escaped Newlines

### Option 1: Use `\n` for newlines

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/draft-message' \
  -H 'Content-Type: application/json' \
  -d '{
  "doctor_id": 1015682,
  "practice_id": 3015951,
  "session_id": 4014399224,
  "job_description": "On site free parking available\nCan be flexible re start/finish times\nSite Manager will ensure you have all necessary access to our clinical systems & support from our Partners, clinical staff, reception team & medical secretaries, during your session.\nCoffee, Tea, Squash available for your use in our staff kitchen.\nOur Clinical rotas include;\n\n16 x 10 min appointments.\n2 x 10 min clinical admin catch up slots\n1 x hour admin",
  "pricing": 190,
  "start_time": "09:30",
  "end_time": "12:30",
  "date": "2025-11-05",
  "practice_name": "GPS Healthcare - Meadowside Health Centre (Branch)",
  "practice_postcode": "B92 8PJ"
}'
```

### Option 2: Use a JSON File (Recommended)

Create `payload.json`:
```json
{
  "doctor_id": 1015682,
  "practice_id": 3015951,
  "session_id": 4014399224,
  "job_description": "On site free parking available\nCan be flexible re start/finish times\nSite Manager will ensure you have all necessary access to our clinical systems & support from our Partners, clinical staff, reception team & medical secretaries, during your session.\nCoffee, Tea, Squash available for your use in our staff kitchen.\nOur Clinical rotas include;\n\n16 x 10 min appointments.\n2 x 10 min clinical admin catch up slots\n1 x hour admin",
  "pricing": 190,
  "start_time": "09:30",
  "end_time": "12:30",
  "date": "2025-11-05",
  "practice_name": "GPS Healthcare - Meadowside Health Centre (Branch)",
  "practice_postcode": "B92 8PJ"
}
```

Then use:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/draft-message' \
  -H 'Content-Type: application/json' \
  -d @payload.json
```

### Option 3: Use Python (Easiest)

```python
import requests
import json

payload = {
    "doctor_id": 1015682,
    "practice_id": 3015951,
    "session_id": 4014399224,
    "job_description": """On site free parking available
Can be flexible re start/finish times
Site Manager will ensure you have all necessary access...""",
    "pricing": 190,
    "start_time": "09:30",
    "end_time": "12:30",
    "date": "2025-11-05",
    "practice_name": "GPS Healthcare - Meadowside Health Centre (Branch)",
    "practice_postcode": "B92 8PJ"
}

response = requests.post(
    "http://127.0.0.1:8000/draft-message",
    json=payload  # requests automatically handles JSON encoding
)
print(response.json())
```

## 🔧 Quick Fix Script

If you have a JSON file with literal newlines, use this Python script to escape them:

```python
import json

# Read your JSON file
with open('input.json', 'r') as f:
    data = json.load(f, strict=False)  # This might fail if JSON is invalid

# Or manually fix the job_description
data = {
    "doctor_id": 1015682,
    "practice_id": 3015951,
    "session_id": 4014399224,
    "job_description": "On site free parking available\nCan be flexible...",  # Use \n
    # ... rest of fields
}

# Write properly formatted JSON
with open('output.json', 'w') as f:
    json.dump(data, f, indent=2)
```

## 💡 Best Practice

**Use FastAPI's interactive docs** at http://localhost:8000/docs - it handles JSON encoding automatically!

