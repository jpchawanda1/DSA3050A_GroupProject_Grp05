# Documentation

| File | Pages | Contents |
|---|---|---|
| `Project_Report.pdf` | 13 | Full written report — business problem, data understanding, Power Query cleaning, data modelling, DAX, dashboard design, insights, recommendations, limitations, conclusion |
| `Data_Dictionary.pdf` | 7 | Every column of the raw and cleaned datasets plus all three dimension tables: name, type, meaning, example value, null count. Includes the cancellation and airport code reference |
| `Insights.pdf` | 8 | Eight evidence-backed insights with supporting charts, six recommendations traced to those insights, and the overall storyline |
| `Presentation.pdf` | 12 | Landscape slide deck for the 10-minute presentation |

No figure or statistic in these documents is hand-entered — every number is
computed from the files in `Dataset/`, and every chart is generated from the same
source. The build scripts that produce them are kept outside version control.

## PowerQuery_Cleaning_Steps.docx

The one document here that is *not* generated. It is a live capture: 24
screenshots taken in the Power Query Editor, in the order the transformations
were applied — rename and delete columns, set data types, remove duplicates and
blank rows, trim and clean text, replace inconsistent values, handle missing
values, split and merge columns, custom and conditional columns, extract date
parts — followed by the advanced tasks: merge queries, append queries, unpivot
columns, parameters, a reference query, and business categories built from
nested conditions.

It is the evidence that the cleaning described in `Project_Report.pdf` was done
in the tool rather than reconstructed afterwards. Carried over from the `main`
branch, where it was committed as `Dataset/BI project screenshots.docx`.

## figures/

The seven charts used in the report and deck:

| File | Shows |
|---|---|
| `fig1_monthly_trend.png` | Average arrival delay and on-time rate by month |
| `fig2_airline_ontime.png` | On-time rate by airline against the system average |
| `fig3_cancellations.png` | Cancellations by month, split by reason |
| `fig4_hour_of_day.png` | Average departure delay by scheduled departure hour |
| `fig5_delay_mix.png` | Delay severity mix of completed flights |
| `fig6_worst_routes.png` | Worst routes by average arrival delay |
| `fig7_airport_compare.png` | IAH against HOU on taxi-out, departure and arrival delay |
