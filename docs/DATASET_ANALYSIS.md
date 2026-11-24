# CIU signature dataset analysis

Reviewed on 2026-11-24. This document distinguishes statements in the supplied
publication/DOCX from observations in the supplied archive and from interpretations
that still need confirmation. The source documents are evidence, not instructions
to implement their methods. STA remains at the original upstream implementation.

**Agreed scope: signatures only, pooled per writer, without emotion grouping or
classification.** All 60 nominal signatures in each subject folder belong to one
writer pool. Handwriting is excluded. Collection-task descriptions below explain
the source documents and file selection only; they are not modeling labels.
Ignoring emotion labels does not assert that the recordings were acquired in an
identical emotional state. No modeling or dataset cleanup has been performed.

## 1. What each supplied file contains

| File | Role | Inspection |
| --- | --- | --- |
| `Database Details.docx` | Short collection-task description, numeric sample ranges, and one embedded directory diagram | All paragraphs, the hyperlink, and the embedded image were examined. |
| `Database Publication-Emotional_State_Prediction_From_Online_Handwriting_and_Signature_Biometrics.pdf` | 16-page IEEE Access paper describing acquisition, labels, experiments, results, references, and authors | All pages were read; all 11 tables and six figures were inspected, including content not exposed by PDF text extraction. |
| `Copy of Database.7z` | Original biometric files and participant metadata | Full archive integrity was checked; the published numeric/image analysis selects only signatures. |

