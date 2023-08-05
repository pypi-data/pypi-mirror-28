from cement.core.controller import expose
from cfoundation import Controller
from os import path

class StorageController(Controller):
    class Meta:
        label = 'remount'
        description = 'Remount storage'
        stacked_on = 'base'
        stacked_type = 'nested'
        arguments = [
            (['-m', '--mount'], {
                'action': 'store',
                'dest': 'mount',
                'help': 'mount path',
                'required': False
            }),
            (['-p', '--project'], {
                'action': 'store',
                'dest': 'project',
                'help': 'project name',
                'required': False
            }),
            (['extra_arguments'], {
                'action': 'store',
                'nargs': '*'
            })
        ]

    @expose(hide=True)
    def default(self):
        s = self.app.services
        prompt = s.helper_service.prompt
        pargs = self.app.pargs
        mount = pargs.mount
        if not mount:
            if len(pargs.extra_arguments) > 0:
                mount = pargs.extra_arguments[0]
            else:
                mount = prompt('mount')
        project = pargs.project
        mount = path.abspath(mount)
        return s.storage_service.remount(mount, projectName=project)
