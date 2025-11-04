<?php
/**
 * Example: How to call FastAPI draft-message endpoint from Laravel
 * 
 * This shows how Laravel automatically handles multiline strings in JSON
 */

use Illuminate\Support\Facades\Http;

// Example 1: Using Laravel HTTP Facade (Easiest)
function draftMessageWithHttpFacade()
{
    $jobDescription = "On site free parking available
Can be flexible re start/finish times
Site Manager will ensure you have all necessary access to our clinical systems & support from our Partners, clinical staff, reception team & medical secretaries, during your session.
Coffee, Tea, Squash available for your use in our staff kitchen.
Our Clinical rotas include;

16 x 10 min appointments.
2 x 10 min clinical admin catch up slots
1 x hour admin";

    try {
        $response = Http::timeout(30)->post('http://127.0.0.1:8000/draft-message', [
            'doctor_id' => 1015682,
            'practice_id' => 3015951,
            'session_id' => 4014399224,
            'job_description' => $jobDescription, // ✅ Laravel handles multiline automatically!
            'pricing' => 190,
            'start_time' => '09:30',
            'end_time' => '12:30',
            'date' => '2025-11-05',
            'practice_name' => 'GPS Healthcare - Meadowside Health Centre (Branch)',
            'practice_postcode' => 'B92 8PJ',
        ]);

        if ($response->successful()) {
            return $response->json();
        } else {
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

// Example 2: Using Guzzle Client
function draftMessageWithGuzzle()
{
    $client = new \GuzzleHttp\Client([
        'base_uri' => 'http://127.0.0.1:8000',
        'timeout' => 30.0,
    ]);

    $jobDescription = "On site free parking available
Can be flexible re start/finish times
Site Manager will ensure...";

    try {
        $response = $client->post('/draft-message', [
            'json' => [ // ✅ 'json' key automatically encodes to JSON!
                'doctor_id' => 1015682,
                'practice_id' => 3015951,
                'session_id' => 4014399224,
                'job_description' => $jobDescription, // ✅ Multiline works!
                'pricing' => 190,
                'start_time' => '09:30',
                'end_time' => '12:30',
                'date' => '2025-11-05',
                'practice_name' => 'GPS Healthcare - Meadowside Health Centre (Branch)',
                'practice_postcode' => 'B92 8PJ',
            ]
        ]);

        return json_decode($response->getBody()->getContents(), true);
    } catch (\GuzzleHttp\Exception\RequestException $e) {
        return [
            'error' => true,
            'message' => $e->getMessage()
        ];
    }
}

// Example 3: Complete Laravel Controller
class MessageDraftingController extends \App\Http\Controllers\Controller
{
    public function draftMessage(\Illuminate\Http\Request $request)
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
            $response = Http::timeout(30)->post(config('services.fastapi.url') . '/draft-message', $validated);

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

/*
 * KEY POINTS:
 * 
 * 1. Laravel's Http::post() automatically converts arrays to JSON
 * 2. Multiline strings are automatically escaped as \n in JSON
 * 3. No manual escaping needed - Laravel handles it all!
 * 4. Use 'json' key in Guzzle for automatic JSON encoding
 * 5. Set appropriate timeout (30 seconds recommended for LLM)
 */


