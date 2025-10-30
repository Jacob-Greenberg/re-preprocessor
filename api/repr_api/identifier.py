import abc

class Identifier(abc.ABC):
    @abc.abstractmethod
    def identify_file(self, file_path: str) -> tuple[float, list[str]]:
        """
        :file_path: the path to a file which needs to be identified
        :returns: a tuple with a float representing the confidence value
                  and a list of file types

                  Confidence is a float between 0 and 1. If a file is totally
                  unknown the confidence is 0 and a value of 1 means the file
                  is certainly this type.

                  The list of strings is the type of file. It can be a single string
                  or can be multiple in case the file format has synonym file types 
                  (i.e gzip and gnuzip are the same format).
        """
        pass
