# The TodoListMiddleware adds a todo list tool that the ai agent use to write todos on how to go about a project.
# Then it updats the state: pending -> in_progress -> completed
from models import model
from langchain.agents.middleware import TodoListMiddleware

from langchain.agents import create_agent

agent = create_agent(model=model, middleware=[TodoListMiddleware()])
# Agent now has access to write_todos tool and todo state tracking
result =  agent.invoke({"messages": "Help me refactor my codebase"})

print(result["todos"])