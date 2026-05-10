from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
import os
import sys

app = FastAPI(title="AEGIS AI Desktop App")

# Global system instance - will be initialized lazily
aegis_system = None

class ChatRequest(BaseModel):
    message: str
    mode: str = "think"

class SystemStatus(BaseModel):
    status: str
    cycle_count: int

def get_aegis_system():
    global aegis_system
    if aegis_system is None:
        print("Initializing AEGIS Brain...")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from aegis import AegisSystem
        aegis_system = AegisSystem()
        print("AEGIS Initialized.")
    return aegis_system

@app.get("/")
async def read_root():
    """Serve the main UI page."""
    from fastapi.responses import Response
    index_path = os.path.join(os.path.dirname(__file__), "ui", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        return Response(content=content, media_type="text/html", headers={"Cache-Control": "no-cache, no-store, must-revalidate", "Pragma": "no-cache", "Expires": "0"})
    return {"AEGIS": "Online - Create a UI folder with index.html"}

@app.get("/api/status")
async def get_status():
    """Get the current system status."""
    try:
        system = get_aegis_system()
        state = system.state.get_state()
        return SystemStatus(
            status=state["system_status"],
            cycle_count=state["cycle_count"]
        )
    except Exception as e:
        return SystemStatus(
            status="Initializing...",
            cycle_count=0
        )

@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Send a message to AEGIS and get a response."""
    try:
        system = get_aegis_system()
        
        # Capture output (we'll redirect stdout/stderr later)
        import io
        from contextlib import redirect_stdout
        
        f = io.StringIO()
        with redirect_stdout(f):
            if request.mode == "goal":
                system.autonomous_cycle(request.message, skip_critic=True)
            else:
                system.cognitive_cycle(request.message, skip_critic=True)
        
        output = f.getvalue()
        
        return {
            "success": True,
            "output": output
        }
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    import webbrowser
    import threading
    import time
    
    def open_browser():
        time.sleep(1.5)
        webbrowser.open("http://localhost:8000")
    
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host="127.0.0.1", port=8000)
