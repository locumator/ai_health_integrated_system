# Testing the Draft Message Endpoint

## 🚀 Method 1: FastAPI Auto-Generated Docs (Easiest!)

FastAPI automatically generates interactive API documentation!

### Steps:
1. **Start your server:**
   ```bash
   cd /home/ai/Desktop/ai_health_integrated_system/app
   fastapi dev main.py
   ```

2. **Open in browser:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test the endpoint:**
   - Click on `POST /draft-message`
   - Click "Try it out"
   - Fill in the request body (see example below)
   - Click "Execute"
   - See the response!

## 📋 Example Request Body

```json
{
  "doctor_id": 1012382,
  "practice_id": 3015908,
  "session_id": 12345,
  "job_description": "Remote GP session needed for urgent coverage",
  "pricing": 150.00,
  "start_time": "09:00",
  "end_time": "17:00",
  "date": "2025-01-15",
  "practice_name": "Prime Medics",
  "practice_postcode": "SW1A 1AA"
}
```

## 🔧 Method 2: Using cURL (Command Line)

```bash
curl -X POST "http://localhost:8000/draft-message" \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": 1012382,
    "practice_id": 3015908,
    "session_id": 12345,
    "job_description": "Remote GP session needed for urgent coverage",
    "pricing": 150.00,
    "start_time": "09:00",
    "end_time": "17:00",
    "date": "2025-01-15",
    "practice_name": "Prime Medics",
    "practice_postcode": "SW1A 1AA"
  }'
```

## 🐍 Method 3: Using Python (requests library)

```python
import requests
import json

url = "http://localhost:8000/draft-message"

payload = {
    "doctor_id": 1012382,
    "practice_id": 3015908,
    "session_id": 12345,
    "job_description": "Remote GP session needed for urgent coverage",
    "pricing": 150.00,
    "start_time": "09:00",
    "end_time": "17:00",
    "date": "2025-01-15",
    "practice_name": "Prime Medics",
    "practice_postcode": "SW1A 1AA"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

## 📱 Method 4: Using Postman

1. **Create new request:**
   - Method: `POST`
   - URL: `http://localhost:8000/draft-message`

2. **Set headers:**
   - Key: `Content-Type`
   - Value: `application/json`

3. **Set body:**
   - Select "raw" and "JSON"
   - Paste the example JSON above

4. **Send request**

## ✅ Expected Response

```json
{
  "draft_message": "12345\nWed 15, Jan\nPrime Medics, SW1A 1AA\n\nHi\n\nThank you for your request...",
  "strategy_used": "rapport",
  "analysis": {
    "has_reply": true,
    "sentiment": "positive",
    "rapport_level": "high",
    "messages_sent": 5,
    "messages_received": 3
  },
  "session_id": 12345
}
```

## 🔍 What Each Field Does

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `doctor_id` | int | ID of the doctor | `1012382` |
| `practice_id` | int | ID of the practice | `3015908` |
| `session_id` | int | Session/booking ID | `12345` |
| `job_description` | string | Description of the job | `"Remote GP session..."` |
| `pricing` | float | Hourly rate | `150.00` |
| `start_time` | string | Start time (HH:MM) | `"09:00"` |
| `end_time` | string | End time (HH:MM) | `"17:00"` |
| `date` | string | Date (YYYY-MM-DD) | `"2025-01-15"` |
| `practice_name` | string | Name of practice | `"Prime Medics"` |
| `practice_postcode` | string | Practice postcode | `"SW1A 1AA"` |

## 🧪 Quick Test Script

Save this as `test_endpoint.py`:

```python
import requests
import json

def test_draft_message():
    url = "http://localhost:8000/draft-message"
    
    payload = {
        "doctor_id": 1012382,
        "practice_id": 3015908,
        "session_id": 12345,
        "job_description": "Remote GP session needed",
        "pricing": 150.00,
        "start_time": "09:00",
        "end_time": "17:00",
        "date": "2025-01-15",
        "practice_name": "Prime Medics",
        "practice_postcode": "SW1A 1AA"
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        print("✅ Success!")
        print(json.dumps(response.json(), indent=2))
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        if hasattr(e.response, 'text'):
            print(e.response.text)

if __name__ == "__main__":
    test_draft_message()
```

Run it:
```bash
python test_endpoint.py
```

## ⚠️ Common Issues

1. **"422 Validation Error"** - Missing or wrong field types
2. **"500 Internal Server Error"** - Check if MongoDB is running and API keys are set
3. **"Connection refused"** - Make sure FastAPI server is running

## 🎯 Best Method for Testing

**Use FastAPI Docs** (`http://localhost:8000/docs`) - it's the easiest and shows you exactly what fields are required!

