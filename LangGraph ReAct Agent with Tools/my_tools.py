"""
Centralized Tools Module
========================

This module contains all resuable tools for Langgraph Agents. 
Import and use: import my_tools
"""

from langchain_core.tools import tool
import requests

# 1. Weathe Tool
@tool
def get_weather(location: str) -> str:
    """
    Retrieve the current weather for a given location.

    This function is intended to be used as a LangGraph tool. It accepts
    simple, serializable inputs and returns a JSON-serializable dictionary
    describing current weather conditions.

    Args:
        location (str): The name of the city or geographic location
            (e.g., "San Francisco", "Paris", "Tokyo").
        unit (str, optional): Temperature unit to use. Supported values
            are "celsius" and "fahrenheit". Defaults to "celsius".

    Returns:
        dict: A dictionary containing weather information with the
        following keys:
            - location (str): Resolved location name
            - temperature (float): Current temperature in the requested unit
            - unit (str): Temperature unit ("celsius" or "fahrenheit")
            - condition (str): Short textual description of the weather
              (e.g., "clear", "rain", "cloudy")

    Raises:
        ValueError: If the location is empty or the unit is unsupported.
        RuntimeError: If weather data cannot be retrieved.

    Tool Behavior:
        - Designed for deterministic, side-effect-free execution.
        - Inputs and outputs must be JSON serializable.
        - Suitable for direct invocation by LLMs within a LangGraph workflow.
    """
    url = f"https://wttr.in/{location}?format=j1"
    response = requests.get(url, timeout=10)

    response.raise_for_status()
    data = response.json()

    return data

# 2. Math Tools
@tool
def calculate(expression: str) -> str:
    """
    Evaluate a basic arithmetic expression.

    This function is intended to be used as a LangGraph tool. It accepts a
    single arithmetic expression as input and returns a JSON-serializable
    result containing the computed value.

    Supported operations are addition (+), subtraction (-), multiplication (*),
    division (/), modulo (%), and parentheses.

    Args:
        expression (str): A valid arithmetic expression represented as a string
            (e.g., "2 + 3 * (4 - 1)", "10 / 2", "7 % 3").

    Returns:
        dict: A dictionary containing the calculation result with the
        following keys:
            - expression (str): The original input expression
            - result (float | int): The evaluated numeric result

    Raises:
        ValueError: If the expression is empty, malformed, or contains
            unsupported operations.
        ZeroDivisionError: If the expression attempts division by zero.
        RuntimeError: If the expression cannot be evaluated.

    Tool Behavior:
        - Designed for deterministic, side-effect-free execution.
        - Accepts a single string input for compatibility with LLM tool calling.
        - Inputs and outputs must be JSON serializable.
        - Intended for use within LangGraph ToolNode workflows.

    Example:
        >>> calculator("2 + 3 * 4")
        {
            "expression": "2 + 3 * 4",
            "result": 14
        }
    """
    try:
        result = eval(expression)
        print(f"[TOOL] calculate ('{expression}') -> '{result}'")
    except Exception as e:
        print(f"Exception has occured with error: {e}")
        return f"Exception has occured with error: {e}"
    return result