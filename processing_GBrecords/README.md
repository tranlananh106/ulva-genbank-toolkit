# Ulva GenBank Toolkit

A Python research script for extracting metadata and DNA sequences from downloaded GenBank records.

## Background

I developed the original script in 2018 to prepare GenBank data for research that contributed to our 2022 paper, [*An appraisal of Ulva (Ulvophyceae, Chlorophyta) taxonomy*](https://doi.org/10.1007/s10811-022-02815-x). The study examined species delimitation, species-name usage and geographic coverage of genetic data in *Ulva*.

`genbank_to_csv_fasta.py` preserves the original extraction workflow with updated portable project paths. It processes files already downloaded from GenBank.

## Run

Requires Python 3.10 or later. No additional packages are needed.

Set the input path in section 2 of the script, then run:

```bash
python genbank_to_csv_fasta.py
```

Results are saved as `outputs/metadata.csv` and `outputs/sequences.fasta`. Running again replaces these files.
