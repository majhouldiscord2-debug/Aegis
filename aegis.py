import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint
import os
import logging
import json

# AEGIS Core Imports
from brain_core.state_manager import StateManager
from brain_core.context_manager import ContextManager
from brain_core.reasoning_engine import ReasoningEngine
from brain_core.action_parser import ActionParser
from brain_core.reflection_engine import ReflectionEngine
from brain_core.planner import Planner
from brain_core.agent_manager import AgentManager
from memory.episodic_memory import EpisodicMemory
from memory.procedural_memory import ProceduralMemory
from memory.vector_store import VectorStore
from actions.tool_registry import ToolRegistry
from actions import filesystem_tools, app_control, browser_agent

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("brain_data/runtime.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AEGIS")

console = Console()

class AegisSystem:
    """The central orchestrator wiring all cognitive modules together."""
    
    def __init__(self):
        self.settings = self._load_settings()
        model_name = self.settings.get("model", "tinyllama")
        logger.info(f"Initializing AEGIS with model: {model_name}")
        self.state = StateManager()
        self.context = ContextManager()
        self.reasoning = ReasoningEngine(model=model_name)
        self.parser = ActionParser()
        self.episodic = EpisodicMemory()
        self.procedural = ProceduralMemory()
        self.vector_memory = VectorStore()
        self.reflection = ReflectionEngine(self.vector_memory, self.episodic)
        self.planner = Planner(self.reasoning)
        self.agents = AgentManager(self.reasoning)
        self.tools = ToolRegistry()
        
        self._register_default_tools()
        self._load_identity()

    def _load_settings(self):
        if os.path.exists("config/settings.json"):
            with open("config/settings.json", "r") as f:
                return json.load(f)
        return {}

    def _register_default_tools(self):
        self.tools.register_tool("list_files", filesystem_tools.list_files, "List files in a directory")
        self.tools.register_tool("read_file", filesystem_tools.read_file, "Read content of a file")
        self.tools.register_tool("write_file", filesystem_tools.write_file, "Write content to a file")
        self.tools.register_tool("shell", app_control.run_shell_command, "Execute a shell command")
        self.tools.register_tool("search", browser_agent.search_web, "Search the web for a query")
        self.tools.register_tool("fetch_url", browser_agent.fetch_url, "Fetch and read the text content of a URL")

    def _load_identity(self):
        if os.path.exists("identity.txt"):
            with open("identity.txt", "r") as f:
                self.context.set_identity(f.read())

    def autonomous_cycle(self, goal, skip_critic=False):
        """Execute the full autonomous cycle: Goal -> Plan -> Execute -> Reflect."""
        rprint(f"\n[bold magenta]>>> AEGIS Autonomous Goal: {goal}[/bold magenta]")
        
        # 1. Planning
        rprint("[italic cyan]Orchestrating Planner agent...[/italic cyan]")
        self.state.update_state(active_goal=goal, system_status="planning")
        
        # Give the planner a clear instruction
        plan = self.planner.generate_plan(goal, self.context.build_full_context())
        
        if not plan:
            rprint("[bold yellow]Planner failed to generate a structured JSON plan.[/bold yellow]")
            rprint("[italic]Falling back to direct execution...[/italic]")
            self.cognitive_cycle(goal, skip_critic=skip_critic)
            return

        self.state.update_state(active_plan=plan, system_status="executing")
        
        rprint(f"[bold cyan]Plan Generated:[/bold cyan]")
        for task in plan:
            rprint(f"- {task.get('description')} (Hint: {task.get('tool_hint')})")
            
        # 2. Execution of Plan
        for task in plan:
            rprint(f"\n[bold yellow]Current Task:[/bold yellow] {task.get('description')}")
            # Feed task into the cognitive cycle
            self.cognitive_cycle(task.get('description'), skip_critic=skip_critic)
            self.state.current_state["completed_tasks"].append(task)
            
        # 3. Final Reflection
        rprint(f"\n[bold green]Goal Achieved: {goal}[/bold green]")
        self.state.update_state(active_goal=None, active_plan=[], completed_tasks=[], system_status="idle")

    def cognitive_cycle(self, user_input, max_retries=2, skip_critic=False):
        """Execute one full cognitive cycle with self-healing (Critic feedback)."""
        logger.info(f"Cycle started with input: {user_input}")
        rprint(f"\n[bold blue]>>> AEGIS Cycle Starting[/bold blue]")
        
        current_retry = 0
        last_feedback = ""
        
        while current_retry <= max_retries:
            # 1. State & Memory Retrieval
            current_state = self.state.get_state()
            
            # Elite Memory Retrieval: Find semantically relevant facts (Lazy loaded)
            relevant_facts = self.vector_memory.query(user_input, limit=2)
            if relevant_facts:
                self.context.add_memory(f"RELEVANT FACTS: {relevant_facts}")
            
            # 2. Context Building
            self.context.add_memory(f"Status: {current_state['system_status']}, Cycle: {current_state['cycle_count']}")
            if last_feedback:
                self.context.add_memory(f"CRITIC FEEDBACK: {last_feedback}. Adjust your approach.")
            
            max_id_chars = 500 if self.settings.get("model") == "tinyllama" else 2000
            full_context = self.context.build_full_context(max_chars=max_id_chars)
            
            # 3. Reasoning
            response = self.reasoning.reason(full_context, user_input)
            rprint(Panel(response, title="Aegis Reasoning", border_style="cyan"))
            
            # 4. Action Parsing & Execution
            actions = self.parser.parse_actions(response)
            
            if not actions:
                # No actions requested, just a conversational response
                self.episodic.store_episode(user_input, response, [])
                break

            observations = []
            all_actions_approved = True
            
            for action in actions:
                tool_name = action["tool"]
                if tool_name in self.tools.tools:
                    # Elite Multi-Agent Check: Critic verify before execution (Unless skipped)
                    if not skip_critic:
                        approved, feedback = self.agents.verify_action(
                            f"Use {tool_name} with {action['args']}", 
                            f"Input: {user_input}"
                        )
                    else:
                        approved, feedback = True, ""
                    
                    if not approved:
                        rprint(f"[bold red]CRITIC REJECTED:[/bold red] {feedback}")
                        last_feedback = feedback
                        all_actions_approved = False
                        break # Exit action loop to retry reasoning

                    rprint(f"[bold yellow]Executing Action:[/bold yellow] {tool_name}")
                    result = self.tools.execute(tool_name, action["args"])
                    
                    # Elite Persistence: Add successful observations to Vector Memory
                    self.vector_memory.add_text(f"Task: {user_input}, Result: {result}")
                    
                    observations.append(f"Action {tool_name} Result: {result}")
                    self.context.add_observation(result)
                else:
                    logger.warning(f"Hallucinated tool call ignored: {tool_name}")
            
            if all_actions_approved:
                # 5. Logging & Persistence
                rprint("[dim]Saving episodic memory...[/dim]")
                self.episodic.store_episode(user_input, response, observations)
                self.state.increment_cycle()
                break
            else:
                current_retry += 1
                rprint(f"[italic yellow]Retrying cycle (Attempt {current_retry}/{max_retries})...[/italic yellow]")

        # 6. Reflection (Conditional)
        if self.state.get_state()["reflection_needed"]:
            rprint("[bold magenta]Starting Reflection Cycle...[/bold magenta]")
            insights = self.reflection.reflect([], observations if 'observations' in locals() else [])
            for insight in insights:
                rprint(f"- [dim]{insight}[/dim]")
            self.state.update_state(reflection_needed=False)
            
        self.context.clear_short_term()
        rprint("[bold blue]<<< Cycle Complete[/bold blue]\n")

@click.group()
def cli():
    """AEGIS Cognitive Operating System CLI."""
    pass

@cli.command()
@click.argument("goal_text")
@click.option("--fast", is_flag=True, help="Skip multi-agent checks for maximum speed.")
def goal(goal_text, fast):
    """Start an autonomous cycle to achieve a complex goal."""
    system = AegisSystem()
    system.autonomous_cycle(goal_text, skip_critic=fast)

@cli.command()
@click.argument("input_text")
@click.option("--fast", is_flag=True, help="Skip multi-agent checks for maximum speed.")
def think(input_text, fast):
    """Process a thought through the AEGIS cognitive cycle."""
    system = AegisSystem()
    system.cognitive_cycle(input_text, skip_critic=fast)

@cli.command()
def status():
    """Check the current cognitive state of AEGIS."""
    state = StateManager().get_state()
    
    table = Table(title="AEGIS System Status", border_style="green")
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="white")
    
    for key, value in state.items():
        table.add_row(key, str(value))
        
    console.print(table)

if __name__ == "__main__":
    cli()
