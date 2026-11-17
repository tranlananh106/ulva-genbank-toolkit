# 0. Import modules ---------------------------------------------------
import csv
import glob
from pathlib import Path


# 1. Define the extraction function -----------------------------------
# Input: the text of one GenBank record.
# Returns: metadata values and the uppercase DNA sequence.
def sequence(subfile):
    """Extract metadata and DNA from one GenBank record."""

    # Extract metadata in the same order as the CSV columns.
    # Note: only the first matching line is kept for each field.
    value_list = []
    for variable in ("ACCESSION   ", "ORGANISM  ", "AUTHORS   ", "TITLE     ", "JOURNAL   ", "/isolate=", "/specimen_voucher=", "/country=", "/lat_lon=", "/collected_by=", "/identified_by="):
        if variable in subfile:
            start_index = subfile.find(variable)
            subsubfile = subfile[start_index:]
            line_end = subsubfile.find("\n")
            value = subfile[start_index + len(variable):start_index + line_end]
        else:
            value = "None"  # Keep a placeholder for missing metadata.
        value_list.append(value)

    # Extract DNA after ORIGIN; remove line numbers and join sequence blocks.
    # Note: this assumes the ORIGIN heading matches the text below.
    start_index = subfile.find("ORIGIN      \n")
    sequence = subfile[start_index + 14:]
    seq_list = sequence.split()
    seq_list = [i for i in seq_list if i.isalpha()]
    sequence = "".join(seq_list)
    return value_list, sequence.upper()


# 2. Set input and output paths ---------------------------------------
# Paths start from this script's folder. Use data/raw/*.gb for several files.
# Note: running again replaces the existing output files.
project_folder = Path(__file__).resolve().parent
filesource = glob.glob(str(project_folder / "data/raw/sequences.txt"))
if not filesource:
    raise FileNotFoundError("No input files found. Check the input path.")
(project_folder / "outputs").mkdir(exist_ok=True)
fasta_path = project_folder / "outputs/sequences.fasta"
csv_path = project_folder / "outputs/metadata.csv"


# 3. Prepare the metadata table ---------------------------------------
variable_list = ["accession", "organism", "authors", "title", "journal", "isolate", "specimen_voucher", "country", "lat_long", "collector", "identifier"]
output_list = [variable_list]  # The first row is the CSV header.


# 4. Read GenBank records and export FASTA -----------------------------
# Accumulate one record at a time; // marks the end of a record.
with open(fasta_path, "w", encoding="utf-8") as sequence_fasta_file:
    for f in filesource:
        with open(f, "r", encoding="utf-8") as sequence_file:
            line = sequence_file.readline()
            mysubfile = ""

            while line:
                if line == "//\n":
                    value_list, mysequence = sequence(mysubfile)

                    # FASTA header: organism_specimen-voucher_accession.
                    # Metadata positions: [1] organism, [6] voucher, [0] accession.
                    name = ">" + value_list[1] + "_" + value_list[6] + "_" + value_list[0] + "\n" + mysequence + "\n"
                    print(name, file=sequence_fasta_file)
                    output_list.append(value_list)

                    # Reset the buffer before reading the next record.
                    line = sequence_file.readline()
                    mysubfile = ""
                else:
                    mysubfile += line
                    line = sequence_file.readline()


# 5. Export metadata --------------------------------------------------
# Write the header and one metadata row per record.
with open(csv_path, "w", encoding="utf-8", newline="") as output_file:
    writer = csv.writer(output_file)
    for row in output_list:
        writer.writerow(row)
