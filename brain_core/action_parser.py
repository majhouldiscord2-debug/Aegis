import re
import json

class ActionParser:
    """Parses model output to identify and extract deterministic tool calls."""
    
    def __init__(self):
        # Matches patterns like [TOOL: name ARGS: {"key": "value"}]
        self.tool_pattern = re.compile(r"\[TOOL:\s*(\w+)\s*ARGS:\s*({.*?})\]")

    def parse_actions(self, text):
        """Extract tool names and arguments from text output."""
        actions = []
        matches = self.tool_pattern.finditer(text)
        for match in matches:
            tool_name = match.group(1)
            args_str = match.group(2)
            try:
                args = json.loads(args_str)
                actions.append({
                    "tool": tool_name,
                    "args": args
                })
            except json.JSONDecodeError:
                continue
        return actions
