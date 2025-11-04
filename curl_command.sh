#!/bin/bash
# Properly formatted curl command with escaped newlines

curl -X 'POST' \
  'http://127.0.0.1:8000/draft-message' \
  -H 'accept: application/json' \
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


