from abc import ABC, abstractmethod


class MerchandiseServiceInterface(ABC):

    @classmethod
    async def get_all_merchandises(cls):
        pass

