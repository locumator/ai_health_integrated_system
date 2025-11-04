# Message Drafting System - Implementation Outline

## 📋 Overview
AI-powered message drafting system that analyzes message history and generates personalized messages on behalf of doctors to practices.

## 🏗️ Architecture

### 1. **Dependencies to Install**
```
langchain
langchain-google-genai  # For Gemini
cerebras-cloud-sdk  # For Cerebras AI inference
python-dotenv  # Already installed
```

### 2. **File Structure**
```
app/
├── service/
│   ├── query.py (existing - message history)
│   └── message_drafting.py (NEW - LLM integration)
├── routes.py (add new endpoint)
└── db/database.py (existing)
```

## 🔄 Workflow

### Step 1: Receive Request from Laravel API
**Endpoint**: `POST /draft-message`

**Request Body**:
```json
{
  "doctor_id": 1012382,
  "practice_id": 3015908,
  "session_id": 12345,
  "job_description": "Remote GP session needed...",
  "pricing": 150.00,
  "start_time": "09:00",
  "end_time": "17:00",
  "date": "2025-01-15",
  "practice_name": "Prime Medics",
  "practice_postcode": "SW1A 1AA"
}
```

### Step 2: Fetch Message History
- Use existing `query_message(practice_id, doctor_id)`
- Get all previous messages between doctor and practice
- Extract: message bodies, sender info, timestamps

### Step 3: Analyze History with LLM (Cerebras Primary, Gemini Fallback)
**Analysis Tasks**:
1. **Sentiment Analysis**: 
   - Check if practice replied
   - Determine if reply was positive/negative/neutral
   - Identify rapport level (good rapport vs cold)

2. **Strategy Decision**:
   - If positive reply → Use "rapport template" (shorter, personal)
   - If no reply or negative → Use "default template" (full, detailed)
   - Learn from successful patterns

3. **Tone Adjustment**:
   - Match previous successful message tone
   - Avoid repeating unsuccessful approaches

### Step 4: Generate Draft with LLM (Gemini Primary, Cerebras Fallback)
**Input to LLM**:
- Analysis results from Step 3
- Selected template (default or rapport)
- Job details (description, pricing, time, date)
- Doctor info (name, experience)
- Practice info (name, postcode)
- Session ID

**Output**: Drafted message following template structure

### Step 5: Return Draft
**Response**:
```json
{
  "draft_message": "...",
  "strategy_used": "rapport_template" | "default_template",
  "analysis": {
    "rapport_level": "high" | "medium" | "low",
    "previous_reply_sentiment": "positive" | "negative" | "none",
    "recommendation": "..."
  },
  "session_id": 12345
}
```

## 📝 Template Structure

### Default Template (Full)
```
{session_id}
{date formatted as "D d, M"}
{practice_name}, {practice_postcode}

Hi

Thank you for your request. If the terms are acceptable, please feel free to request Dr.

Start time: {start_time}
End time: {end_time}
Rate: £{pricing} per hr

Remote only

Dr. {doctor_last_name} is one of the most requested doctors on Lantum, having worked in over 300 practices. Please see Dr's profile for further details and the glowing testimonials.

Remote service is great for last-minute coverage or enhancing access. Dr can see many patients remotely, freeing up on-site partners.

Services include triage, advice, prescriptions, medication reviews, weaning controlled meds, admin sessions, MED3 reviews, mental health & dermatology appts, prescription queries, referrals, and extended access.

Please ignore our applications if terms don't suit you -with bulk bookings, is difficult to filter practices on Lantum.

For last-minute bookings, call/text 07515393107 or 07842557072, as we may miss Lantum notifications.

Thanks,

Juliana (Dr's PA)

On Behalf of:
```

### Rapport Template (Shorter, Personal)
```
NOTE: This application is being submitted by Gibril, Dr. {doctor_last_name}'s assistant. Dr. {doctor_last_name} only provides remote GP services via secure NHS N3 connection. She is one of the most requested and recognized doctors on Lantum with extensive experience in remote consultations. Dr. {doctor_last_name} offers efficient patient triage and remote care to help manage your list. If this remote arrangement works for your practice needs, please go ahead and accept. However, if on-site presence is essential, we completely understand that I won't be suitable on this occasion. Please review her profile for more information about her excellent track record. For questions: 07515393107 - Gibril (Assistant to Dr. {doctor_last_name}).
```

## 🔧 Key Functions to Create

### 1. `create_llm_agent(primary_llm, fallback_llm)`
- **Purpose**: Create LangChain agent with dual LLM support
- **Implementation**: 
  - Agent with Cerebras as primary
  - Gemini as fallback
  - Auto-switch on rate limit
  - Tools: message analysis, template selection, message drafting

### 2. `analyze_and_draft_message(agent, messages, job_details, doctor_info, practice_info)`
- **Purpose**: Agent orchestrates entire process
- **Agent Tasks**:
  1. Analyze message history for sentiment/rapport
  2. Decide template strategy (default vs rapport)
  3. Generate drafted message following template
  4. Handle fallback if rate limit hit
- **Returns**: Complete drafted message + strategy used

### 3. `handle_rate_limit(primary_llm, fallback_llm)`
- **Purpose**: Switch between LLMs if rate limit hit
- **Implementation**: Agent automatically handles in try-catch

### 4. Agent Tools/Abilities:
- **Tool 1**: `analyze_sentiment` - Analyze message history
- **Tool 2**: `select_template` - Choose default vs rapport
- **Tool 3**: `draft_message` - Generate message from template

## 🛡️ Error Handling

1. **Rate Limit**: Automatically switch to fallback LLM
2. **No History**: Use default template (first-time application)
3. **LLM Failure**: Return error with fallback option
4. **Missing Data**: Validate all required fields before processing

## 📦 Implementation Steps

1. ✅ Install dependencies (langchain, gemini, cerebras)
2. ✅ Create `.env` file with API keys
3. ✅ Create `message_drafting.py` service
4. ✅ Set up LLM clients with fallback logic
5. ✅ Implement analysis function
6. ✅ Implement drafting function
7. ✅ Create POST endpoint in routes.py
8. ✅ Test with sample data
9. ✅ Handle edge cases

## 🔐 Environment Variables Needed
```
CEREBRAS_API_KEY=your_key
GOOGLE_API_KEY=your_key
```

## 📊 Decision Matrix

| Previous Reply | Sentiment | Template Choice |
|---------------|-----------|----------------|
| Yes | Positive | Rapport |
| Yes | Negative | Default (redraft) |
| No | N/A | Default |
| Yes | Neutral | Default |

---

**Next Steps**: Ready to implement? Confirm if this matches your vision!

