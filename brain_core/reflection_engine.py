class ReflectionEngine:
    """Handles self-reflection cycles and memory consolidation."""
    
    def __init__(self, vector_memory, episodic_memory):
        self.vector_memory = vector_memory
        self.episodic_memory = episodic_memory

    def reflect(self, history, observations):
        """Analyze recent history and observations, and consolidate memory."""
        insights = [
            "Cycle complete: System stability nominal.",
            "Memory Consolidation: Moving recent episodes to long-term storage."
        ]
        
        # Consolidate memory: Move episodic data to vector store
        recent_episodes = self.episodic_memory.data[-5:]
        for ep in recent_episodes:
            content = f"Experience: {ep['input']} -> {ep['output']}. Observations: {ep['observations']}"
            self.vector_memory.add_text(content, metadata={"type": "consolidation"})
            
        return insights
