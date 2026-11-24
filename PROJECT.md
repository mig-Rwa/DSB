# DSB: original STA and dataset review

This is the team's starting repository. The original Scanpath Trend Analysis
implementation and its research examples remain unchanged. No signature adapter,
Python 3 port, preprocessing pipeline, model, or evaluation has been implemented.
The supervisor's first-step implementation instructions are still pending.

The agreed scope is **signature verification only**: select samples 4–18, 20–34,
36–50 and 52–66, then treat all 60 as one pool for each writer. Handwriting is
excluded. Emotion labels and collection conditions are not features, classes,
separate models or evaluation groups for this project.

## Original algorithm

- Source: <https://github.com/SukruEraslan/sta>
- Baseline commit: `8c3939e4acbcc524babdaadb08a0f20378470d47`
- Original history is retained in this repository.
- `STA.py` is the original STA script; `STA_withToleranceLevel.py` is the original
  tolerance extension. The `sta-ds/` variants and `Help/` examples are also intact.
- The original scripts require Python 2 and contain parameters that must be
  supplied before execution. They have deliberately not been modernized here.

The original [README](README.md) contains the STA authors and publications.
No new license is assigned to the upstream code or dataset.

## Dataset documents and inspection

- [Dataset guide](datasets/README.md): supplied files, local setup, and checksums.
- [Dataset analysis](docs/DATASET_ANALYSIS.md): document interpretation, archive
  counts, file formats, discrepancies, and unresolved questions.
- [Audit results](datasets/audit-summary.json): inspection results, with no
  participant demographic values, signature images, or trajectories.
- [Read-only audit utility](tools/audit_dataset.py): inspects extracted files and
  does not import, call, or change STA.

The repository owner explicitly chose to keep the raw biometric archive and
extracted participant records local. Only the supplied PDF/DOCX, source checksums,
and analysis are published. Git ignore rules exclude the raw archive and local
extraction directory. Obtain the archive separately through the instructor's
approved channel.
