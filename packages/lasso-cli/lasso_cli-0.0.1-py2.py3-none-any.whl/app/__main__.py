from cement.core.foundation import CementApp
from config import NAME, BANNER
from controllers import (
    BaseController,
    StorageController
)
from cfoundation import register

class App(CementApp):
    class Meta:
        label = NAME
        base_controller = BaseController
        handlers = [
            StorageController
        ]

def main():
    with App() as app:
        register(app)
        app.run()

if __name__ == '__main__':
    main()
