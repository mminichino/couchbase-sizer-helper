##
##

import sys
import os
import inspect
import logging


class FatalError(Exception):

    def __init__(self, message):
        import traceback
        logging.debug(traceback.print_exc())
        frame = inspect.currentframe().f_back
        (filename, line, function, lines, index) = inspect.getframeinfo(frame)
        filename = os.path.basename(filename)
        logging.debug("Error: {} in {} {} at line {}: {}".format(type(self).__name__, filename, function, line, message))
        logging.error(f"{message} [{filename}:{line}]")
        sys.exit(1)


class NonFatalError(Exception):

    def __init__(self, message):
        frame = inspect.currentframe().f_back
        (filename, line, function, lines, index) = inspect.getframeinfo(frame)
        filename = os.path.basename(filename)
        self.message = "Error: {} in {} {} at line {}: {}".format(
            type(self).__name__, filename, function, line, message)
        super().__init__(self.message)


class InputFileReadError(FatalError):
    pass
