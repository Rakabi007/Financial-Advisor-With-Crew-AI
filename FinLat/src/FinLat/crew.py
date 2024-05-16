from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool,WebsiteSearchTool, ScrapeWebsiteTool 
import os
#from langchain_openai import ChatOpenAI
#from agentops.agent import track_agent
#import agentops

# Uncomment the following line to use an example of a custom tool
# from finlat.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class FinLat():
	""" Your own AI Fianancial Advisor """
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'


def __init__(self) -> None:
	self.groq_llm = ChatGroq(temperature=0.6,groq_api_key=os.environ.get("GROQ_API_KEY"), model_name ="mixtral-8x7b-32768")
       
	     


@agent
def researcher(self) -> Agent:
		"agent responsible for reserch the topic and analyzing insight"
		return Agent(
			config=self.agents_config['researcher'],
			tools=[WebsiteSearchTool()],
			llm=self.groq_llm,
			allow_delegation=False,
			verbose=True
		)

@agent
def insights_analyst(self) -> Agent:
		"Agent reposnsible for Analyze the topic, get insight out of it"
		return Agent(
			config = self.agents_config['insights_analyst'],
			llm = self.groq_llm,
			allow_delegation = True,
			verbose = True
		)

@agent
def Copy_writer(self) -> Agent:
		"Agent responsible for Copywritting"
		return Agent(
			config=self.agents_config['Copy_writer'],
			llm=self.groq_llm,
			allow_delegation=False,
			verbose=True
		)

@task
def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher(),
			expected_output=expected_output
		)
    
@task
def insights_task(self) -> Task:
		return Task(
			config=self.tasks_config['insights_task'],
			agent=self.insights_analyst(),
			human_input=True,
			expected_output=expected_output,
		)

@task
def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.Copy_writer(),
			expected_output=expected_output,
			
		)

@crew
def crew(self) -> Crew:
		"""Creates the Finlat crew"""
		return Crew(
            agents=[
                self.researcher(),
                self.insights_analyst(),
                self.Copy_writer(),
            ],
            tasks=[
                self.research_task(),
                self.insights_task(),
                self.reporting_task(),
            ],
            process=Process.sequential,
            memory=False,
            max_rpm=5,
            verbose=2,
        )
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/