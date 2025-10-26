import abc

class Identifier(abc.ABC):
    @abc.abstractmethod
    def identify_file(self, file_path: str) -> float:
        """
        :file_path: the path to a file which needs to be identified
        :returns: a confidence value between 0 and 1 of the files type
                  0 means you have no idea what the file is, 1 means you
                  are certain the file is of specific type
        """
        pass