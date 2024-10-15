import importlib
import inspect
import os
from datetime import datetime

from croniter import croniter

from utils import get_trackers_selected


def process_trackers():
    print("Processing trackers...")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    trackers_selected = get_trackers_selected()
    if len(trackers_selected) == 0:
        print("No trackers selected. Exiting...")
        return
    
    trackers_dir = "trackers"
    for filename in os.listdir(trackers_dir):
        if filename.endswith(".py"):
            module_name = os.path.splitext(filename)[0]
            if module_name in trackers_selected:
                module = importlib.import_module(f"{trackers_dir}.{module_name}")
                for name in dir(module):
                    obj = getattr(module, name)
                    if inspect.isclass(obj):
                        if obj.__name__ != "Tracker":
                            instance = obj()
                            if hasattr(instance, "process") and callable(getattr(instance, "process")):
                                try:
                                    print(f"Processing {instance.name} tracker...", end=" ")
                                    instance.process()
                                    print("OK")
                                except Exception as e:
                                    print(f"ERROR! \n{e}")
    print("Finished processing trackers.")


def calculate_next_run_time():
    now = datetime.now()
    cron_expression = os.environ.get("CRON_EXPRESSION", "0 12 * * *")
    cron = croniter(cron_expression, now)
    return cron.get_next(datetime)


def main():
    print("Torrent Tracker Notifier")
    next_run_time = calculate_next_run_time()
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    process_trackers()
    next_run_time = calculate_next_run_time()
    print(f"Next run time: {next_run_time}")


if __name__ == '__main__':
   main()