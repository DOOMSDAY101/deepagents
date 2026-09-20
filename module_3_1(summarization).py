# deep agents already does this automatically. this is just to customise it to the way we want
from deepagents import create_deep_agent
from deepagents.backends import StateBackend
from deepagents.middleware.summarization import (
    SummarizationMiddleware,
)
from models import model

backend = StateBackend()

summarization = SummarizationMiddleware(
    model=model,
    backend=backend,

    # Start summarizing at 85% of context window
    trigger=("fraction", 0.85),

    # Keep the most recent 10% of the conversation
    keep=("fraction", 0.10),
)

agent = create_deep_agent(
    model=model,
    backend=backend,
    middleware=[
        summarization,
    ],
)
