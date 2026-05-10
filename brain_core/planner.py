import json
import re

class Planner:
    """Decomposes high-level goals into a sequence of executable tasks."""
    
    def __init__(self, reasoning_engine):
        self.reasoning = reasoning_engine

    def generate_plan(self, goal, context):
        """Generate a structured plan for a given goal."""
        system_prompt = (
            "You are the AEGIS Planner. Break down the user's goal into a JSON list of tasks.\n"
            "Each task must have: 'id', 'description', and 'tool_hint'.\n"
            "Format: [{\"id\": 1, \"description\": \"...\", \"tool_hint\": \"...\"}]\n"
            "Keep it simple and deterministic."
        )
        
        response = self.reasoning.reason(system_prompt, f"Goal: {goal}")
        return self._parse_plan(response)

    def _parse_plan(self, text):
        """Extract JSON list from model response."""
        try:
            # Look for JSON-like structure in the text
            match = re.search(r"(\[.*\])", text, re.DOTALL)
            if match:
                tasks = json.loads(match.group(1))
                if isinstance(tasks, list) and len(tasks) > 0:
                    return tasks
            return [] # Return empty if no valid plan found
        except Exception:
            return []
