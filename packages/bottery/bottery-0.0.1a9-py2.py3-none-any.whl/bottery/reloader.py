from multiprocessing import Process

import click
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FSEventHandler(FileSystemEventHandler):
    def __init__(self, target, bot_module):
        self.target = target
        self.bot_module = bot_module
        self.run()

    def on_any_event(self, event):
        if event.is_directory:
            return

        ignore_list = ['*.swp', '*.swo', '.git/']
        for ignore_pattern in ignore_list:
            if event.src_path.endswith(ignore_pattern):
                return

        self.reload()

    def run(self, reloading=False):
        target_kwargs = {
            'reloading': reloading,
            'bot_module': self.bot_module,
        }

        self.process = Process(target=self.target, kwargs=target_kwargs)
        self.process.daemon = True
        self.process.start()

    def reload(self):
        click.echo('Reloading...')
        self.process.terminate()
        self.process.join()
        self.run(reloading=True)

