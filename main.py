# Core simulation logic
from utils import simulate_lap, export_telemetry
import matplotlib.pyplot as plt
import datetime
import os

if __name__ == "__main__":
    segments = [
        {"type": "straight", "base_time": 2.5, "drs_zone": True},
        {"type": "corner", "base_time": 3.2, "drs_zone": False},
        {"type": "straight", "base_time": 1.8, "drs_zone": True},
        {"type": "corner", "base_time": 2.9, "drs_zone": False},
        {"type": "straight", "base_time": 2.0, "drs_zone": False},
    ]

    lap_data, total_time = simulate_lap(segments, ers_energy=4.0, tyre_health=0.95, drs_boost=0.03)

    # Build timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/lap_telemetry_{timestamp}.csv"

    # Export and confirm
    export_telemetry(lap_data, filename)
    print(f"✅ Telemetry saved to: {os.path.abspath(filename)}")
    print(f"🏁 Total lap time: {total_time:.2f} seconds")

    #Plot the segment times
    times = [seg["time"] for seg in lap_data]
    plt.plot(range(len(times)), times, marker='o')
    plt.title("Segment Times")
    plt.xlabel("Segment")
    plt.ylabel("Time (seconds)")
    plt.grid()
    plt.show()