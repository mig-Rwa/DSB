"""Check signature packet duplication and capture-header labels without editing data.

Select the same signature filenames as audit_dataset.py. All selected signatures
are pooled by directory identity; there are no emotion labels or task groups.
The report contains identifiers and conflicts, never the raw packet content.
"""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re


def audit_links(root):
    packet_hashes = defaultdict(list)
    label_conflicts = []
    id_patterns = defaultdict(list)
    for path in sorted(root.rglob("*.tst")):
        match = re.fullmatch(r"EA_HW(\d+)", path.stem)
        if not match:
            continue
        number = int(match.group(1))
        if not any(a <= number <= b for a, b in [(4, 18), (20, 34), (36, 50), (52, 66)]):
            continue
        raw = path.read_bytes()
        header, data = raw.split(b"#Data:", 1)
        digest = hashlib.sha256(b"\n".join(data.splitlines()).strip()).hexdigest()
        relative = path.relative_to(root)
        subject = relative.parts[0]
        packet_hashes[digest].append(relative.as_posix())
        for line in header.decode("latin-1").splitlines():
            if line.startswith("#Test Conducted:"):
                match = re.search(r"EA_HW(\d+)\s*$", line)
                if not match or int(match.group(1)) != number:
                    label_conflicts.append({"subject": subject, "file_sample": number,
                                            "header_sample": int(match.group(1)) if match else None})
            if line.startswith("#ID:"):
                value = line.split(":", 1)[1].strip()
                if value != subject:
                    safe_id = value if re.fullmatch(r"E\d+", value) else "[nonstandard ID withheld]"
                    id_patterns[(subject, safe_id)].append(number)
    groups = [paths for paths in packet_hashes.values() if len(paths) > 1]
    return {
        "scope": "Signatures only, pooled by subject folder; no emotion classification",
        "comparison": "SHA-256 of packet text after newline normalization and stripping surrounding whitespace",
        "distinct_packet_streams": len(packet_hashes),
        "duplicate_groups": len(groups),
        "files_in_duplicate_groups": sum(len(paths) for paths in groups),
        "redundant_copies": sum(len(paths) - 1 for paths in groups),
        "identical_numeric_packet_groups": groups,
        "sample_label_conflicts": sorted(label_conflicts, key=lambda row: (row["subject"], row["file_sample"])),
        "header_id_conflicts": [{"directory": subject, "header_id": value,
                                 "sample_numbers": sorted(numbers)}
                                for (subject, value), numbers in sorted(id_patterns.items())],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("datasets/extracted/Database"))
    parser.add_argument("--output", type=Path, default=Path(".local-analysis/signature-integrity-details.json"))
    args = parser.parse_args()
    result = audit_links(args.data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Found {result['duplicate_groups']} duplicate groups and {len(result['sample_label_conflicts'])} sample-label conflicts.")
    print(f"Report: {args.output}")
