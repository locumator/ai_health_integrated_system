# Message Drafting System - Setup Guide

## ✅ What's Been Created

1. **`app/service/message_drafting.py`** - Main service with LangChain integration
2. **`app/routes.py`** - Added POST `/draft-message` endpoint
3. **`requirements.txt`** - Updated with dependencies

## 📦 Installation Steps

### 1. Install Dependencies
```bash
cd /home/ai/Desktop/ai_health_integrated_system
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create or update `.env` file in project root:
```bash
MONGO_URI=mongodb://localhost:27017
DB_NAME=dagg_api
GOOGLE_API_KEY=your_google_api_key_here
CEREBRAS_API_KEY=your_cerebras_api_key_here  # Optional for now
```

### 3. Get API Keys
- **Google Gemini**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Cerebras**: Get from [Cerebras Cloud](https://cerebras.ai/cloud) (optional for now)

## 🚀 How It Works

### Endpoint: `POST /draft-message`

**Request Body:**
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

**Response:**
```json
{
  "draft_message": "...",
  "strategy_used": "rapport" | "default",
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

## 🔄 Workflow

1. **Fetch Message History** - Uses existing `query_message()` function
2. **Analyze Sentiment** - Determines if practice replied and sentiment
3. **Select Template** - Chooses "rapport" or "default" template
4. **Draft Message** - Generates message using selected template
5. **LLM Refinement** - Uses Gemini/Cerebras to polish the draft
6. **Fallback Handling** - If primary LLM fails, switches to fallback

## 🛠️ Architecture

### LLM Strategy:
- **Primary**: Gemini (Cerebras can be added later)
- **Fallback**: Gemini (if primary fails)
- **Direct Tool**: If both LLMs fail, uses template directly

### Template Selection Logic:
- **Rapport Template**: Used when practice replied positively
- **Default Template**: Used for cold outreach or negative replies

## 📝 Notes

1. **Cerebras Integration**: Currently uses Gemini as primary. Cerebras integration can be added when `cerebras-cloud-sdk` LangChain support is available.

2. **Doctor Last Name**: Extracted from `display_name` field. If you have a separate `last_name` field in your database, update `get_doctor_info()` to return it.

3. **Message History**: Uses existing `query_message()` function - no changes needed!

4. **Error Handling**: System gracefully falls back if LLMs fail.

## 🧪 Testing

Test the endpoint:
```bash
curl -X POST http://localhost:8000/draft-message \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": 1012382,
    "practice_id": 3015908,
    "session_id": 12345,
    "job_description": "Remote GP session",
    "pricing": 150.00,
    "start_time": "09:00",
    "end_time": "17:00",
    "date": "2025-01-15",
    "practice_name": "Prime Medics",
    "practice_postcode": "SW1A 1AA"
  }'
```

## 🔧 Future Enhancements

1. Add Cerebras LLM integration when SDK supports it
2. Add more sophisticated sentiment analysis
3. Learn from successful message patterns
4. Add A/B testing for different templates
5. Store draft history for analytics

---

**Ready to test!** Make sure to:
1. ✅ Install dependencies
2. ✅ Set up `.env` with API keys
3. ✅ Run the FastAPI server
4. ✅ Test the endpoint

