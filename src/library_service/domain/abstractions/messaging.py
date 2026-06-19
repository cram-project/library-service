from typing import Protocol, runtime_checkable


@runtime_checkable
class IMessagePublisher(Protocol):
    async def publish(self, message: str):
        pass