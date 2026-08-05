# Screenshots

Evidence for the Power Query, modelling and DAX work.

| File | What it shows | Origin |
|---|---|---|
| `raw_data.png` | First 14 rows of the raw dataset — HHMM times, 0/1 flags, blank cancellation codes | Rendered from `Dataset/raw_dataset.csv` |
| `column_profiling.png` | Column quality profile of all 21 raw columns: type, null count, null %, distinct values, range | Computed from `Dataset/raw_dataset.csv` |
| `cleaned_data.png` | First 14 rows of the cleaned table — decoded codes, real clock times, derived categories | Rendered from `Dataset/cleaned_dataset.csv` |
| `data_model.png` | The star schema and relationships | Power BI Desktop capture |
| `dax_measures.png` | Basic Measures and Delay Performance folders | Power BI Desktop capture |
| `dax_measures_advanced.png` | KPI Status, Rankings and Time Intelligence folders | Power BI Desktop capture |
| `dax_measure_folders.png` | The six measure display folders | Power BI Desktop capture |

The three data images are faithful renderings of the actual CSV files rather than
Power BI screen captures, and each carries a caption saying so.

The Power Query Editor and Applied Steps evidence is not here — it lives in
[Documentation/PowerQuery_Cleaning_Steps.docx](../Documentation/PowerQuery_Cleaning_Steps.docx),
which captures all 24 transformation steps from a live session.
