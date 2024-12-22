import json
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Watcher(FileSystemEventHandler):
    def _init_(self, log_file):
        self.log_file = log_file

    def on_modified(self, event):
        if event.is_directory:
            return
        self.log_event('modified', event.src_path)

    def on_created(self, event):
        if event.is_directory:
            return
        self.log_event('created', event.src_path)

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.log_event('deleted', event.src_path)

    def log_event(self, action, file_path):
        log_entry = {
            'action': action,
            'file': file_path,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        }
        with open(self.log_file, 'a') as log:
            log.write(json.dumps(log_entry) + '\n')
        print(f'Logged: {log_entry}')

def start_watching(path_to_watch, log_file):
    event_handler = Watcher(log_file)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if _name_ == "_main_":
    path_to_watch = '/home/muhammed/bsm/test'  # İzlenecek dizin
    log_file = '/home/muhammed/bsm/logs/changes.json'  # Log dosyasının yolu
    start_watching(path_to_watch, log_file)