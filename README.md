# 🛡️ Aegis AI

A beautiful, modern AI assistant with cognitive architecture, built with Python, FastAPI, and a stunning UI.

## ✨ Features

### 🎨 Beautiful UI
- Modern, clean black theme
- Sidebar navigation with Recent chats
- Welcome screen with animated logo
- Smooth animations and transitions
- Responsive design
- Think/Goal mode toggle
- Terminal output display

### 🧠 AI Features
- Cognitive reasoning engine
- Autonomous goal planning
- Memory system (episodic, semantic, vector)
- Reflection and self-critique
- Tool execution (filesystem, shell, web search)
- Multiple AI models support

### 🚀 Deployment Options
- **Local Development**: Run on your machine
- **Desktop App**: Package as .exe with PyInstaller
- **Web App**: Hosted version coming soon

## 📦 Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/majhouldiscord2-debug/Aegis.git
   cd Aegis
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   - Navigate to: `http://127.0.0.1:8000`
   - The app will automatically open in your default browser

## 🎯 Usage

### Think Mode
Single cognitive cycle for quick tasks and conversations.

### Goal Mode
Autonomous planning and execution of complex goals.

### Chat History
All conversations are automatically saved to your browser's localStorage and appear in the "Recents" section.

## 📁 Project Structure

```
Aegis/
├── app.py                 # FastAPI backend server
├── aegis.py               # Core AI system
├── ui/
│   └── index.html         # Beautiful web UI
├── brain_core/            # AI cognitive modules
├── actions/               # Tool registry
├── memory/                # Memory systems
├── brain_data/            # Memory storage
├── config/                # Configuration files
├── personality/           # AI personality settings
├── requirements.txt       # Python dependencies
├── aegis.spec            # PyInstaller config
├── build.bat             # Windows build script
├── start.bat             # Windows startup script
└── README.md             # This file
```

## 🛠️ Building the .exe

To build a standalone Windows executable:

1. Double-click `build.bat`
2. Wait for the build to complete
3. Find `AEGIS_AI.exe` in the `dist` folder

## 🌐 Cloudflare Pages Hosting

**Important Note**: Cloudflare Pages hosts static websites only. The current Aegis AI requires a Python backend server.

### Options for Cloudflare Pages:

1. **Static Demo Version** (coming soon)
   - A demo version with static UI only
   - No AI functionality, but shows the interface

2. **Full Deployment**
   - Use a backend hosting service (Render, PythonAnywhere, etc.)
   - Connect Cloudflare Pages to your backend API

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Fork the repository
- Create a feature branch
- Submit a Pull Request

## 📄 License

MIT License - feel free to use this project!

## 👤 Author

**Majhoul Discord**
- GitHub: [@majhouldiscord2-debug](https://github.com/majhouldiscord2-debug)

## 🙏 Acknowledgments

Built with ❤️ using:
- FastAPI
- Python
- Pure CSS & Emojis (no external libraries needed!)
