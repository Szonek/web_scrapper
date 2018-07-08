import sys
class Logger:
    """
    Error logger.
    Further implementations will have more advanced logging.
    """

    @staticmethod
    def log_error(e):
        """
        Prints content of the e.
        :param e: Content to print.
        """
        print(e)
        pass

    @staticmethod
    def CHECK_IF_NONE(e):
        if e is None:
            sys.exit(1)

