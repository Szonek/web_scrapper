import sys
import logging


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
            Logger.__advanced_log("Object is none.")
            sys.exit(1)

    @staticmethod
    def is_istance(obj, class_type):
        if isinstance(obj, class_type):
            pass
        else:
            Logger.log_error(str(obj), "is not type: ", str(class_type))

    @staticmethod
    def __advanced_log(message):
        """
        Automatically log the current function details.
        !!! WORK IN PROGRESS. THIS FUNCTION SHOULB BE SOME KIND OF INLINE FUNCTION !!!
        """
        logger = logging.getLogger('root')
        err_format = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=err_format)
        logger.setLevel(logging.DEBUG)
        logger.debug(message)