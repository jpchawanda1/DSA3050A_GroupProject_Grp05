# DSA3050A_GroupProject_Grp05

## Airline Delay and Operations Dashboard

**Course:** DSA 3050A – Business Intelligence & Visualization
**Project:** Advanced Group Power BI Project

## Group Name
Grp05

## Members and Student IDs
| Name | Student ID |
|---|---|
| TODO | TODO |
| TODO | TODO |
| TODO | TODO |

## Dataset Source URL
- Houston Intercontinental Airport (IAH) 2011 flights dataset ("hflights"), originally distributed via the R `hflights` package.
- TODO: add the exact URL you obtained the file from.

## Dataset Description
- File: [Dataset/hflights_raw.xlsx](Dataset/hflights_raw.xlsx) / [Dataset/raw_dataset.csv](Dataset/raw_dataset.csv)
- Rows: 227,496
- Columns: 21 — `Year, Month, DayofMonth, DayOfWeek, DepTime, ArrTime, UniqueCarrier, FlightNum, TailNum, ActualElapsedTime, AirTime, ArrDelay, DepDelay, Origin, Dest, Distance, TaxiIn, TaxiOut, Cancelled, CancellationCode, Diverted`
- Covers all flights departing Houston (IAH & HOU) in 2011.
- Full column definitions: see [Documentation/Data_Dictionary.pdf](Documentation/Data_Dictionary.pdf) (TODO).

## Business Problem
TODO: State the business problem clearly (e.g., flight delays and cancellations cause operational costs, customer dissatisfaction, and lost revenue for airlines and airports).

## Target Organization / Industry
TODO: e.g., a regional airport operations team / an airline's operations analytics department.

## Key Business Questions
- Which airlines have the highest average delays?
- Which routes are the most delayed?
- How does airport performance compare (departure vs. arrival delays)?
- What are the main cancellation reasons and their frequency?
- How do delays trend by month/season?
- What are the peak travel periods?

## Power Query Transformations
TODO: document cleaning/transformation steps applied (e.g., handling nulls in `ArrDelay`/`DepDelay`, fixing data types, deriving `Season`, `DelayCategory`, merging carrier code lookup table, removing duplicates).

## Data Model
TODO: explain the star schema/relationships between fact and dimension tables (e.g., Fact_Flights, Dim_Date, Dim_Airport, Dim_Carrier).

## DAX Measures
TODO: list and explain key DAX measures created (e.g., Average Delay, % Cancelled Flights, On-Time Performance, YoY Delay Trend).

## Dashboard Pages
- **Page 1:** TODO
- **Page 2:** TODO
- **Page 3:** TODO
- **Page 4:** TODO

## Key Insights
TODO: summarize the top 3-5 insights discovered.

## Recommendations
TODO: business recommendations based on the insights.

## Contribution Summary
| Member | Contribution |
|---|---|
| TODO | TODO |
| TODO | TODO |
| TODO | TODO |

## Repository Structure
```
DSA3050A_GroupProject_Grp05/
├── Dataset/
│   ├── hflights_raw.xlsx
│   ├── raw_dataset.csv
│   └── cleaned_dataset.csv
├── PowerBI/
│   └── GroupProject.pbix
├── Screenshots/
│   ├── raw_data.png
│   ├── power_query_editor.png
│   ├── applied_steps.png
│   ├── data_model.png
│   ├── dax_measures.png
│   ├── dashboard_page_1.png
│   ├── dashboard_page_2.png
│   ├── dashboard_page_3.png
│   └── dashboard_page_4.png
├── Documentation/
│   ├── Project_Report.pdf
│   ├── Data_Dictionary.pdf
│   ├── Presentation.pdf
│   └── Insights.pdf
└── README.md
```
