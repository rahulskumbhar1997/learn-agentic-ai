
class Memory:

    def __init__(self):
        self._conversation_history: list[dict] = []

    def add_message(self, role: str, content: str, **kwargs) -> None:
        message = {
                "role": role,
                "content": content
            }
        message.update(kwargs)
        self._conversation_history.append(message)
    
    def get_messages(self) -> list[dict]:
        return self._conversation_history

    