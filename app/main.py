import importlib
import inspect
import os
import argparse
from datetime import datetime

from croniter import croniter

from utils import get_trackers_selected


def process_trackers(verbose=False):
    print("Processing trackers...")
    trackers_selected = get_trackers_selected()
    if len(trackers_selected) == 0:
        print("No trackers selected. Exiting...")
        return

    if verbose:
        print(f"Selected trackers: {trackers_selected}")

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
                                    if verbose:
                                        print(f"Processing {instance.name} tracker ({instance.abbr})...")
                                    else:
                                        print(f"Processing {instance.name} tracker...")
                                    instance.process()
                                    print("OK")
                                except Exception as e:
                                    print(f"ERROR! \n{e}")
                                    if verbose:
                                        import traceback
                                        traceback.print_exc()
    print("Finished processing trackers.")


def calculate_next_run_time():
    now = datetime.now()
    cron_expression = os.environ.get("CRON_EXPRESSION", "0 12 * * *")
    cron = croniter(cron_expression, now)
    return cron.get_next(datetime)


def main():
    parser = argparse.ArgumentParser(description="Torrent Tracker Notifier")
    parser.add_argument(
        "-t", "--trackers",
        type=str,
        help="Comma-separated list of trackers to process (overrides TRACKERS environment variable)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Process trackers but do not send notifications"
    )

    args = parser.parse_args()

    # If trackers are specified via command line, set the environment variable
    if args.trackers:
        os.environ["TRACKERS"] = args.trackers

    print("Torrent Tracker Notifier")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if args.verbose:
        print(f"TRACKERS environment variable: {os.environ.get('TRACKERS', 'Not set')}")

    process_trackers(verbose=args.verbose)
    next_run_time = calculate_next_run_time()
    print(f"Next run time: {next_run_time}")


if __name__ == '__main__':
   main()