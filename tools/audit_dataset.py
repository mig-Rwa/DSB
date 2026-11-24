"""Read-only signature audit of the supplied CIU archive after extraction.

This is a data inspection utility, not an STA implementation or preprocessing
pipeline. Reports omit demographic values, participant images and trajectories.
All four signature ranges form one pool per subject. No emotion labels are used.
Requires Pillow to verify and decode each selected signature JPEG.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import zlib

from PIL import Image


def summary(values):
    return {"min": min(values), "median": statistics.median(values),
            "max": max(values)} if values else {}


def is_signature(path: Path):
    match = re.fullmatch(r"EA_HW(\d+)", path.stem)
    return bool(match and any(low <= int(match.group(1)) <= high
                             for low, high in [(4, 18), (20, 34), (36, 50), (52, 66)]))


def audit(root: Path, inventory: Path | None):
    files = sorted(p for p in root.rglob("*") if p.is_file())
    subjects = sorted(p.name for p in root.iterdir() if p.is_dir())
    expected_entries = {}
    if inventory:
        for entry in json.loads(inventory.read_text(encoding="utf-8"))["entries"]:
            if "D" not in entry.get("Attributes", ""):
                expected_entries[entry["Path"].replace("\\", "/")] = entry

    extensions, sizes = Counter(), Counter()
    dat_values, subject_keys, subject_bodies = Counter(), Counter(), Counter()
    header_keys, columns_seen, technical = Counter(), Counter(), defaultdict(Counter)
    recording_keys = defaultdict(list)
    samples_per_subject = Counter()
    excluded_files = Counter()
    packet_counts, time_spans = defaultdict(list), defaultdict(list)
    dt_by_type = defaultdict(Counter)
    ranges = {}
    categorical = defaultdict(Counter)
    packet_total, contacts, pressure_positive = Counter(), Counter(), Counter()
    zero_pressure_contact, positive_pressure_hover = Counter(), Counter()
    time_errors, malformed_rows, nonfinite_rows = [], [], []
    empty_recordings, degenerate_contact, identifier_mismatches = [], [], []
    bad_images, image_sizes, image_modes = [], [], Counter()
    crc_errors, size_errors, unexpected_files = [], [], []
    hashes = defaultdict(list)
    subject_id_checks = Counter()
    date_formats, comments_seen = Counter(), Counter()
    signature_contact_counts = []
    technical_keys = {"Protocol", "Capture Device", "Freq", "Axes Unit",
                      "X_Origin", "Y_Origin", "X_Extent", "Y_Extent",
                      "X_Res", "Y_Res", "NP_Max", "Test Group"}
    seen_subject = set()

    for path in files:
        rel = path.relative_to(root).as_posix()
        subject = rel.split("/")[0]
        if subject not in seen_subject:
            seen_subject.add(subject)
            if len(seen_subject) % 20 == 0:
                print(f"Inspecting subject {len(seen_subject)}/{len(subjects)}", flush=True)
        raw = path.read_bytes()
        extensions[path.suffix.lower()] += 1
        sizes[path.suffix.lower()] += len(raw)
        if path.suffix.lower() in {".tst", ".jpg"} and is_signature(path):
            hashes[(path.suffix.lower(), hashlib.sha256(raw).hexdigest())].append(rel)
        if expected_entries:
            entry = expected_entries.get(root.name + "/" + rel)
            if entry is None:
                unexpected_files.append(rel)
            else:
                if len(raw) != int(entry["Size"]):
                    size_errors.append(rel)
                if f"{zlib.crc32(raw) & 0xffffffff:08X}" != entry["CRC"]:
                    crc_errors.append(rel)

        if path.name == "subject.txt":
            for line in raw.decode("latin-1").splitlines():
                if line.startswith("#") and ":" in line:
                    key, value = line[1:].split(":", 1)
                    value = value.strip()
                    subject_keys[key] += 1
                    if key in {"ID", "Hospital ID"}:
                        subject_id_checks[key + (" matches directory" if value == subject else " differs from directory")] += 1
                    if key == "Date of Birth":
                        date_formats[re.sub(r"\d", "d", value)] += 1
                elif line and not line.startswith("#"):
                    subject_bodies[line if line in {"<", ">", "No Comment"} else "non-default text (withheld)"] += 1
        elif path.suffix.lower() == ".dat":
            value = raw.strip()
            dat_values[value.decode("ascii") if value in {b"True", b"False"} else "other content (withheld)"] += 1
        elif path.suffix.lower() == ".jpg":
            if not is_signature(path):
                excluded_files["non_signature_or_aborted_jpg"] += 1
                continue
            try:
                with Image.open(path) as img:
                    img.verify()
                with Image.open(path) as img:
                    img.load()
                    image_sizes.append(img.size)
                    image_modes[img.mode] += 1
            except Exception as exc:
                bad_images.append({"path": rel, "error_type": type(exc).__name__})
        elif path.suffix.lower() == ".tst":
            if not is_signature(path):
                excluded_files["non_signature_tst"] += 1
                continue
            match = re.fullmatch(r"EA_HW(\d+)", path.stem)
            number = int(match.group(1))
            kind = "signature"
            samples_per_subject[subject] += 1
            recording_keys[(subject, number)].append(rel)
            columns, in_data, row_count = None, False, 0
            first_time = previous_time = None
            contact_x, contact_y = [], []
            for line_number, line in enumerate(raw.decode("latin-1").splitlines(), 1):
                if not line.strip():
                    continue
                if line.startswith("#Ti\t"):
                    columns = line[1:].split("\t")
                    columns_seen[" ".join(columns)] += 1
                elif line.startswith("#Data:"):
                    in_data = True
                elif not in_data:
                    if line.startswith("#") and ":" in line:
                        key, value = line[1:].split(":", 1)
                        value = value.strip()
                        header_keys[key] += 1
                        if key in technical_keys:
                            technical[key][value] += 1
                        if key == "ID" and value != subject:
                            identifier_mismatches.append(rel)
                    elif line and not line.startswith("#"):
                        comments_seen[line if line in {"<", ">", "No Comment"} else "non-default text (withheld)"] += 1
                else:
                    if line.startswith("#"):
                        malformed_rows.append({"path": rel, "line": line_number, "reason": "unexpected footer"})
                        continue
                    parts = line.split("\t")
                    if columns is None or len(parts) != len(columns):
                        malformed_rows.append({"path": rel, "line": line_number, "reason": "wrong column count"})
                        continue
                    try:
                        values = [float(value) for value in parts]
                    except ValueError:
                        malformed_rows.append({"path": rel, "line": line_number, "reason": "nonnumeric packet"})
                        continue
                    if not all(math.isfinite(value) for value in values):
                        nonfinite_rows.append({"path": rel, "line": line_number})
                        continue
                    row = dict(zip(columns, values))
                    for key, value in row.items():
                        bounds = ranges.setdefault(key, [value, value])
                        bounds[0], bounds[1] = min(bounds[0], value), max(bounds[1], value)
                        if key in {"TP", "St", "Cu", "Co", "Bu", "Tw", "Pi", "Ro", "Ya"}:
                            categorical[key][value] += 1
                    time = row["Ti"]
                    if first_time is None:
                        first_time = time
                    if previous_time is not None:
                        dt = time - previous_time
                        dt_by_type[kind][dt] += 1
                        if dt <= 0:
                            time_errors.append({"path": rel, "line": line_number, "delta": dt})
                    previous_time = time
                    down = bool(int(row["Bu"]) & 1)
                    positive = row["NP"] > 0
                    contacts[kind] += int(down)
                    pressure_positive[kind] += int(positive)
                    zero_pressure_contact[kind] += int(down and not positive)
                    positive_pressure_hover[kind] += int(positive and not down)
                    if down:
                        contact_x.append(row["X"])
                        contact_y.append(row["Y"])
                    row_count += 1
            packet_counts[kind].append(row_count)
            packet_total[kind] += row_count
            if row_count == 0:
                empty_recordings.append(rel)
            else:
                time_spans[kind].append(previous_time - first_time)
            if kind == "signature":
                signature_contact_counts.append(len(contact_x))
            if len(contact_x) < 2 or max(max(contact_x)-min(contact_x), max(contact_y)-min(contact_y)) == 0:
                degenerate_contact.append(rel)

    tst_stems = {p.relative_to(root).with_suffix("").as_posix() for p in files if p.suffix.lower() == ".tst" and is_signature(p)}
    jpg_stems = {p.relative_to(root).with_suffix("").as_posix() for p in files if p.suffix.lower() == ".jpg" and is_signature(p)}
    duplicate_recordings = {f"{subject}/sample-{number}": paths
                            for (subject, number), paths in recording_keys.items() if len(paths) > 1}
    return {
        "scope": "Signature-only analysis; 60 samples pooled per subject; no emotion grouping, preprocessing or STA execution",
        "subject_count": len(subjects),
        "missing_ids_1_to_142": [f"E{i:03d}" for i in range(1, 143) if f"E{i:03d}" not in subjects],
        "file_count": len(files), "file_counts_by_extension": dict(extensions),
        "bytes_by_extension": dict(sizes), "total_bytes": sum(sizes.values()),
        "extraction_integrity": {"archive_entries_checked": len(expected_entries), "crc_mismatches": crc_errors,
                                 "size_mismatches": size_errors, "unexpected_files": unexpected_files,
                                 "missing_files": sorted(set(expected_entries) - {root.name + '/' + p.relative_to(root).as_posix() for p in files})},
        "signature_recordings": sum(samples_per_subject.values()),
        "unique_subject_sample_pairs": len(recording_keys),
        "excluded_from_signature_analysis": dict(excluded_files),
        "duplicate_subject_sample_pairs": duplicate_recordings,
        "per_subject_signature_counts": dict(sorted(samples_per_subject.items())),
        "same_content_tst_groups": [paths for (suffix, digest), paths in hashes.items() if suffix == ".tst" and len(paths) > 1],
        "same_content_jpg_group_count": sum(suffix == ".jpg" and len(paths) > 1 for (suffix, digest), paths in hashes.items()),
        "jpg_without_tst": sorted(jpg_stems-tst_stems), "tst_without_jpg": sorted(tst_stems-jpg_stems),
        "subject_header_keys": dict(subject_keys), "subject_id_checks": dict(subject_id_checks),
        "birth_date_shapes_only": dict(date_formats), "subject_body_categories": dict(subject_bodies),
        "recording_header_keys": dict(header_keys), "recording_comment_categories": dict(comments_seen),
        "technical_header_values": dict(technical), "packet_column_layouts": dict(columns_seen),
        "packet_totals": dict(packet_total),
        "packets_per_recording": {kind: summary(values) for kind, values in packet_counts.items()},
        "recording_span_raw_ticks": {kind: summary(values) for kind, values in time_spans.items()},
        "numeric_column_ranges": ranges, "categorical_packet_values": dict(categorical),
        "timestamp_deltas": {kind: {"most_common": counts.most_common(15), "distinct": len(counts),
                                   "min": min(counts), "max": max(counts)} for kind, counts in dt_by_type.items()},
        "contact_bit_packets": dict(contacts), "positive_pressure_packets": dict(pressure_positive),
        "contact_bit_with_zero_pressure": dict(zero_pressure_contact),
        "positive_pressure_without_contact_bit": dict(positive_pressure_hover),
        "signature_contact_points": summary(signature_contact_counts),
        "packet_validation": {"malformed_rows": malformed_rows, "nonfinite_rows": nonfinite_rows,
                              "nonincreasing_timestamps": time_errors, "empty_recordings": empty_recordings,
                              "degenerate_contact_geometry": degenerate_contact,
                              "header_id_mismatches": sorted(set(identifier_mismatches))},
        "images": {"fully_decoded": len(image_sizes), "errors": bad_images,
                   "width": summary([w for w, h in image_sizes]), "height": summary([h for w, h in image_sizes]),
                   "modes": dict(image_modes)},
        "dat_contents": dict(dat_values),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("datasets/extracted/Database"))
    parser.add_argument("--inventory", type=Path, help="Optional local 7-Zip inventory JSON for CRC checks")
    parser.add_argument("--output", type=Path, default=Path(".local-analysis/audit.json"))
    args = parser.parse_args()
    report = audit(args.data, args.inventory)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Audited {report['file_count']} files and {sum(report['packet_totals'].values())} packets.")
    print(f"Report: {args.output}")
