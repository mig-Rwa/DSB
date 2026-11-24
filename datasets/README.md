# Supplied CIU dataset material

Project scope: signatures only, pooled per writer, with no emotion grouping or
classification. The sample ranges are 4–18, 20–34, 36–50 and 52–66. The original
documents also discuss handwriting and emotions; those topics do not expand the
agreed project scope.

The original files were supplied by the instructor. Their content has not been
modified. The public repository includes these reference documents:

- [Database Details.docx](source/Database%20Details.docx): task instructions,
  sample-number mapping, and a conceptual directory diagram.
- [Database publication](source/Database%20Publication-Emotional_State_Prediction_From_Online_Handwriting_and_Signature_Biometrics.pdf):
  Yasemin Bay Ayzeren, Meryem Erbilek, and Erbug Celebi, *Emotional State Prediction
  From Online Handwriting and Signature Biometrics*, IEEE Access 7 (2019),
  164759–164774. [DOI: 10.1109/ACCESS.2019.2952313](https://doi.org/10.1109/ACCESS.2019.2952313).
  The supplied PDF identifies the article as CC BY 4.0 on its first page. This
  article license does not establish a redistribution license for the raw archive.

`source/Copy of Database.7z` is retained locally and excluded from Git, together
with `extracted/`. The archive contains biometric recordings and images, exact
dates of birth, demographic data, and capture-machine metadata. The repository
owner chose not to publish those records. There are no raw biometric examples in
the published analysis.

## Verify the supplied copies

[source-manifest.json](source-manifest.json) records the original filename, byte
size, and SHA-256 of each of the three supplied files, including the local archive.
For example, in PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath 'datasets/source/Copy of Database.7z'
```

The archive SHA-256 is
`f8d3ee9ac030d95fa0146f32bb4d4bc8d8ffbe861f993b183f299edb610c3a43`.

## Inspect an authorized local copy

Place the archive at `datasets/source/Copy of Database.7z` without changing its
name or contents. Use 7-Zip to test and extract it from the repository root:

```powershell
& 'C:\Program Files\7-Zip\7z.exe' t 'datasets/source/Copy of Database.7z'
& 'C:\Program Files\7-Zip\7z.exe' x 'datasets/source/Copy of Database.7z' '-odatasets/extracted'
```

The extracted files occupy 948,982,590 bytes before filesystem overhead. The
archive is 133,471,332 bytes. Extraction does not alter the original archive.

The inspection utility needs Python 3.11+ and Pillow; these are requirements for
the audit only, not replacements for STA's original runtime:

```powershell
python -m pip install Pillow
python -B tools/audit_dataset.py --data datasets/extracted/Database --output .local-analysis/audit.json
python -B tools/audit_signature_links.py --data datasets/extracted/Database --output .local-analysis/signature-integrity-details.json
```

This inventories the archive, reads every selected signature `.tst` row, and
fully decodes all 8,040 selected signature JPEGs. Handwriting and the aborted
image are excluded from signature analysis. It reports aggregate values and
pseudonymous file identifiers without
exporting demographic values or biometric samples. The committed report includes
size/CRC checks against a local 7-Zip `l -slt` listing of the original archive.
The optional `--inventory` argument accepts a locally generated JSON version of
that listing; the simple command above omits those extra checks. The 7-Zip test
command independently checks archive integrity.

The second utility compares numeric packet sections independently of their
headers, and checks filename/sample-number and directory/writer-ID agreement.
Its published results are in
[signature-integrity-details.json](signature-integrity-details.json).

Read [the analysis](../docs/DATASET_ANALYSIS.md) before trusting identifiers,
splitting duplicate records, or interpreting capture units. No classification or verification
experiment has been performed in this repository.
