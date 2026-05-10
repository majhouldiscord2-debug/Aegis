class ToolRegistry:
    """Central registry for all deterministic tools available to AEGIS."""
    
    def __init__(self):
        self.tools = {}

    def register_tool(self, name, func, description):
        """Register a new tool with a name and description."""
        self.tools[name] = {
            "func": func,
            "description": description
        }

    def execute(self, name, args):
        """Execute a registered tool by name with provided arguments."""
        if name in self.tools:
            try:
                return self.tools[name]["func"](**args)
            except Exception as e:
                return f"Execution Error in {name}: {str(e)}"
        return f"Tool '{name}' not found in registry."

    def get_all_descriptions(self):
        """Get a list of all registered tool descriptions for context building."""
        return [f"{name}: {info['description']}" for name, info in self.tools.items()]
