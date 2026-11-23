# Eight-Film Study: Critic Dataset Cleaning Log

- Input rows: 8
- Output rows: 8
- Rows removed: 0

## Cleaning actions

- Removed 0 duplicate review IDs.
- Invalid or missing review dates: 0.
- Found 0 invalid normalized ratings before recalculation.
- Recalculated normalized ratings on a 0–10 scale using the raw rating divided by its original scale.
- Review text is blank for 8 rows; left missing rather than inventing excerpts.
- Removed 0 rows with invalid final ratings.

## Missing-data decision

Blank review excerpts are retained as missing values. No review text has been fabricated.
