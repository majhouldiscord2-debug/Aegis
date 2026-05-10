class AgentRole:
    """Base class for specialized agent roles."""
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt

class AgentManager:
    """Manages different specialized agents within the AEGIS system."""
    
    def __init__(self, reasoning_engine):
        self.reasoning = reasoning_engine
        self.roles = {
            "planner": AgentRole(
                "Planner", 
                "You are the AEGIS Planner. Break down goals into tasks."
            ),
            "critic": AgentRole(
                "Critic", 
                "You are the AEGIS Critic. You MUST review the proposed action and say only 'APPROVED' or 'REJECTED: reason'. Focus on safety and logic."
            ),
            "executor": AgentRole(
                "Executor", 
                "You are the AEGIS Executor. Use tools to complete tasks."
            )
        }

    def verify_action(self, action_text, context_summary):
        """Use the Critic agent to verify an action with context."""
        critic_prompt = (
            f"{self.roles['critic'].system_prompt}\n"
            f"Context: {context_summary}\n"
            "Evaluate if the action is safe, logical, and moves the goal forward."
        )
        response = self.reasoning.reason(critic_prompt, f"Action to verify: {action_text}")
        
        is_approved = "APPROVED" in response.upper()
        # Extract feedback if not approved
        feedback = response.replace("REJECTED:", "").strip() if not is_approved else ""
        return is_approved, feedback

    def get_role_prompt(self, role_name):
        return self.roles.get(role_name).system_prompt if role_name in self.roles else ""
