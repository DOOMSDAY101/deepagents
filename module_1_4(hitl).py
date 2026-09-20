from langchain_core.tools import tool

from models import model

@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email to a recipient."""
    return f"Email sent to {to} with subject {subject!r}. Body: {body}"

@tool
def ask_user(question: str, choices: list[str]) -> str:
    """Ask the user a clarifying question with a fixed set of choices."""
    return f"[No response recorded for: {question}]"


from deepagents import create_deep_agent
from langgraph.checkpoint.memory import MemorySaver

SYSTEM_PROMPT = """You are a helpful assistant that can send emails.

Rules:
- If the user's request depends on a choice only they can make, call ask_user
  with the question and the list of choices before drafting anything.
- Use the ask_user response to decide what the email should say.
- Use send_email when you are ready to send.
- Keep emails concise and professional.
- Do not claim an email was sent until the tool result confirms it.
- When confirming an email was sent, quote the subject and body from the tool result, not the original request.
"""

agent = create_deep_agent(
    model=model,
    tools=[send_email, ask_user],
    system_prompt=SYSTEM_PROMPT,
     interrupt_on={
        "ask_user": {"allowed_decisions": ["respond"]},
        "send_email": {"allowed_decisions": ["approve", "edit", "reject"]},
    },
    checkpointer=MemorySaver(),
)

config = {"configurable": {"thread_id": "m1-7-hitl-demo"}}


#FOR SENDING EMAIL
# result = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "Send an email to jane@example.com saying I will be 10 minutes late.",
#             }
#         ]
#     },
#     config=config,
#     version="v2",
# )

#FOR ASKING USER
result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Email professor.weng@university.edu that I'll be late, but first "
                    "check whether I should just apologize or ask for a short extension."
                ),
            }
        ]
    },
    config=config,
    version="v2",
)
from langgraph.types import Command
import questionary


while result.interrupts:
    pending = result.interrupts[0].value
    decisions = []

    for req in pending["action_requests"]:
        if req["name"] == "ask_user":
            selected = questionary.select(
                req["args"]["question"],
                choices=req["args"]["choices"],
            ).ask()
            decisions.append({"type": "respond", "message": selected})
            
        elif req["name"] == "send_email":
            print(f"\nApproval required for {req['name']}:")
            print(req["args"])

            choice = input("\nApprove, edit, or reject? (approve/edit/reject): ").strip().lower()
            if choice in ("approve", "yes", "y"):
                decisions.append({"type": "approve"})
            elif choice in ("edit", "e"):
                edited_args = dict(req["args"])
                edited_args["body"] = input("New email body: ")

                decisions.append(
                    {
                        "type": "edit",
                        "edited_action": {"name": req["name"], "args": edited_args},
                    }
                )
            else:
                decisions.append(
                    {"type": "reject", "message": "User rejected this email draft."}
                )

    result = agent.invoke(Command(resume={"decisions": decisions}), config=config, version="v2")

for msg in result.value["messages"]:
    if hasattr(msg, "name") and msg.name == "send_email":
        print(msg.content)
        break


# from langchain_core.tools import tool
# from langchain.agents import create_agent

# from models import model


# @tool
# def send_email(to: str, subject: str, body: str) -> str:
#     """Send an email to a recipient."""
#     return f"Email sent to {to} with subject {subject!r}. Body: {body}"


# agent = create_agent(
#     model=model,
#     tools=[send_email],
# )


# result = agent.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": (
#                     "Send an email to jane@example.com "
#                     "saying I will be 10 minutes late."
#                 ),
#             }
#         ]
#     }
# )


# for message in result["messages"]:
#     message.pretty_print()
