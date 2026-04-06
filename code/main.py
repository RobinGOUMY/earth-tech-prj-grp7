from screen import launcher
from codecarbon import EmissionsTracker


# ============================================================
# ENTRY POINT
# ============================================================


# Initialize the tracker
tracker = EmissionsTracker()
tracker.start()

try:
    # Code to start the launcher
    launcher()
finally:
    # Important: ensures the tracker stops even if the game crashes
    emissions: float = tracker.stop()
    print(f"CO2 emissions for this session: {emissions:.6f} kg")