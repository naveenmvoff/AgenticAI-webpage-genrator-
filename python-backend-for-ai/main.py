from fastapi import FastAPI
from schema import EditCommand
from agents import run_agentic_editor

app = FastAPI()

@app.post("/process_command")
def process_command(data: EditCommand):
    try:
        result = run_agentic_editor(data.command)
        return {"status": "success", "response": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

