from cement.core.controller import expose
from cfoundation import Controller
from app import config

class BaseController(Controller):
    class Meta:
        label = 'base'
        description = config.DESCRIPTION

    @expose(hide=True)
    def default(self):
        return
