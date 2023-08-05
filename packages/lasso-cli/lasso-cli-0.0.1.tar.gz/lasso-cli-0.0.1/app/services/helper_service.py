from builtins import input
from cfoundation import Service
from getpass import getpass

class HelperService(Service):

    def prompt(self, name, default=None, private=False):
        message = name + ': '
        if default:
            message = name + ' (\' + default + \'): '
        result = None
        if private:
            result = getpass(message)
        else:
            result = input(message)
        if result and len(result) > 0:
            return result
        return default
