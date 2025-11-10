import os
from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from google.genai import types
from IPython.core.display import display, HTML
from jupyter_server.serverapp import list_running_servers


try:
    # Attempt to use Colab secrets for GOOGLE_API_KEY
    from google.colab import userdata
    GOOGLE_API_KEY = userdata.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in Colab secrets. Please add it to the 'Secrets' tab in Colab (left panel > 🔑 icon).")
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
    print("✅ Gemini API key setup complete using Colab secrets.")
except ImportError:
    # Fallback if not in Colab or google.colab is not available
    print("⚠ Not running in Google Colab or 'google.colab' module not found. Attempting to load API key from environment variable.")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        print("🔑 Authentication Error: GOOGLE_API_KEY not found in environment variables. Please set it or add to Colab secrets.")
    else:
        os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
        print("✅ Gemini API key setup complete using environment variable.")
except Exception as e:
    # Catch any other exceptions during key retrieval (e.g., issues with userdata.get())
    print(f"🔑 Authentication Error: An unexpected error occurred while setting up GOOGLE_API_KEY. Details: {e}")

print("✅ ADK components imported successfully.")

# Gets the proxied URL in the Kaggle Notebooks environment
def get_adk_proxy_url():
    PROXY_HOST = "https://kkb-production.jupyter-proxy.kaggle.net"
    ADK_PORT = "8000"

    servers = list(list_running_servers())
    if not servers:
        raise Exception("No running Jupyter servers found.")

    baseURL = servers[0]['base_url']

    try:
        path_parts = baseURL.split('/')
        kernel = path_parts[2]
        token = path_parts[3]
    except IndexError:
        raise Exception(f"Could not parse kernel/token from base URL: {baseURL}")

    url_prefix = f"/k/{kernel}/{token}/proxy/proxy/{ADK_PORT}"
    url = f"{PROXY_HOST}{url_prefix}"

    styled_html = f"""
    <div style="padding: 15px; border: 2px solid #f0ad4e; border-radius: 8px; background-color: #fef9f0; margin: 20px 0;">
        <div style="font-family: sans-serif; margin-bottom: 12px; color: #333; font-size: 1.1em;">
            <strong>⚠ IMPORTANT: Action Required</strong>
        </div>
        <div style="font-family: sans-serif; margin-bottom: 15px; color: #333; line-height: 1.5;">
            The ADK web UI is <strong>not running yet</strong>. You must start it in the next cell.
            <ol style="margin-top: 10px; padding-left: 20px;">
                <li style="margin-bottom: 5px;"><strong>Run the next cell</strong> (the one with <code>!adk web ...</code>) to start the ADK web UI.</li>
                <li style="margin-bottom: 5px;">Wait for that cell to show it is "Running" (it will not "complete").</li>
                <li>Once it's running, <strong>return to this button</strong> and click it to open the UI.</li>
            </ol>
            <em style="font-size: 0.9em; color: #555;">(If you click the button before running the next cell, you will get a 500 error.)</em>
        </div>
        <a href='{url}' target='_blank' style="
            display: inline-block; background-color: #1a73e8; color: white; padding: 10px 20px;
            text-decoration: none; border-radius: 25px; font-family: sans-serif; font-weight: 500;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2); transition: all 0.2s ease;">
            Open ADK Web UI (after running cell below) ↗
        </a>
    </div>
    """

    display(HTML(styled_html))

    return url_prefix

print("✅ Helper functions defined.")

root_agent = Agent(
    name="helpful_assistant",
    model="gemini-2.5-flash-lite",
    description="A simple agent that can answer general questions.",
    instruction="You are a helpful assistant. Use Google Search for current info or if unsure.",
    tools=[google_search],
)

print("✅ Root Agent defined.")

runner = InMemoryRunner(agent=root_agent)

print("✅ Runner created.")
