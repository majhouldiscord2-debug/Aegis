import json
import os

class MemoryBase:
    """Base class for persistent memory modules."""
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return []

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(self.data, f, indent=4)

class EpisodicMemory(MemoryBase):
    """Stores specific experiences and interactions."""
    def __init__(self, storage_path="brain_data/episodic_memory.json"):
        super().__init__(storage_path)

    def store_episode(self, input_text, output_text, observations):
        self.data.append({
            "timestamp": os.path.getmtime(self.storage_path) if os.path.exists(self.storage_path) else 0,
            "input": input_text,
            "output": output_text,
            "observations": observations
        })
        self._save()

class SemanticMemory(MemoryBase):
    """Stores general facts and project knowledge."""
    def __init__(self, storage_path="brain_data/semantic_memory.json"):
        super().__init__(storage_path)

    def store_fact(self, key, value):
        self.data.append({"key": key, "value": value})
        self._save()

class ProceduralMemory(MemoryBase):
    """Stores rules and how-to procedures."""
    def __init__(self, storage_path="brain_data/procedures.json"):
        super().__init__(storage_path)

    def get_all_procedures(self):
        return self.data

class WorkingMemory:
    """Non-persistent memory for the current session."""
    def __init__(self):
        self.active_data = {}

    def set(self, key, value):
        self.active_data[key] = value

    def get(self, key):
        return self.active_data.get(key)

class VectorStore:
    """Placeholder for vector-based semantic retrieval."""
    def __init__(self):
        pass

    def query(self, text, limit=3):
        return [] # Returns top-k relevant fragments
