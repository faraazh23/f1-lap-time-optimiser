#Utils
import csv

def simulate_lap(segments, ers_energy, tyre_health, drs_boost):
    lap_data = []
    total_time = 0.0
    ers_per_segment = 0.25 # MJ assumed
    max_ers_segments = int(ers_energy // ers_per_segment)

    baseline_segments =[]
    for seg in segments:
        time = seg["base_time"]
        if seg["drs_zone"] and seg["type"] == "straight":
            time *= (1 - drs_boost)
        if seg["type"] == "corner":
            time *= 1 + (1 - tyre_health) * 0.05
        baseline_segments.append(time)

    ers_gains = [(i, baseline_segments[i] * 0.15) for i in range(len(baseline_segments))]
    best_segments = sorted(ers_gains, key=lambda x: x[1], reverse=True)[:max_ers_segments]
    ers_indexes = set(i for i, _ in best_segments)

    for i, seg in enumerate(segments):
        time = seg["base_time"]
        drs = seg.get("drs_zone", False)
        is_ers_used = i in ers_indexes

        # Apply DRS
        if drs and seg["type"] == "straight":
            time *= (1 - drs_boost)

        if is_ers_used:
            time *= 0.85 # 15% time gain

        # Apply tyre degradation
        if seg["type"] == "corner":
            time *= 1 + (1 - tyre_health) * 0.05 # 5% max degradation
            tyre_health = max(0.7, tyre_health - 0.002) # 0.2% degradation per lap

        lap_data.append({
            "segment": i + 1,
            "type": seg["type"],
            "drs": drs,
            "ers_used": is_ers_used,
            "time": round(time,3),
            "tyre_health": round(tyre_health,3)
        })

        total_time += time
    print("ERS applied to segments:", ers_indexes)
    return lap_data, total_time

def export_telemetry(data, filepath):
    if not data:
        return
    
    keys = data[0].keys()
    with open(filepath, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)