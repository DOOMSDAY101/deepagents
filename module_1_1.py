from deepagents import create_deep_agent
from models import model

agent = create_deep_agent(model=model)

result = agent.invoke({"messages": [{"role": "user", "content": "what is an LLM?"}]})

print(result["messages"][-1].content)

