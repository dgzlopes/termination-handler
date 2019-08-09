from abc import ABCMeta, abstractmethod


class AbstractHandler():
    """
        Abstract class representing a handler.
        All concrete handlers should implement this.
    """

    @abstractmethod
    def run(self):
        pass  # pragma: no cover
