from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.memory_manager import MemoryManager

@CrewBase
class BalancedLifeCrew:
    """BalancedLife crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # leggi da agents.yaml
    def __init__(self):
        self.memory_manager = MemoryManager()

    @agent
    def trainer_agent(self) -> Agent:
        memory = self.memory_manager.memory
        return Agent(
            config=self.agents_config['trainer_agent'], 
            verbose=True,
            memory=memory,
        )

    @agent
    def nutritionist_agent(self) -> Agent:
        memory = self.memory_manager.memory
        return Agent(
            config=self.agents_config['nutritionist_agent'],
            verbose=True,
            memory=memory,
        )

    @agent
    def stress_agent(self) -> Agent:
        memory = self.memory_manager.memory
        return Agent(
            config=self.agents_config['stress_agent'],
            verbose=True,
            memory=memory,
        )


     # leggi da tasks.yaml
    @task
    def fitness_task(self) -> Task:
        task = Task(config=self.tasks_config['fitness_task'])
        result = task.run(inputs=self.memory_manager.memory)
        self.memory_manager.update("last_workout", result)
        return task

    @task
    def diet_task(self) -> Task:
        task = Task(config=self.tasks_config['diet_task'])
        result = task.run(inputs=self.memory_manager.memory)
        self.memory_manager.update("last_meal_plan", result)
        return task

    @task
    def stress_task(self) -> Task:
        task = Task(config=self.tasks_config['stress_task'])
        result = task.run(inputs=self.memory_manager.memory)
        self.memory_manager.update("last_stress_level", result)
        return task

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
