import os

try:
    from google.colab import userdata
    GOOGLE_API_KEY = userdata.get("GOOGLE_API_KEY")
    if GOOGLE_API_KEY is None:
        raise ValueError("GOOGLE_API_KEY not found in Colab secrets.")
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
    print("✅ Gemini API key setup complete.")
except ImportError:
    print("🔑 Authentication Error: This code expects to run in a Colab environment or requires GOOGLE_API_KEY as an OS environment variable. 'google.colab' module not found.")
except Exception as e:
    print(f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' to your Colab secrets. Details: {e}")
