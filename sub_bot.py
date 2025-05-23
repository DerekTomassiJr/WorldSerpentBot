import discord
import abc

class sub_bot(abc.ABC):
    def __init__(self):
        pass
    
    @abc.abstractmethod
    async def command_handler(self, command):
        raise NotImplementedError
    
    @property
    @abc.abstractmethod
    def client(self):
        pass

    @property
    @abc.abstractmethod
    def channel(self):
        pass

    @property
    @abc.abstractmethod
    def bot_active(self):
        pass
