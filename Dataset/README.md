# Dataset

All data here is the `hflights` dataset — every commercial flight that departed
Houston's two airports in 2011, as reported by the **US DOT Bureau of
Transportation Statistics**. Source: https://cran.r-project.org/package=hflights

| File | Rows × Cols | What it is |
|---|---|---|
| `hflights_raw.xlsx` | 227,496 × 21 | Original source workbook, exactly as downloaded |
| `raw_dataset.csv` | 227,496 × 21 | Raw extract, unmodified |
| `cleaned_dataset.csv` | 227,496 × 32 | Output of the Power Query pipeline — the `Fact_Flights` table |
| `dim_airline.csv` | 15 × 2 | Carrier-code lookup, merged into the fact table |
| `dim_date.csv` | 365 × 9 | Generated 2011 calendar, marked as the model date table |

## Raw columns

`Year, Month, DayofMonth, DayOfWeek, DepTime, ArrTime, UniqueCarrier, FlightNum,
TailNum, ActualElapsedTime, AirTime, ArrDelay, DepDelay, Origin, Dest, Distance,
TaxiIn, TaxiOut, Cancelled, CancellationCode, Diverted`

## Regenerating the cleaned files

`cleaned_dataset.csv`, `dim_airline.csv` and `dim_date.csv` are produced by the
same transformation pipeline that runs in Power Query:

```bash
python3 Documentation/clean_dataset.py
```

Every column is defined in [Documentation/Data_Dictionary.pdf](../Documentation/Data_Dictionary.pdf).

## One thing worth knowing

The 3,622 null values in `Arrival Delay` are **not** a data-quality defect — they
are the cancelled and diverted flights, which have no arrival to be late for.
They are deliberately left null rather than filled with zero, because a zero would
read as "arrived on time" and would both deflate every delay average and inflate
the on-time rate. The DAX divides by completed flights instead.
