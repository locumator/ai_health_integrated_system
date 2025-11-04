# Laravel Integration Guide

## How to Call the FastAPI Endpoint from Laravel

### ✅ Method 1: Using Laravel HTTP Facade (Recommended)

```php
<?php

use Illuminate\Support\Facades\Http;

// In your Laravel controller or service
public function draftMessage($doctorId, $practiceId, $sessionId, $jobDescription, $pricing, $startTime, $endTime, $date, $practiceName, $practicePostcode)
{
    try {
        $response = Http::post('http://127.0.0.1:8000/draft-message', [
            'doctor_id' => $doctorId,
            'practice_id' => $practiceId,
            'session_id' => $sessionId,
            'job_description' => $jobDescription, // Laravel automatically handles multiline strings!
            'pricing' => $pricing,
            'start_time' => $startTime,
            'end_time' => $endTime,
            'date' => $date,
            'practice_name' => $practiceName,
            'practice_postcode' => $practicePostcode,
        ]);

        if ($response->successful()) {
            return $response->json();
        } else {
            // Handle error
            return [
                'error' => true,
                'message' => $response->body(),
                'status' => $response->status()
            ];
        }
    } catch (\Exception $e) {
        return [
            'error' => true,
            'message' => $e->getMessage()
        ];
    }
}
```

### ✅ Method 2: Using Guzzle HTTP Client

```php
<?php

use GuzzleHttp\Client;

$client = new Client([
    'base_uri' => 'http://127.0.0.1:8000',
    'timeout' => 30.0,
]);

try {
    $response = $client->post('/draft-message', [
        'json' => [
            'doctor_id' => $doctorId,
            'practice_id' => $practiceId,
            'session_id' => $sessionId,
            'job_description' => $jobDescription, // Multiline string - Guzzle handles it!
            'pricing' => $pricing,
            'start_time' => $startTime,
            'end_time' => $endTime,
            'date' => $date,
            'practice_name' => $practiceName,
            'practice_postcode' => $practicePostcode,
        ]
    ]);

    $result = json_decode($response->getBody()->getContents(), true);
    return $result;
    
} catch (\GuzzleHttp\Exception\RequestException $e) {
    // Handle error
    return [
        'error' => true,
        'message' => $e->getMessage()
    ];
}
```

### ✅ Method 3: Using cURL (Low-level)

```php
<?php

$data = [
    'doctor_id' => $doctorId,
    'practice_id' => $practiceId,
    'session_id' => $sessionId,
    'job_description' => $jobDescription, // Can be multiline - json_encode handles it!
    'pricing' => $pricing,
    'start_time' => $startTime,
    'end_time' => $endTime,
    'date' => $date,
    'practice_name' => $practiceName,
    'practice_postcode' => $practicePostcode,
];

$ch = curl_init('http://127.0.0.1:8000/draft-message');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data)); // json_encode handles multiline!
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Content-Type: application/json',
    'Accept: application/json'
]);

$response = curl_exec($ch);
$statusCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($statusCode === 200) {
    return json_decode($response, true);
} else {
    return ['error' => true, 'response' => $response];
}
```

## 📝 Complete Laravel Example

### Example Controller

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class MessageDraftingController extends Controller
{
    public function draftMessage(Request $request)
    {
        $validated = $request->validate([
            'doctor_id' => 'required|integer',
            'practice_id' => 'required|integer',
            'session_id' => 'required|integer',
            'job_description' => 'required|string',
            'pricing' => 'required|numeric',
            'start_time' => 'required|string',
            'end_time' => 'required|string',
            'date' => 'required|date',
            'practice_name' => 'required|string',
            'practice_postcode' => 'required|string',
        ]);

        try {
            $response = Http::timeout(30)->post('http://127.0.0.1:8000/draft-message', $validated);

            if ($response->successful()) {
                return response()->json($response->json());
            } else {
                return response()->json([
                    'error' => true,
                    'message' => 'Failed to draft message',
                    'details' => $response->body()
                ], $response->status());
            }
        } catch (\Exception $e) {
            return response()->json([
                'error' => true,
                'message' => $e->getMessage()
            ], 500);
        }
    }
}
```

### Example Route

```php
// routes/api.php
Route::post('/draft-message', [MessageDraftingController::class, 'draftMessage']);
```

## 🔑 Key Points

1. **Laravel automatically handles multiline strings** - When you use `Http::post()` or `json_encode()`, Laravel/Guzzle automatically escapes newlines as `\n` in JSON
2. **No manual escaping needed** - Just pass the string as-is, Laravel handles it
3. **Use `json` key in Guzzle** - Guzzle automatically encodes to JSON
4. **Use array in Http facade** - Laravel's Http facade automatically converts arrays to JSON

## ⚠️ Important Notes

1. **Environment Variable**: Store the FastAPI URL in `.env`:
   ```env
   FASTAPI_URL=http://127.0.0.1:8000
   ```

2. **Timeout**: Set appropriate timeout for LLM processing:
   ```php
   Http::timeout(30)->post(...) // 30 seconds
   ```

3. **Error Handling**: Always handle errors gracefully

4. **Production URL**: Update URL for production:
   ```php
   config('services.fastapi.url') // Store in config/services.php
   ```

## 🧪 Testing from Laravel

```php
// In tinker or a test
$jobDescription = "On site free parking available
Can be flexible re start/finish times
Site Manager will ensure...";

Http::post('http://127.0.0.1:8000/draft-message', [
    'doctor_id' => 1015682,
    'practice_id' => 3015951,
    'session_id' => 4014399224,
    'job_description' => $jobDescription, // Works perfectly!
    // ... rest of fields
]);
```

## ✅ Why This Works

- **Laravel's `json_encode()`** automatically escapes newlines as `\n`
- **HTTP Facade** automatically converts arrays to JSON
- **Guzzle** handles JSON encoding properly
- **No manual escaping needed** - Laravel handles it all!


