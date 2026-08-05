# Power BI

| File | Contents |
|---|---|
| `GroupProject.pbix` | **The submission file.** Full data model, 22 DAX measures, Executive Summary and Geographic & Route Analysis pages |
| `GroupProject_ExecSummary_TrendPages.pbix` | Holds the **Trend Analysis** page. Same data model — pending merge into `GroupProject.pbix` |
| `Executive_Summary_Insights.docx` / `.pdf` | Five insights read off the Executive Summary and Trend pages, plus five recommendations |
| `Geographic_and_Drillthrough_Analysis.docx` / `.pdf` | Walkthrough of the Geographic & Segment, drill-through, decomposition tree and custom tooltip pages |

Both write-ups are kept in Word and PDF. Edit the `.docx`, then re-export the
`.pdf` so the two stay in step.

## Merging the two files

Both files carry an identical data model (same tables, same relationships, same
lineage tags), so the merge is a copy-paste rather than a rebuild:

1. Open both files in Power BI Desktop.
2. In `GroupProject_ExecSummary_TrendPages.pbix`, select the visuals on the Trend
   Analysis page and copy them.
3. Paste onto a new page in `GroupProject.pbix`. Because the model is identical,
   every field binding resolves without remapping.
4. Re-sync the slicers across all pages (View → Sync slicers).
5. Delete `GroupProject_ExecSummary_TrendPages.pbix` once the merge is verified.

## Model summary

- **Fact_Flights** — 227,496 rows, one per flight
- **Dim_Date** — 365 rows, marked as the model date table
- **Dim_Airline** — 15 rows
- **Summary_Airline_Performance** — 15-row Group By aggregate
- **_Measures** — disconnected table holding all 22 measures in six display folders

All relationships are many-to-one, single-direction. No bi-directional filters.

## Still to build

- **Page 4 — Route Drill-through**, drilling through on `Fact_Flights[Route]`
  from the map and matrix on the Geographic page.
- A **custom tooltip page** for the carrier visuals.

> Keep the `.pbix` under GitHub's 100 MB limit. Both files are currently ~3 MB.
