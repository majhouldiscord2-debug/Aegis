# AEGIS AI - Desktop Application

## What's Included

- **FastAPI Backend**: Modern Python API server
- **Beautiful UI**: Modern gradient design chat interface
- **PyInstaller Packaging**: Build everything into a single .exe
- **Two Modes**: Think Mode (single cycle) and Goal Mode (autonomous planning)

## Quick Start

### Development Mode

1. **Install Dependencies** (already done):
   ```
   pip install fastapi uvicorn pyinstaller
   ```

2. **Start the App**:
   - Double-click `start.bat`, or
   - Run: `python app.py`
   - Then open: `http://localhost:8000`

### Build .exe File

1. **Build the Executable**:
   - Double-click `build.bat`
   - Wait for the build to complete

2. **Run the .exe**:
   - Go to the `dist` folder
   - Run `AEGIS_AI.exe`

## Features

### UI Features
- Real-time status monitoring
- Chat interface with terminal output
- Two operational modes (Think/Goal)
- Beautiful gradient design
- Responsive layout

### AI Features
- Cognitive reasoning engine
- Tool execution (filesystem, shell, web search)
- Memory system (episodic, semantic, vector)
- Reflection and self-critique
- Autonomous goal planning

## File Structure

```
Aegis AI/
├── app.py              # FastAPI backend
├── aegis.py            # Core AI system
├── aegis.spec          # PyInstaller config
├── build.bat           # Build script
├── start.bat           # Startup script
├── ui/
│   └── index.html      # Web UI
├── brain_core/         # AI modules
├── brain_data/         # Memory storage
├── actions/            # Tool registry
└── memory/             # Memory systems
```

## Troubleshooting

- If the UI doesn't load, make sure port 8000 is available
- Check `brain_data/runtime.log` for detailed logs
- The first build may take several minutes

## Notes

- The UI uses vanilla JavaScript (no React) for easier packaging
- All data files are included in the .exe
- The app runs a local web server on port 8000
