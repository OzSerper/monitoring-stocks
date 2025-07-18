from abc import ABC, abstractmethod
from pymongo.collection import Collection

class AbstractMongoConnection(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_collection(self, collection_name: str) -> Collection:
        pass

    @abstractmethod
    def get_by_filter(self, collection: Collection, filters):
        pass

    @abstractmethod
    def insert_doc(self, collection: Collection, **filters):
        pass

    @abstractmethod
    def close(self):
        pass
