import json
import os
from datetime import datetime

class StateManager:
    """Manages the persistent state of the AEGIS cognitive system."""
    
    def __init__(self, state_file="brain_data/current_state.json"):
        self.state_file = state_file
        self.current_state = self._load_state()

    def _load_state(self):
        defaults = self._default_state()
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    loaded = json.load(f)
                    # Merge loaded state with defaults
                    for key, value in defaults.items():
                        if key not in loaded:
                            loaded[key] = value
                    return loaded
            except Exception:
                return defaults
        return defaults

    def _default_state(self):
        return {
            "last_interaction": None,
            "cycle_count": 0,
            "active_goal": None,
            "active_plan": [],
            "completed_tasks": [],
            "system_status": "initialized",
            "reflection_needed": False
        }

    def update_state(self, **kwargs):
        """Update specific fields in the current state."""
        for key, value in kwargs.items():
            self.current_state[key] = value
        self.current_state["last_interaction"] = datetime.now().isoformat()
        self._save_state()

    def increment_cycle(self):
        """Increment the cognitive cycle count."""
        self.current_state["cycle_count"] += 1
        if self.current_state["cycle_count"] % 5 == 0:
            self.current_state["reflection_needed"] = True
        self._save_state()

    def _save_state(self):
        os.makedirs(os.path.dirname(self.state_file), exist_ok=True)
        with open(self.state_file, "w") as f:
            json.dump(self.current_state, f, indent=4)
        print(f"DEBUG: Saved state to {os.path.abspath(self.state_file)}")

    def get_state(self):
        return self.current_state
