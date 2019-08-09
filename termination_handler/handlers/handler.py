from abc import ABCMeta   # noqa: F401
from abc import abstractmethod   # noqa: F401


class AbstractHandler():
    """
        Abstract class representing a handler.
        All concrete handlers should implement this.
    """

    @abstractmethod
    def run(self):
        pass  # pragma: no cover
