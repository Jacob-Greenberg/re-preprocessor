import abc

class Information(abc.ABC):
    @abc.abstractmethod
    def show_info(self, file_path: str) -> None:
        """
        :file_path: the path to a file which needs to be identified
        """
        pass
