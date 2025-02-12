from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

from dotenv import load_dotenv
import os
load_dotenv()

@tool
def check_daytime_or_nighttime_from_current_time(current_time :str)-> str: 
    """A tool that checks whether it's nighttime or daytime based on timestamp
    Args:
        current_time: A string representing current time in %Y-%m-%d %H:%M:%S format
    """
    
    # Convert the string back to a datetime object
    dt = datetime.datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
    
    # Check if the hour is between 6 and 18 
    if 6 <= dt.hour < 18:
        return "It's daytime"
    else:
        return "It's nighttime"


@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()
model = HfApiModel(
# max_tokens=2096,
# temperature=0.5,
# model_id='deepseek-ai/DeepSeek-R1-Distill-Qwen-14B',# it is possible that this model may be overloaded
# custom_role_conversions=None,
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("first_agent/prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
agent = CodeAgent(
    model=model,
    tools=[get_current_time_in_timezone, check_daytime_or_nighttime_from_current_time, DuckDuckGoSearchTool(), image_generation_tool, final_answer], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates
)


GradioUI(agent).launch()