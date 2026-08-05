# Screenshots

Evidence for the Power Query, modelling and DAX work.

## Present

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

## Still to capture

These must come from a live Power BI Desktop session — they are evidence of work
done in the tool and cannot be reconstructed from the data:

| File | What to capture |
|---|---|
| `power_query_editor.png` | Power Query Editor with the cleaned query selected, showing the data preview and the query list |
| `applied_steps.png` | The Applied Steps pane, expanded to show the full transformation sequence |
| `dashboard_page_1.png` | Executive Summary page |
| `dashboard_page_2.png` | Trend Analysis page |
| `dashboard_page_3.png` | Geographic & Route Analysis page |
| `dashboard_page_4.png` | Route Drill-through page (once built) |
