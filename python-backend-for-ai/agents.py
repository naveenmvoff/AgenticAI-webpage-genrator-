import os, re
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
gemini = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Shared in-memory session state
session_state = {
    "current": None,
    "history": [],
    "preset_colors": {
        "black": "#000000",
        "red": "#ff0000",
        "yellow": "#ffff00"
    }
}

# 1️⃣ NL Command Parser Agent
def parse_nl_command(command: str):
    prompt = PromptTemplate.from_template("""
    Given a user's instruction, convert it into an action plan with:
    - action: what to do (e.g., create_layout, update_css, undo)
    - target: selector like header/body/footer
    - props: any CSS styles if present

    Example: "Make the header bold and red"
    Output:
    {"action": "update_css", "target": "header", "props": {"fontWeight": "bold", "color": "red"}}

    Instruction: {command}
    """)
    try:
        response = gemini.invoke(prompt.format(command=command))
        return eval(response.content.strip())
    except:
        return {"action": "unknown", "target": "", "props": {}}

# 2️⃣ RAG-Enabled Tool Router Agent
def tool_router(parsed):
    action = parsed.get("action", "")
    if action == "create_layout":
        return "generate_layout"
    elif action == "update_css":
        return "apply_css"
    elif action == "undo":
        return "undo_change"
    else:
        return "parse_fallback"

# 3️⃣ Change Executor: Tool - Website Generator
def generate_layout(_: str):
    layout_html = "<html><body><h1>Welcome to Shoe Store</h1><p>Best shoes here.</p></body></html>"
    css = {
        "backgroundColor": session_state["preset_colors"]["black"],
        "color": session_state["preset_colors"]["red"]
    }
    result = {"layout": layout_html, "props": css}
    session_state["history"].append(session_state["current"])
    session_state["current"] = result
    return result

# 4️⃣ Change Executor: Tool - CSS Modifier
def apply_css(command: str):
    parsed = parse_nl_command(command)
    colors = parsed.get("props", {})
    if session_state["current"] is None:
        session_state["current"] = {"layout": "<html><body></body></html>", "props": {}}
    updated = session_state["current"].copy()
    updated["props"].update(colors)
    session_state["history"].append(session_state["current"])
    session_state["current"] = updated
    return updated

# 5️⃣ Undo/Redo Tool
def undo_change(_: str):
    if session_state["history"]:
        session_state["current"] = session_state["history"].pop()
        return session_state["current"]
    return {"error": "No previous state"}

# 6️⃣ Fallback Tool
def parse_fallback(command: str):
    return parse_nl_command(command)

# Register tools
tools = [
    Tool(name="generate_layout", func=generate_layout, description="Create a new layout based on prompt"),
    Tool(name="apply_css", func=apply_css, description="Apply new CSS styles"),
    Tool(name="undo_change", func=undo_change, description="Undo last website change"),
    Tool(name="parse_fallback", func=parse_fallback, description="Fallback NL parsing tool")
]

agent = initialize_agent(
    tools=tools,
    llm=gemini,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

# 🔁 Final Routing
def run_agentic_editor(command: str):
    parsed = parse_nl_command(command)
    tool_name = tool_router(parsed)
    result = agent.run(f"use {tool_name} to process: {command}")
    return {
        "parsed": parsed,
        "tool_used": tool_name,
        "current_state": session_state["current"],
        "result": result
    }


# import os
# import re
# from dotenv import load_dotenv
# from langchain_core.prompts import PromptTemplate
# from langchain_google_genai import ChatGoogleGenerativeAI

# load_dotenv()
# gemini_api_key = os.getenv("GOOGLE_API_KEY")

# # Initialize Gemini
# gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key)

# # In-memory session state
# session_state = {
#     "current": None,
#     "history": [],
#     "intent_history": [],
#     "preset_colors": {
#         "black": "#000000",
#         "red": "#ff0000",
#         "yellow": "#ffff00"
#     }
# }

# # Layout generator
# def generate_layout(theme_colors: dict = None):
#     layout_html = "<html><body><h1>Welcome to the Shoe Store</h1><p>Best shoes in town!</p></body></html>"
#     css = theme_colors or {
#         "backgroundColor": "#000000",
#         "color": "#ff0000"
#     }
#     return {"layout": layout_html, "css": css}

# # Main command parser
# def parse_command(command: str) -> dict:
#     command = command.lower()
#     session_state["intent_history"].append(command)

#     if "previous" in command or "undo" in command:
#         if session_state["history"]:
#             session_state["current"] = session_state["history"][-1]
#             return {"action": "reverted", "data": session_state["current"]}
#         return {"error": "No previous state found"}

#     elif "change the layout" in command:
#         layout = generate_layout(session_state.get("current", {}).get("props"))
#         session_state["history"].append(session_state["current"])
#         session_state["current"] = {"selector": "body", "props": layout["css"], "layout": layout["layout"]}
#         return {"action": "layout_updated", "data": session_state["current"]}

#     elif "color" in command:
#         colors = re.findall(r"(black|red|yellow)", command)
#         css_props = {}
#         if colors:
#             if len(colors) == 2:
#                 css_props = {
#                     "backgroundColor": session_state["preset_colors"][colors[0]],
#                     "color": session_state["preset_colors"][colors[1]]
#                 }
#             else:
#                 css_props = {"color": session_state["preset_colors"][colors[0]]}

#         if session_state["current"]:
#             session_state["history"].append(session_state["current"])

#         session_state["current"] = {"selector": "body", "props": css_props}
#         return {"action": "color_updated", "data": session_state["current"]}

#     # Default fallback: use Gemini to parse generic instructions
#     prompt = PromptTemplate.from_template("""
#     Convert this user instruction into a structured object with 'selector' and 'props'.

#     Example Input: "Make the header bold and blue"
#     Output Format: {{
#         "selector": "header",
#         "props": {{
#             "color": "blue",
#             "fontWeight": "bold"
#         }}
#     }}

#     Now convert: {command}
#     """)

#     result = gemini.invoke(prompt.format(command=command))
#     try:
#         parsed = eval(result.content)
#         if session_state["current"]:
#             session_state["history"].append(session_state["current"])
#         session_state["current"] = parsed
#         return {"action": "parsed", "data": parsed}
#     except:
#         return {"error": "Failed to parse command"}
