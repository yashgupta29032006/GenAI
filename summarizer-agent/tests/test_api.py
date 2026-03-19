import requests
import json
import sys

def test_summarize(url, text):
    payload = {"text": text}
    headers = {"Content-Type": "application/json"}
    
    print(f"Testing URL: {url}/summarize")
    print(f"Input Text: {text[:50]}...")
    
    try:
        response = requests.post(f"{url}/summarize", data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        result = response.json()
        print("\n--- API RESPONSE ---")
        print(json.dumps(result, indent=2))
        print("--------------------")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        if response is not None:
             print(f"Response: {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    # Change this to your live URL after deployment
    BASE_URL = "http://localhost:8080"
    
    sample_text = """
    Artificial Intelligence (AI) is transforming the world at an unprecedented pace. 
    From healthcare to finance, AI systems are being integrated into daily operations to improve efficiency and decision-making. 
    However, with these advancements come ethical considerations such as data privacy and bias in algorithms. 
    It is crucial for developers and policymakers to work together to ensure AI is used responsibly and for the benefit of all humanity.
    """
    
    test_summarize(BASE_URL, sample_text)
    
    # Test Empty Input
    print("\nTesting Empty Input...")
    test_summarize(BASE_URL, "")
