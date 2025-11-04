#!/usr/bin/env python3
"""
Quick test script for the draft-message endpoint
"""
import requests
import json

def test_draft_message():
    url = "http://localhost:8000/draft-message"
    
    payload = {
        "doctor_id": 1015682,
        "practice_id": 3015951,
        "session_id": 4014399224,
        "job_description": """On site free parking available
Can be flexible re start/finish times
Site Manager will ensure you have all necessary access to our clinical systems & support from our Partners, clinical staff, reception team & medical secretaries, during your session.
Coffee, Tea, Squash available for your use in our staff kitchen.
Our Clinical rotas include;

16 x 10 min appointments.
2 x 10 min clinical admin catch up slots
1 x hour admin""",
        "pricing": 190,
        "start_time": "09:30",
        "end_time": "12:30",
        "date": "2025-11-05",
        "practice_name": "GPS Healthcare - Meadowside Health Centre (Branch)",
        "practice_postcode": "B92 8PJ"
    }
    
    print("🚀 Testing draft-message endpoint...")
    print(f"📤 Sending request to: {url}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    print("\n" + "="*50 + "\n")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        print("✅ Success!")
        print(f"📥 Status Code: {response.status_code}")
        print("\n📄 Response:")
        print(json.dumps(response.json(), indent=2))
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to server")
        print("   Make sure FastAPI server is running on http://localhost:8000")
    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out")
        print("   The LLM might be taking too long to respond")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        print(f"   Status Code: {response.status_code}")
        if hasattr(e.response, 'text'):
            print(f"   Response: {e.response.text}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    test_draft_message()

