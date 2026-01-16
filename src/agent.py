from a2a.server.tasks import TaskUpdater
from a2a.types import Message, TaskState, Part, TextPart
from a2a.utils import get_message_text, new_agent_text_message

from messenger import Messenger

import json
import os

from dotenv import load_dotenv
import litellm

from a2a.server.tasks import TaskUpdater
from a2a.types import DataPart, Message, Part, TaskState
from a2a.utils import get_message_text, new_agent_text_message


load_dotenv()


SYSTEM_PROMPT = (
    "You are a helpful customer service agent. "
    "Follow the policy and tool instructions provided in each message."
)


class Agent:
    def __init__(self):
        self.messenger = Messenger()
        # Initialize other state here

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        """Implement your agent logic here.

        Args:
            message: The incoming message
            updater: Report progress (update_status) and results (add_artifact)

        Use self.messenger.talk_to_agent(message, url) to call other agents.
        """
        input_text = get_message_text(message)

        # Replace this example code with your agent logic
        await updater.update_status(TaskState.working, new_agent_text_message("Thinking..."))

        self.messages.append({"role": "user", "content": input_text})

        try:
            completion = litellm.completion(
                model=self.model,
                messages=self.messages,
                temperature=0.0,
                response_format={"type": "json_object"},
            )
            assistant_content = completion.choices[0].message.content or "{}"
            assistant_json = json.loads(assistant_content)
        except Exception:
            assistant_json = {
                "name": "respond",
                "arguments": {"content": "I ran into an error processing your request."},
            }
            assistant_content = json.dumps(assistant_json)

        self.messages.append({"role": "assistant", "content": assistant_content})

        await updater.add_artifact(
            parts=[Part(root=DataPart(data=assistant_json))],
            name="Action",
        )


      