The PDF is by Yasemin Bay Ayzeren, Meryem Erbilek, and Erbug Celebi (2019), DOI
[10.1109/ACCESS.2019.2952313](https://doi.org/10.1109/ACCESS.2019.2952313).
The supplied first page states CC BY 4.0 for the article. The DOCX links to the
same article. Checksums of all supplied originals are in
[source-manifest.json](../datasets/source-manifest.json).

## 2. Reading the DOCX in order

1. **Database Details / article link.** This identifies the accompanying study;
   it is not an additional dataset download link.
2. **Directory diagram.** This is a conceptual picture of a subject directory,
   demographic file, handwriting files, and signature files. Its labels such as
   `HW1.txt`, `SG1.txt`, and `Demographic info.txt` do not match this archive's
   actual filenames. The diagram ending at E140 is not an inventory.
3. **Number of subjects: 142.** This conflicts with the paper and archive. The
   archive contains 134 subject directories, with identifiers reaching E142.
   An identifier range is not a participant count.
4. **Fixed Task 1.** Participants copy the supplied passage three times. This
   produces handwriting samples 1, 2, and 3, followed by 15 signatures, 4–18.
   The quoted passage has 43 whitespace-separated words and 285 characters
   including spaces; the stated 243 characters counts characters without spaces.
   This is the initial/natural condition, not evidence that every person was
   emotionally neutral.
5. **Variable Task 2.** Two successive video/opinion tasks are grouped under one
   heading: happy video, then sad video. The opinion texts are samples 19 and 35;
   their respective signature ranges are 20–34 and 36–50. The paper calls these
   Task 2 and Task 3 separately. A video condition is a collection condition;
   it does not itself supply an individual's self-reported emotion score.
6. **Fixed Task 2.** This is the paper's Task 4. A countdown limits copying the
   short sentence to 10 seconds. Handwriting is sample 51, followed by signatures
   52–66. The short sentence contains 10 words, 59 characters with spaces and 50
   without spaces. The time limit applies to the copying task; the documents do
   not say that each subsequent signature must last 10 seconds.

The exact quoted passages are preserved in the original DOCX. They are stimuli
for handwriting collection, not text to synthesize as signatures.

## 3. Signature selection for this archive

Every complete subject contributes 66 numbered samples. The actual prefix
`EA_HW` is used for both handwriting and signatures; the prefix alone does not
identify the modality.

| Included filename numbers | Files per subject | Files across 134 subject folders |
| --- | ---: | ---: |
| 4–18 | 15 | 2,010 |
| 20–34 | 15 | 2,010 |
| 36–50 | 15 | 2,010 |
| 52–66 | 15 | 2,010 |
| **One combined pool** | **60** | **8,040** |

These ranges come from the supplied DOCX and select files by filename. Internal
header labels sometimes disagree with filenames or directories, as documented
below. Numbers 1, 2, 3, 19, 35 and 51 are excluded. The four included ranges are
combined; they do not define four classes or four separate evaluation groups.

## 4. Physical archive inventory

The archive is a single, unencrypted, solid LZMA2 7-Zip archive. It contains
270 directories and 18,099 files, totaling 948,982,590 uncompressed bytes.
7-Zip reported a successful integrity test and extraction.

| Extension | Files | Meaning |
| --- | ---: | --- |
| `.tst` | 8,847 | MEDDRAW text recordings: metadata followed by time-ordered tablet packets |
| `.jpg` | 8,848 | Raster renderings of handwriting/signatures, including one aborted image |
| `.txt` | 134 | One `subject.txt` demographic record per subject |
| `.dat` | 270 | `analysis.dat` and `playback.dat` capture-software files; every one contains `False` |

There are 134 subject directories. Missing IDs between E001 and E142 are E034,
E036, E038, E039, E043, E050, E051, and E133. The paper attributes skipped IDs
generally to registrations without donated samples; the archive does not provide
an individual exclusion log confirming the reason for each missing ID.

The actual structure is:

```text
Database/
  E001/
    subject.txt
    EA_HW-<capture-date-and-time>/
      EA_HW1.tst
      EA_HW1.jpg
      ...
      EA_HW66.tst
      EA_HW66.jpg
      analysis.dat
      playback.dat
  ...
```

Every subject folder has the 60 selected signature filenames. The archive also
contains 807 handwriting `.tst` files, which are outside this project. Its extra
partial capture folder contains only excluded sample numbers and does not add
signature samples. No source file has been removed or altered.

`E099/EA_HW20(Aborted).jpg` is the sole image without a matching `.tst` file. The
regular sample 20 is still present in E099's capture directory. Every `.tst`
recording has a corresponding `.jpg`. The extra image must not be counted as an
additional valid online signature.

There is no CSV, spreadsheet, questionnaire, score sheet, README, or dataset
license file in the archive. All `.dat` files are boolean text flags; they are
not feature vectors or emotion labels.

## 5. `subject.txt`: meaning of every field

These files are metadata, not tablet trajectories. All 134 have the same set of
named fields. Their literal demographic values are kept out of this public report.

| Line/field | Interpretation |
| --- | --- |
| Initial `#` software/comment lines | Capture-software provenance and formatting comments, not observations. |
| `#File Created`, `#File Last Edited` | Metadata-file creation/edit dates; not the sample's drawing time. |
| `#By` | Metadata operator/author field; not the participant's biometric identifier. |
| `#Test Group` | Capture-software group label. The word `Patient`, where present, does not establish a clinical diagnosis. |
| `#ID` | Subject identifier; the directory supplies the corresponding pseudonymous grouping. |
| `#Date of Birth` | Exact birth date. It is personal information, not a recording timestamp. |
| `#Gender` | Recorded demographic category. The archive contains 39 `F` and 95 `M` values, matching the paper's aggregate counts. |
| `#Writing Hand` | Recorded writing hand: 123 Right and 11 Left, matching the paper. |
| `#Hospital ID` | A second identifier field inherited from the capture software; its label does not prove clinical recruitment. |
| `#Edu.(1-High Sch 2-Uni 3-Ms 4-PhD)` | Education coding: 1 high school, 2 university, 3 master's, 4 doctorate. Observed counts are 5, 58, 40, 31 respectively, matching the paper. |
| `#Nat.(1-TC 2-KKTC 3-NG 4-ZW 5-Other)` | Nationality code. The header documents only 1–5, but observed values span 1–22. Codes 6–22 require a separate codebook; do not invent country mappings or derive ethnicity from them. |
| `#Comments:` and `< ... >` | Delimited free-text comment block. Every subject's block contains `No Comment`. It contains no emotion ratings. |
| Blank lines | Formatting separators. |

The paper reports 22 nationalities but this archive does not include a full
nationality codebook. Its broad figure labelled ethnicity is not a substitute
for that missing codebook. These demographic fields are not required simply to
identify which signatures belong to one writer.

## 6. `.tst`: header and packet structure

All 8,847 recordings have the same named metadata fields and a delimited
`No Comment` block. The extension `.tst` is a text format, not an image or a
spreadsheet. Read the header before interpreting numeric rows.

| Header line/field | Meaning and limits |
| --- | --- |
| `#Written using MEDDRAW Data Capture Version 2.1 ...` | Software and institution attribution; minor spacing variations occur. |
| `#Date` | Capture date/time, separate from the packet-relative `Ti` column. |
| `#Filename` | Original capture-machine path. It may disclose workstation/user information and is not a portable path to open on this computer. |
| `#Test Conducted` | Capture task and sample label such as `EA_HW, EA_HW4`; use the DOCX's numeric ranges to determine modality/condition. |
| `#Clinician` | Capture operator field, not the writer's identity or an emotion label. |
| `#Tablet Info` | Start of device metadata. |
| `#Protocol` | Reported tablet protocol, `WACOM Tablet`. |
| `#Capture Device` | Device type, `Graphics Tablet`. |
| `#Freq` | Nominal capture-frequency setting. It must not replace the actual recorded timestamps with fabricated evenly spaced samples. |
| `#Axes Unit` | Literal coordinate-unit descriptor. Its notation needs capture-software documentation before a physical unit conversion is asserted. |
| `#X_Origin`, `#Y_Origin` | Device-coordinate origin settings. |
| `#X_Extent`, `#Y_Extent` | Configured coordinate extents, not each signature's bounding box. |
| `#X_Res`, `#Y_Res` | Recorded resolution settings. Their physical interpretation depends on the device/capture mapping. |
| `#NP_Max` | Declared maximum normal-pressure value; compare with observed values rather than assuming a new tablet shares this scale. |
| `#Subject Info` | Start of participant metadata embedded in every recording. |
| `#Test Group`, `#ID` | Group and writer identifier. |
| `#Age` | Age at capture in years/months; this repeats personal information even if `subject.txt` is removed. |
| `#Gender`, `#Writing Hand` | Repeated participant demographics. |
| `#Hospital ID` | Repeated secondary identifier field. |
| Education and nationality fields | Same coded meanings and codebook limitations as `subject.txt`. |
| `#Comments:` / `<` / `No Comment` / `>` | Empty-in-substance comment block, not a label record. |
| `#Ti X Y NP TP St Cu Co Bu Az Al Tw Pi Ro Ya` | Tab-separated packet-column names in order. The leading `#` marks a header. |
| `#Data:` | Numeric packet data begins after this marker. |
| Each following row | One recorded tablet event, with 15 tab-separated numeric fields. It is not one complete signature or necessarily a pen-down event. |

### Packet-column dictionary

The supplied files do not include a MEDDRAW format specification. Coordinates,
pressure and orientation are supported by the paper's acquisition/feature
description. Several abbreviations also resemble Wintab packet fields. The
following Wintab-related expansions are interpretations, not a verified MEDDRAW
serialization contract; the exact capture mapping remains to be confirmed.

| Column | Interpretation |
| --- | --- |
| `Ti` | Recorded elapsed-time value. Keep its original ticks/deltas; the supplied documents do not explicitly establish the serialized unit. |
| `X`, `Y` | Recorded horizontal and vertical coordinates. Do not assume image pixels or an axis direction without checking the capture mapping. |
| `NP` | Normal/tip pressure, consistent with `NP_Max`. Zero pressure and a released contact/button state are not necessarily identical. |
| `TP` | Likely tangential-pressure channel. |
| `St` | Likely packet status flags, not stress or emotional state. |
| `Cu` | Likely cursor/tool identifier. |
| `Co` | Likely tablet context identifier; not an emotion or task-condition code. |
| `Bu` | Likely button-state field. The audit compares its low bit with positive pressure as a diagnostic; this does not establish a final pen-contact rule. |
| `Az` | Azimuth/orientation channel. |
| `Al` | Altitude/tilt channel. |
| `Tw` | Likely twist orientation channel. |
| `Pi`, `Ro`, `Ya` | Likely pitch, roll and yaw rotation channels. A recorded constant zero does not prove that the underlying physical motion was zero. |

[Wacom's official Wintab reference](https://developer-docs.wacom.com/docs/icbt/windows/wintab/wintab-reference/)
describes packet time, coordinates, pressure, status, cursor, context, buttons,
orientation and rotation. It does not document MEDDRAW's export abbreviations or
any transformations applied before writing this dataset. Wintab's timestamp
description alone therefore does not prove the unit of `Ti` here.

### JPEGs and `.dat` files

The JPEGs are static raster views; they do not retain timing, pressure, stroke
order or pen-lift timing. The paper describes black ink on white, a 20-pixel
border, and generation at 100 pixels per inch. Those are acquisition-description
claims, not a calibration method for recovering device coordinates from images.
The complete audit verifies and decodes the actual JPEG files separately.

Each of the 135 capture directories has `analysis.dat` and `playback.dat`.
All 270 files contain `False`. These appear to be capture-application state
flags; their exact application semantics are undocumented. They provide neither
precomputed kinematic features nor per-participant emotion scores.

## 7. Publication interpretation within this project's scope

All 16 pages, 11 tables and six figures were examined. Pages 1–6 introduce the
motivation and prior databases; pages 6–9 describe acquisition, participants,
tasks, consent and file organization; pages 9–13 describe feature extraction,
normalization, emotion classifiers and results; pages 13–16 contain conclusions,
references and author information. The paper studies emotion prediction. Its
emotion thresholds, class labels, feature choices and reported classification
accuracies are not instructions or benchmarks for this signature-verification
project.

The useful acquisition facts are the reported single-session collection,
pressure-sensitive Wacom capture, online event records, static companion images,
and the intended grouping of samples by person. The sample-count and filename
claims need to be checked against this particular archive. The DOCX's 142 count,
the diagram's E140 endpoint, and the paper's conceptual HW/SG `.txt` names do not
match the 134 actual folders and `EA_HW*.tst` filenames.

The paper's individual emotion score sheets were not found in this archive.
They are not needed for the agreed project scope. Demographic categories,
collection tasks and emotion information are not used as classification labels,
verification features or separate evaluation groups here.

The paper's permission/consent discussion and article CC BY 4.0 notice do not
establish raw-data redistribution terms for this copy. At the repository owner's
explicit request, raw records remain local and only reference documents and
analysis are published.

## 8. Signature-quality findings that matter for verification

The files are preserved exactly as supplied. This section records problems for
review; it does not clean, relabel, discard, normalize or interpolate any sample.
There are **8,040 selected signature filenames in 134 subject folders**, which
must not be confused with 8,040 independent, validated observations or 134
independently verified identities.

The signature audit read **3,237,402 numeric packets** and fully decoded all
**8,040 selected JPEGs**. No malformed numeric rows, non-finite numbers, empty
signature data sections, or JPEG decoding failures were found. The time/contact/
identifier findings below are separate semantic problems, not archive damage.
All 18,099 extracted files also matched the archive's listed size and CRC.

### Duplicate recordings

Comparing the numeric packet sections after normalizing line endings finds
**56 duplicate groups containing 116 files**. These include 53 pairs, two triples
and one group of four: 60 redundant copies and **7,980 distinct packet streams**.
All detected duplicates occur within the same subject directory. Twelve pairs
also have byte-identical complete `.tst` files; looking only at complete-file
hashes would miss other repeated recordings because their headers differ.

Full group memberships are recorded in the linkage audit. A future enrollment/
test split must keep copies of the same packet stream together. Ignoring emotion
labels does not remove the duplicate problem. No copy has been deleted or chosen
as canonical.

### Writer-ID disagreements

**121 selected recordings** have a header `#ID` different from their directory:

| Directory | Selected samples with conflicting IDs | Header ID |
| --- | --- | --- |
| E021 | All 60 signatures | E022 |
| E132 | 23 and 52–66 | E133 |
| E141 | 20–34 | E142 |
| E141 | 36–50 | E143 |
| E141 | 52–66 | E144 |

Directory IDs are the audit's grouping keys, not proof that the conflicting
header values are wrong. Do not silently merge these folders with similarly
named IDs or relabel recordings. The dataset owner needs to clarify the correct
writer identity before those groups are used as unquestioned biometric ground
truth.

### Filename/sample-label disagreements

**210 signatures** have a `#Test Conducted` sample number that differs from the
filename number. The affected subject directories are E006, E007, E013, E072,
E073, E083, E094, E106, E118, E122, E125, E131, E132, E140 and E141. Some have
systematic offsets; others have repeated header labels. Exact differences are
in the linkage audit. Representative images with conflicting labels were
visually inspected, but this does not establish the correct historical label
for every affected record.

The current selection follows the supplied DOCX's filename ranges. Header
conflicts are retained as audit findings, not silently used to move files into
or out of the signature pool.

### Timestamps

Four signatures contain a backward timestamp step:

| Directory/sample | Source line | Backward change in raw ticks |
| --- | ---: | ---: |
| E014 / 13 | 70 | -3,354 |
| E028 / 48 | 52 | -3,459 |
| E042 / 64 | 43 | -2,172 |
| E120 / 7 | 107 | -6 |

E014/13 even ends below its first timestamp. E042/64 has values near and above
2^32; this suggests a counter/offset issue but does not establish its cause.
Do not silently sort the packets or turn negative deltas into valid dwell times.

The nominal `Freq` value is 100, while the most common consecutive differences
are 8 and 7 raw ticks. Sampling is not uniformly spaced. Confirm the capture
format before labeling ticks as milliseconds or computing physical velocities.

### Pressure/contact and companion images

E031/4 has 44 raw packets with `NP = 0` and `Bu = 0` throughout. Its companion
JPEG nevertheless contains visible drawn ink. Thus the dynamic file lacks
positive-pressure/contact evidence even though the image is not visually empty.
This is a record/image consistency issue for review, not an automatically
repaired or removed sample.

Across the selected signatures, 3,045 packets have the low button bit set with
zero pressure. None has positive pressure with that bit clear. The indicators
are related but not identical. A final pen-contact rule requires capture-format
confirmation.

Representative JPEGs show blue strokes on a large white canvas; all inspected
JPEG metadata lacks a declared DPI value. The paper's black-ink, border and
100-PPI description is therefore not a verified pixel-to-device conversion for
this archive. The numeric `.tst` packets are the dynamic evidence.

## 9. Decisions still needed before implementation

1. The supervisor's exact first implementation step and expected deliverable.
2. The correct identity for conflicting headers/directories and the correct
   handling of conflicting sample labels.
3. A documented policy for duplicate packet streams, backward timestamps, and
   the raw/image mismatch. No automatic cleanup has been applied.
4. The MEDDRAW definitions of timestamp units, axes, orientation scales and
   button/contact state. Several abbreviations are inferred, not fully specified.
5. A future enrollment/test protocol for one pooled signature set per writer.
   No counts, thresholds, model or experiment have been selected at this stage.

No skilled-forgery recordings or corresponding labels are described in the
supplied material. Another person's genuine signature would be a random-impostor
probe, not a skilled forgery. This audit has not performed either evaluation.

See [audit-summary.json](../datasets/audit-summary.json) for numeric checks and
[signature-integrity-details.json](../datasets/signature-integrity-details.json)
for duplicate groups and header conflicts. Neither report contains raw
trajectories, signature images, birth dates or demographic values.
