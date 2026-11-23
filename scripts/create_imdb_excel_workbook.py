
from pathlib import Path
import csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = ROOT / "data" / "processed" / "imdb" / "eight_films_imdb.csv"
OUTPUT_FILE = ROOT / "data" / "staging" / "imdb" / "eight_films_excel_cleaning.xlsx"

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Read original CSV
with open(INPUT_FILE, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file)
    rows = list(reader)

if not rows:
    raise ValueError("The input CSV is empty.")

headers = rows[0]
data = rows[1:]

# Create workbook
wb = Workbook()

# Sheet 1: Original data
raw = wb.active
raw.title = "Raw_Data"

for row in rows:
    raw.append(row)

# Sheet 2: Working copy for Excel cleaning
cleaned = wb.create_sheet("Cleaned_Data")

for row in rows:
    cleaned.append(row)

# Sheet 3: Cleaning log
log = wb.create_sheet("Cleaning_Log")

log_headers = ["Step", "Cleaning Operation", "Excel Method", "Result / Observation"]
log.append(log_headers)

operations = [
    [1, "Check for duplicate records", "Data > Remove Duplicates", ""],
    [2, "Check for missing values", "Filter each column for blanks", ""],
    [3, "Remove leading/trailing whitespace if present", "TRIM() formula", ""],
    [4, "Verify numeric data types", "Format Cells / VALUE()", ""],
    [5, "Verify film IDs and IMDb IDs", "Filter and inspect values", ""],
    [6, "Check rating values are within 0–10", "Sort / conditional formatting", ""],
    [7, "Check vote counts are non-negative integers", "Format Cells / filter", ""],
]

for operation in operations:
    log.append(operation)

# Formatting
header_fill = PatternFill(
    start_color="1F4E78",
    end_color="1F4E78",
    fill_type="solid"
)

for ws in wb.worksheets:
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center")

    for column_cells in ws.columns:
        max_length = max(
            len(str(cell.value)) if cell.value is not None else 0
            for cell in column_cells
        )
        column_letter = get_column_letter(column_cells[0].column)
        ws.column_dimensions[column_letter].width = min(max_length + 3, 40)

# Save workbook
wb.save(OUTPUT_FILE)

print("Excel workbook created successfully!")
print(f"Input records: {len(data)}")
print(f"Columns: {len(headers)}")
print(f"Saved to: {OUTPUT_FILE}")
