import pyinotify

# Define the directory to watch
watched_dir = '.'

# Define a callback function to handle file creation events
def on_file_created(event):
    print(f"File created: {event.pathname}")

# Create a watch manager and notifier
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, default_proc_fun=on_file_created)

# Watch for IN_CREATE events (file creation) in the directory
wm.add_watch(watched_dir, pyinotify.IN_CREATE)

# Start the event loop
notifier.loop()
