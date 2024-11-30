import os
import requests
import argparse
from autogen import ConversableAgent, register_function
from autogen.coding import LocalCommandLineCodeExecutor
from dotenv import load_dotenv

load_dotenv()

def scraping_tool(url: str):
    response = requests.get(url, timeout=10)
    return response.text

parser = argparse.ArgumentParser(description="Scrape a URL for analysis.")
parser.add_argument("--url", type=str, required=True, help="The URL to scrape")

args = parser.parse_args()
url = args.url


llm_config_gpt35_turbo = {
    "temperature": 0.1,
    "config_list": [
        {
            "api_type": "openai",
            "model": "gpt-4o",
            "api_key": os.getenv('SECRET_KEY'),
            "cache_seed": None,
        }
    ],
}

recon_agent_sys_msg = """
You are a cybersecurity analysis agent specializing in examining HTML structures to identify input sources and endpoints that could be exploited for command injection attacks. Your task is to analyze scraped HTML and metadata to locate all potential user input points, flagging areas of interest based on risk factors.

- HTML Parsing: Extract and analyze all input fields, forms, and their attributes (e.g., name, id, type, action).
- Endpoint Identification: Identify form actions, API endpoints, and URL parameters that accept user input ADD FULL URL AS AN ENDPOINT.
- Reporting: Summarize your findings and provide a structured report with actionable insights for further investigation.
- Get all server name if you are able to find any.
"""

exploit_crafter_agent_sys_msg = """
You are the master command injector exploit crafter. Ensure to adhere to the following program:
- Use blank payload to determine the legitimate use of the application
- Ensure to only execute `whoami`.
- Include 20 different and unique command injection payloads.
- Base on endpoint, craft a payload that will return the current value of the endpoint.
- Include 10 more different and unique command injection payloads that follow this format "-t custom 'command' ".
- Make sure to include a payload that will return the current value of the endpoint.
- Return only the Python code in three backticks (```).
"""

recon_agent = ConversableAgent(
    name="recon_agent",
    llm_config=False,
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
    system_message="You are responsible for executing crafted commands securely.",
    llm_config=llm_config_gpt35_turbo,
    human_input_mode="NEVER",
    default_auto_reply="...",
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "executor": LocalCommandLineCodeExecutor(work_dir="coding", timeout=2048),
    },
)

register_function(
    scraping_tool,
    name="scraping_tool",
    caller=summerize_agent,
    executor=recon_agent,
    description="A tool to scrape a given URL.",
)

recon_chat = recon_agent.initiate_chat(
    summerize_agent,
    message=f"Can you scrape {url} for me?",
    max_turns=2,
)

scraped_content = recon_chat.chat_history[3]['content']

craft_payload = executor_agent.initiate_chat(
    exploit_crafter_agent,
    message=f"Based on this context, I need you to read the JavaScript code, and attack the relevant endpoint with command injection payloads: {recon_chat}",
    max_turns=2,
)
