import os


def check_ratio(ratio: str, min_ratio: str) -> str:
    if ratio == "∞":
        return ">"
    ratio = float(ratio)
    min_ratio = float(min_ratio)
    if ratio > min_ratio:
        return ">"
    elif ratio == min_ratio:
        return "="
    else:
        return "<"


def get_trackers_selected():
    trackers_selected = os.environ.get("TRACKERS")
    if not trackers_selected:
        return []
    trackers_selected = trackers_selected.split(',')
    trackers_selected = [tracker.lower() for tracker in trackers_selected]
    return trackers_selected