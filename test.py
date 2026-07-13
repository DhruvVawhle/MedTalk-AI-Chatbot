import google.generativeai as genai
import time

genai.configure(api_key="AIzaSyAhH2fifCPq_gjzftEgwzeh0jJ57uBMvLk")  # Replace with actual API key

model = genai.GenerativeModel("gemini-2.0-flash")

try:
    response = model.generate_content("Hello!")
    print(response.text if hasattr(response, "text") else "API failed")
except Exception as e:
    if "429" in str(e) or "quota" in str(e).lower():
        print("❌ ERROR: API Quota Exceeded!")
        print(f"Error: {str(e)}")
        print("\nSolutions:")
        print("1. Wait for quota to reset (usually 32+ seconds)")
        print("2. Upgrade to a paid plan at https://ai.dev")
        print("3. Use a different API key with available quota")
    else:
        print(f"❌ ERROR: {str(e)}")
        raise
