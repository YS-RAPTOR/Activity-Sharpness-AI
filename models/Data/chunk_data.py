import csv
from data import PROCESSED_DATA_DIR
from pathlib import Path

path = Path(PROCESSED_DATA_DIR)


input_file = path / "data.csv"
rows_per_chunk = 10000
output_file_template = str(path / "chunk_{}.csv")

print(f"Splitting {input_file} into chunks of {rows_per_chunk} rows each.")
print(f"Output files will be named {output_file_template}.")

with open(input_file, newline="") as infile:
    reader = csv.reader(infile)
    header = next(reader)

    file_count = 0
    rows = []

    for i, row in enumerate(reader, start=1):
        rows.append(row)
        if i % rows_per_chunk == 0:
            with open(
                output_file_template.format(file_count), "w", newline=""
            ) as outfile:
                writer = csv.writer(outfile)
                writer.writerow(header)
                writer.writerows(rows)
            rows = []
            file_count += 1

    # Write any remaining rows
    if rows:
        with open(output_file_template.format(file_count), "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)
            writer.writerows(rows)

