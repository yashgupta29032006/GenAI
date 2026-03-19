import requests
import json
import sys

def test_endpoint(url, path, method="GET", payload=None):
    full_url = f"{url}{path}"
    headers = {"Content-Type": "application/json"}
    
    print(f"\n--- Testing {method} {full_url} ---")
    if payload:
        print(f"Payload: {json.dumps(payload)[:100]}...")
    
    try:
        if method == "POST":
            response = requests.post(full_url, data=json.dumps(payload), headers=headers)
        else:
            response = requests.get(full_url, headers=headers)
        
        print(f"Status Code: {response.status_code}")
        result = response.json()
        print("Response Body:")
        print(json.dumps(result, indent=2))
        return response.status_code, result
    except Exception as e:
        print(f"Error during request: {e}")
        return 500, str(e)

if __name__ == "__main__":
    # Change this to your live URL after deployment
    BASE_URL = "http://localhost:8080"
    
    print("Starting AI Summarizer Agent Production Tests...")
    
    # 1. Health Check
    test_endpoint(BASE_URL, "/health")
    
    # 2. Success Case
    sample_text = "ADK simplifies agent development by providing a code-first Python framework for building and deploying AI agents."
    test_endpoint(BASE_URL, "/summarize", "POST", {"text": sample_text})
    
    # 3. Validation Case (Empty Text)
    test_endpoint(BASE_URL, "/summarize", "POST", {"text": ""})
    
    # 4. Large Text Case
    long_text = "AI " * 500  # A bit long, but within limits
    test_endpoint(BASE_URL, "/summarize", "POST", {"text": long_text})

    print("\nTests completed. Ensure your server is running and GEMINI_API_KEY is set for success cases.")
