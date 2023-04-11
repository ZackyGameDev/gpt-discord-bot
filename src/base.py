from dataclasses import dataclass
from typing import Optional, List

@dataclass(frozen=True)
class Message:
    user: str
    text: Optional[str] = None

    def render(self) -> dict:
        result = {"role": self.user, "content": self.text if self.text else ""}
        return result


@dataclass
class Conversation:
    messages: List[Message]

    def prepend(self, message: Message):
        self.messages.insert(0, message)
        return self

    def render(self) -> List[dict]:
        return [message.render() for message in self.messages]


@dataclass(frozen=True)
class Config:
    name: str
    instructions: str
    example_conversations: Optional[List[Conversation]]


@dataclass(frozen=True)
class Prompt:
    header: Message
    examples: List[Conversation]
    convo: Conversation

    def render(self):
        rendered = (
            [self.header.render()]
            + [Message("system", "Example conversations:").render()]
            + sum([conversation.render() for conversation in self.examples], [])
            + [Message("system", "Current conversation:").render()]
            + self.convo.render()
        )
        if not self.examples:
            del rendered[1] # Remove the "Example Conversation: system thing if no examples"
        
        return rendered
