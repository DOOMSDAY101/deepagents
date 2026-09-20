from models import model
from deepagents import create_deep_agent, FilesystemPermission,FilesystemMiddleware
from langchain.agents.middleware import TodoListMiddleware
from deepagents.backends import CompositeBackend, FilesystemBackend, StateBackend
from pathlib import Path

reference_dir = Path(__file__).parent / "reference"

agent = create_deep_agent(
    model=model,
    backend=CompositeBackend(
        default=StateBackend(),
        routes= {
            "/reference/": FilesystemBackend(
                root_dir= str(reference_dir),
                virtual_mode=True
            )
        }
    ),
    permissions=[
        FilesystemPermission(
            operations="write",
            paths=["/reference/**"],
            mode="deny"
        )
    ],
    middleware=[FilesystemMiddleware(tools=["read_file", "grep", "ls"])]
)