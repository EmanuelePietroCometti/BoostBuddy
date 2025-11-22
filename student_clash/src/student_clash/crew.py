from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import FileSearchTool
from src.tools import open_food_facts_tool

@CrewBase
class BalancedLifeCrew:
    """BalancedLife crew"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    def __init__(self, agents: List[BaseAgent], tasks: List[Task]):
        self.agents = agents
        self.tasks = tasks
        self.agents_config = {
            'orchestrator': 'student_clash/agents/orchestrator.yaml',
            'trainer': 'student_clash/agents/trainer.yaml',
            'nutritionist': 'student_clash/agents/nutritionist.yaml',
        }
        self.tasks_config = {
            'fitness_task': 'student_clash/tasks/fitness_task.yaml',
            'diet_task': 'student_clash/tasks/diet_task.yaml',
            'stress_task': 'student_clash/tasks/stress_task.yaml',
        }
        self.trainer_tool = FileSearchTool(
            description="Tool for searching and retrieving precise information from corporate training log files.",
            config={
                "search_tool": {
                    "dir_path": "knowledge/fitness" 
                }
            }
        )
        self.nutritionist_tool = FileSearchTool(
            description="Tool for consulting official nutritional guidelines and food tables.",
            config={
                "search_tool": {
                    "dir_path": "knowledge/nutrition" 
                }
            }
        )
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def orchestrator(self) -> Agent:
        return Agent(
            config=self.agents_config['orchestrator'], 
            allow_delegation=True,
            memory=True,
            verbose=True
        )
    @agent
    def trainer(self) -> Agent:
        return Agent(
            config=self.agents_config['trainer'], 
            tools=[self.trainer_tool],
            memoryv=True,
            verbose=True
        )

    @agent
    def nutritionist(self) -> Agent:
        return Agent(
            config=self.agents_config['nutritionist'], 
            tools=[self.nutritionist_tool, open_food_facts_tool],
            memory=True,
            verbose=True
        )


     # leggi da tasks.yaml
    @task
    def fitness_task(self) -> Task:
        return Task(
            config=self.tasks_config['fitness_task'],
        )

    @task
    def diet_task(self) -> Task:
        return Task(
            config=self.tasks_config['diet_task'],
        )

    @task
    def stress_task(self) -> Task:
        return Task(
            config=self.tasks_config['stress_task'],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
