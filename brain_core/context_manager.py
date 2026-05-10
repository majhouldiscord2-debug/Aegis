class ContextManager:
    """Builds and maintains the cognitive context for reasoning."""
    
    def __init__(self):
        self.context_layers = {
            "identity": "",
            "tools": [],
            "memories": [],
            "recent_history": [],
            "current_observations": [],
            "environment": {}
        }

    def set_identity(self, identity_prompt):
        """Set the core identity layer of the context."""
        self.context_layers["identity"] = identity_prompt

    def set_tools(self, tools_list):
        """Set the available tools layer."""
        self.context_layers["tools"] = tools_list

    def add_memory(self, memory_fragment):
        """Add a retrieved memory to the current context."""
        self.context_layers["memories"].append(memory_fragment)

    def add_observation(self, observation):
        """Add a new observation from tool execution or environment."""
        self.context_layers["current_observations"].append(observation)

    def build_full_context(self, max_chars=1000):
        """Assemble a flat, simple context for small models."""
        identity = self.context_layers["identity"]
        context = f"{identity}\n\n"
        
        if self.context_layers["memories"]:
            # Only include the last 2 memories to avoid distraction
            memories = "\n".join(self.context_layers["memories"][-2:])
            context += f"RECENT INFO:\n{memories}\n\n"
            
        if self.context_layers["current_observations"]:
            obs = "\n".join(self.context_layers["current_observations"][-2:])
            context += f"OBSERVATIONS:\n{obs}\n\n"
            
        return context

    def clear_short_term(self):
        """Clear observations and memories after a full reasoning cycle if needed."""
        self.context_layers["memories"] = []
        self.context_layers["current_observations"] = []
