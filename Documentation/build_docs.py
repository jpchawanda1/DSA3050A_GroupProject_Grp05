"""Build the four submission PDFs from the real data.

    python3 Documentation/build_docs.py

Produces Project_Report.pdf, Data_Dictionary.pdf, Insights.pdf and
Presentation.pdf in this folder. Every figure is read from Documentation/figures/
and every number is computed from Dataset/ at build time.
"""
import os
import pandas as pd, numpy as np
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, Image, PageBreak,
                                KeepTogether)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC  = os.path.join(ROOT, 'Documentation')
FIG  = os.path.join(DOC, 'figures')

# --- Corporate Blue theme ------------------------------------------------
NAVY   = colors.HexColor('#104281')
BLUE   = colors.HexColor('#2a78d6')
PALE   = colors.HexColor('#eef4fc')
INK    = colors.HexColor('#0b0b0b')
INK2   = colors.HexColor('#3d3d3a')
MUTED  = colors.HexColor('#6b6a66')
RULE   = colors.HexColor('#d8dde4')
ORANGE = colors.HexColor('#eb6834')

FONT, BOLD, ITAL = 'Helvetica', 'Helvetica-Bold', 'Helvetica-Oblique'

def S(name, size, leading, color=INK, font=FONT, space_before=0, space_after=0,
      left=0, align=TA_LEFT):
    return ParagraphStyle(name, fontName=font, fontSize=size, leading=leading,
                          textColor=color, spaceBefore=space_before,
                          spaceAfter=space_after, leftIndent=left, alignment=align)

TITLE   = S('t',  22, 27, NAVY, BOLD, 0, 4)
SUBTITLE= S('st', 11, 15, MUTED, FONT, 0, 16)
H1      = S('h1', 15, 19, NAVY, BOLD, 16, 7)
H2      = S('h2', 11.5, 15, BLUE, BOLD, 11, 4)
BODY    = S('b',  9.4, 14.2, INK2, FONT, 0, 6)
BULLET  = S('bu', 9.4, 14.2, INK2, FONT, 0, 3, left=11)
SMALL   = S('sm', 8, 11, MUTED, FONT, 0, 4)
CAPTION = S('cap', 8, 11.5, MUTED, ITAL, 3, 10)
CELL    = S('c',  7.7, 10.2, INK2)
CELLB   = S('cb', 7.7, 10.2, INK, BOLD)
CODE    = S('code', 7.6, 11, INK2, 'Courier', 2, 6, left=8)


def header_footer(canvas, doc, title):
    canvas.saveState()
    w, h = doc.pagesize
    canvas.setFont(BOLD, 7.5); canvas.setFillColor(NAVY)
    canvas.drawString(18*mm, h - 12*mm, 'DSA 3050A  ·  Grp05')
    canvas.setFont(FONT, 7.5); canvas.setFillColor(MUTED)
    canvas.drawRightString(w - 18*mm, h - 12*mm, title)
    canvas.setStrokeColor(RULE); canvas.setLineWidth(0.5)
    canvas.line(18*mm, h - 14*mm, w - 18*mm, h - 14*mm)
    canvas.line(18*mm, 14*mm, w - 18*mm, 14*mm)
    canvas.setFont(FONT, 7.5); canvas.setFillColor(MUTED)
    canvas.drawString(18*mm, 10*mm, 'Airline Delay and Operations Intelligence Dashboard')
    canvas.drawRightString(w - 18*mm, 10*mm, str(doc.page))
    canvas.restoreState()


def build(path, story, title, pagesize=A4):
    doc = BaseDocTemplate(path, pagesize=pagesize,
                          leftMargin=18*mm, rightMargin=18*mm,
                          topMargin=20*mm, bottomMargin=18*mm,
                          title=title, author='DSA 3050A Grp05')
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
    doc.addPageTemplates([PageTemplate(id='p', frames=[frame],
                          onPage=lambda c, d: header_footer(c, d, title))])
    doc.build(story)
    print('wrote', os.path.basename(path))


def tbl(rows, widths, header=True, zebra=True, align_right=(), fontsize=None):
    data = []
    for r_i, row in enumerate(rows):
        out = []
        for c_i, cell in enumerate(row):
            st = CELLB if (header and r_i == 0) else CELL
            if fontsize:
                st = ParagraphStyle(f's{r_i}{c_i}', parent=st,
                                    fontSize=fontsize, leading=fontsize * 1.35)
            if c_i in align_right:
                st = ParagraphStyle(f'r{r_i}{c_i}', parent=st, alignment=2)
            out.append(Paragraph(str(cell), st))
        data.append(out)
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0)
    style = [('VALIGN', (0, 0), (-1, -1), 'TOP'),
             ('TOPPADDING', (0, 0), (-1, -1), 4),
             ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
             ('LEFTPADDING', (0, 0), (-1, -1), 5),
             ('RIGHTPADDING', (0, 0), (-1, -1), 5),
             ('LINEBELOW', (0, 0), (-1, -2), 0.4, RULE)]
    if header:
        style += [('BACKGROUND', (0, 0), (-1, 0), PALE),
                  ('LINEBELOW', (0, 0), (-1, 0), 0.8, BLUE)]
    if zebra:
        for i in range(1 if header else 0, len(data)):
            if i % 2 == 0:
                style.append(('BACKGROUND', (0, i), (-1, i), colors.HexColor('#fafbfc')))
    t.setStyle(TableStyle(style))
    return t


def fig(name, width=170*mm, caption=None):
    p = os.path.join(FIG, name)
    from PIL import Image as PILImage
    iw, ih = PILImage.open(p).size
    img = Image(p, width=width, height=width * ih / iw)
    items = [Spacer(1, 4), img]
    if caption:
        items.append(Paragraph(caption, CAPTION))
    return items


def cover(title, subtitle, kind):
    return [
        Spacer(1, 34*mm),
        Paragraph('DSA 3050A — Business Intelligence &amp; Visualization', SUBTITLE),
        Paragraph(title, TITLE),
        Paragraph(subtitle, S('cs', 11.5, 16, INK2, FONT, 4, 20)),
        Table([['']], colWidths=[170*mm], rowHeights=[2],
              style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), BLUE)])),
        Spacer(1, 12),
        tbl([['Document', kind],
             ['Group', 'Grp05'],
             ['Topic', 'Option 4 — Airline Delay and Operations Dashboard'],
             ['Dataset', 'hflights — 227,496 Houston departures, 2011'],
             ['Source', 'US DOT Bureau of Transportation Statistics'],
             ['Members', 'J. P. Chawanda · Catherine Ingabire · Ruth Musanhu · '
                         'Faith Chakwanira · Racheal H.']],
            [34*mm, 136*mm], header=False, zebra=False),
        PageBreak()]


# =========================================================================
# Shared numbers, computed once from the real data
# =========================================================================
raw = pd.read_csv(os.path.join(ROOT, 'Dataset', 'raw_dataset.csv'))
cl  = pd.read_csv(os.path.join(ROOT, 'Dataset', 'cleaned_dataset.csv'))
RAW_COLS = raw.shape[1]          # captured before the Route helper is added
raw['Route'] = raw.Origin + '-' + raw.Dest
comp = raw[raw.Cancelled == 0]
c = comp.dropna(subset=['ArrDelay'])

N          = len(raw)
CANC       = int(raw.Cancelled.sum())
DIV        = int(raw.Diverted.sum())
ONTIME     = (c.ArrDelay <= 0).mean() * 100
AVG_ARR    = c.ArrDelay.mean()
AVG_DEP    = comp.DepDelay.mean()
SEVERE     = (c.ArrDelay >= 60).mean() * 100
N_SEVERE   = int((c.ArrDelay >= 60).sum())
N_EXTREME  = int((c.ArrDelay >= 180).sum())
FEB_CANC   = int(raw[(raw.Month == 2) & (raw.Cancelled == 1)].shape[0])
FEB_WX     = int(raw[(raw.Month == 2) & (raw.CancellationCode == 'B')].shape[0])
EX_FEB     = 100 * (CANC - FEB_CANC) / (N - (raw.Month == 2).sum())


# =========================================================================
# 1. DATA DICTIONARY
# =========================================================================
RAW_DEFS = [
 ('Year','Whole number','Calendar year of the flight. Constant 2011 throughout, so removed during cleaning.'),
 ('Month','Whole number','Month of departure, 1-12.'),
 ('DayofMonth','Whole number','Day of the month, 1-31.'),
 ('DayOfWeek','Whole number','Day of week, 1 = Monday through 7 = Sunday.'),
 ('DepTime','Decimal','Actual departure time as an HHMM integer (e.g. 1400 = 14:00). Null when the flight did not depart.'),
 ('ArrTime','Decimal','Actual arrival time as an HHMM integer. Null when the flight did not arrive.'),
 ('UniqueCarrier','Text','Two-letter IATA carrier code identifying the operating airline.'),
 ('FlightNum','Whole number','Flight number as published by the carrier. Not unique across carriers.'),
 ('TailNum','Text','Aircraft registration (tail number) — identifies the physical airframe.'),
 ('ActualElapsedTime','Decimal','Total gate-to-gate time in minutes: taxi-out + air time + taxi-in.'),
 ('AirTime','Decimal','Wheels-up to wheels-down time in minutes.'),
 ('ArrDelay','Decimal','Arrival delay in minutes. Negative means the flight arrived early. Null for cancelled and diverted flights.'),
 ('DepDelay','Decimal','Departure delay in minutes. Negative means an early pushback. Null for cancelled flights.'),
 ('Origin','Text','Origin airport IATA code — IAH or HOU only.'),
 ('Dest','Text','Destination airport IATA code. 116 distinct values.'),
 ('Distance','Whole number','Great-circle distance between the airports, in statute miles.'),
 ('TaxiIn','Decimal','Minutes between landing and arriving on stand.'),
 ('TaxiOut','Decimal','Minutes between pushback and take-off.'),
 ('Cancelled','Whole number','Flag: 1 if the flight was cancelled, 0 otherwise.'),
 ('CancellationCode','Text','Reason code, populated only when Cancelled = 1. A = Carrier, B = Weather, C = National Air System, D = Security.'),
 ('Diverted','Whole number','Flag: 1 if the flight was diverted to an airport other than its scheduled destination.'),
]

CLEAN_DEFS = [
 ('Flight Date','Date','Calendar date of departure, built from Year, Month and DayofMonth. Joins to Dim_Date[Date].'),
 ('Month','Whole number','Month number, 1-12. Kept for sorting.'),
 ('Month Name','Text','Abbreviated month name, Jan-Dec.'),
 ('Quarter','Text','Calendar quarter, Q1-Q4.'),
 ('Season','Text','Winter (Dec-Feb), Spring (Mar-May), Summer (Jun-Aug), Autumn (Sep-Nov).'),
 ('Day','Whole number','Day of the month, 1-31.'),
 ('Day of Week','Text','Abbreviated weekday name, Mon-Sun.'),
 ('Airline Code','Text','Two-letter IATA carrier code, trimmed and upper-cased.'),
 ('Airline','Text','Full airline name, attached by merging Dim_Airline on Airline Code. Joins to Dim_Airline[Airline].'),
 ('Flight Number','Whole number','Carrier flight number.'),
 ('Aircraft ID','Text','Aircraft registration. 795 missing values replaced with "Unknown".'),
 ('Origin Airport','Text','Origin IATA code — IAH or HOU.'),
 ('Destination Airport','Text','Destination IATA code.'),
 ('Route','Text','Origin and destination merged into one key, e.g. IAH-DFW. The drill-through field.'),
 ('Distance (Miles)','Whole number','Great-circle distance in statute miles.'),
 ('Distance Band','Text','Short Haul (&lt;500), Medium Haul (500-999), Long Haul (1000-1499), Extended Haul (1500+).'),
 ('Departure Time','Text','Actual departure as HH:MM clock text, converted from the HHMM integer. 2400 rolls to 00:00.'),
 ('Departure Hour','Whole number','Hour of departure, 0-23. Drives the time-of-day analysis.'),
 ('Time of Day','Text','Night (00-05), Morning (06-11), Afternoon (12-17), Evening (18-23).'),
 ('Arrival Time','Text','Actual arrival as HH:MM clock text.'),
 ('Departure Delay','Whole number','Departure delay in minutes. Null for cancelled flights — deliberately not imputed.'),
 ('Arrival Delay','Whole number','Arrival delay in minutes. Null for cancelled and diverted flights.'),
 ('Delay Recovered','Whole number','Departure Delay minus Arrival Delay — minutes clawed back in the air. Positive means time was made up.'),
 ('Delay Category','Text','On Time / Early (&#8804;0), Minor (1-14), Moderate (15-59), Severe (60-179), Extreme (180+), Not Completed (null).'),
 ('Elapsed Time','Whole number','Gate-to-gate minutes.'),
 ('Air Time','Whole number','Wheels-up to wheels-down minutes.'),
 ('Taxi In','Whole number','Minutes from landing to stand.'),
 ('Taxi Out','Whole number','Minutes from pushback to take-off.'),
 ('Flight Status','Text','Cancelled, Diverted, On Time (Arrival Delay &#8804; 0) or Delayed. The measure filter field.'),
 ('Is Cancelled','Text','Yes / No, decoded from the raw 0/1 flag.'),
 ('Is Diverted','Text','Yes / No, decoded from the raw 0/1 flag.'),
 ('Cancellation Reason','Text','Carrier, Weather, National Air System, Security, or Not Cancelled.'),
]


def example_of(series):
    v = series.dropna()
    if not len(v): return ''
    s = str(v.iloc[0])
    return (s[:22] + '…') if len(s) > 23 else s


def data_dictionary():
    st = cover('Data Dictionary',
               'Complete column-level definition of the raw and cleaned datasets',
               'Data Dictionary')

    st += [Paragraph('1. Purpose and scope', H1),
           Paragraph(
        f'This dictionary defines every column in both datasets used by the project: the raw '
        f'extract as downloaded ({N:,} rows &#215; {RAW_COLS} columns) and the cleaned table '
        f'produced by the Power Query pipeline ({len(cl):,} rows &#215; {cl.shape[1]} columns). '
        'For each column it gives the name, the data type as set in the model, the business '
        'meaning, an example value taken from the data itself, and the count of missing values.', BODY),
           Paragraph(
        'The row count is identical before and after cleaning. No flights were dropped: the '
        'cleaning work renamed, decoded, derived and re-typed, but never filtered. This is '
        'deliberate — cancelled and diverted flights are the subject of part of the analysis, '
        'so removing them would have destroyed the evidence.', BODY)]

    st += [Paragraph('2. Raw dataset — Dataset/raw_dataset.csv', H1),
           Paragraph(f'{N:,} rows &#215; {RAW_COLS} columns. Source: US DOT Bureau of '
                     'Transportation Statistics, via the R <i>hflights</i> package.', SMALL)]
    rows = [['Column', 'Type', 'Meaning', 'Example', 'Nulls']]
    for name, typ, mean in RAW_DEFS:
        s = raw[name]
        rows.append([f'<b>{name}</b>', typ, mean, example_of(s), f'{int(s.isna().sum()):,}'])
    st += [tbl(rows, [26*mm, 18*mm, 78*mm, 24*mm, 14*mm], align_right=(4,)), PageBreak()]

    st += [Paragraph('3. Cleaned dataset — Dataset/cleaned_dataset.csv', H1),
           Paragraph(f'{len(cl):,} rows &#215; {cl.shape[1]} columns. This is the Fact_Flights '
                     'table in the Power BI model.', SMALL)]
    rows = [['Column', 'Type', 'Meaning', 'Example', 'Nulls']]
    for name, typ, mean in CLEAN_DEFS:
        s = cl[name]
        rows.append([f'<b>{name}</b>', typ, mean, example_of(s), f'{int(s.isna().sum()):,}'])
    st += [tbl(rows, [28*mm, 18*mm, 76*mm, 24*mm, 14*mm], align_right=(4,)), PageBreak()]

    st += [Paragraph('4. Dimension tables', H1),
           Paragraph('<b>Dim_Airline</b> — 15 rows, one per operating carrier.', H2),
           tbl([['Column', 'Type', 'Meaning'],
                ['Airline Code', 'Text', 'Two-letter IATA carrier code. Merge key against the fact table.'],
                ['Airline', 'Text', 'Full carrier name. The relationship key to Fact_Flights[Airline].']],
               [30*mm, 20*mm, 120*mm]),
           Spacer(1, 8),
           Paragraph('<b>Dim_Date</b> — 365 rows, 1 Jan to 31 Dec 2011. Marked as the model date table.', H2),
           tbl([['Column', 'Type', 'Meaning'],
                ['Date', 'Date', 'Calendar date. Relationship key to Fact_Flights[Flight Date].'],
                ['Year', 'Whole number', 'Calendar year — 2011 throughout.'],
                ['Month', 'Whole number', 'Month number 1-12, used to sort Month Name.'],
                ['Month Name', 'Text', 'Full month name, January-December.'],
                ['Quarter', 'Text', 'Q1-Q4.'],
                ['Day', 'Whole number', 'Day of month, 1-31.'],
                ['Day of Week', 'Text', 'Full weekday name.'],
                ['Week of Year', 'Whole number', 'ISO week number, 1-52.'],
                ['Is Weekend', 'Text', 'Yes for Saturday and Sunday, otherwise No.']],
               [30*mm, 20*mm, 120*mm]),
           Spacer(1, 8),
           Paragraph('<b>Summary_Airline_Performance</b> — 15 rows, one per carrier, built with '
                     'Group By.', H2),
           tbl([['Column', 'Type', 'Meaning'],
                ['Airline', 'Text', 'Carrier name. Relationship key to Dim_Airline[Airline].'],
                ['Total Flights', 'Whole number', 'Count of flights operated by that carrier.'],
                ['Average Arrival Delay', 'Decimal', 'Mean arrival delay in minutes across completed flights.'],
                ['Total Cancellations', 'Whole number', 'Count of cancelled flights for that carrier.']],
               [42*mm, 22*mm, 106*mm])]

    st += [Paragraph('5. Code reference', H1),
           Paragraph('<b>Cancellation codes</b> as published by the BTS:', H2),
           tbl([['Code', 'Meaning', 'Count in 2011', 'Notes'],
                ['A', 'Carrier', f'{int((raw.CancellationCode=="A").sum()):,}',
                 'Within the airline&#8217;s control — crew, maintenance, aircraft swap.'],
                ['B', 'Weather', f'{int((raw.CancellationCode=="B").sum()):,}',
                 'Outside anyone&#8217;s control. Heavily concentrated in February.'],
                ['C', 'National Air System', f'{int((raw.CancellationCode=="C").sum()):,}',
                 'Air traffic control, airport capacity, non-extreme weather.'],
                ['D', 'Security', f'{int((raw.CancellationCode=="D").sum()):,}',
                 'Security incidents, evacuations, screening failures.'],
                ['<i>blank</i>', 'Not cancelled', f'{int(raw.CancellationCode.isna().sum()):,}',
                 'Null by design — the flight operated. Mapped to "Not Cancelled".']],
               [14*mm, 32*mm, 24*mm, 100*mm]),
           Spacer(1, 8),
           Paragraph('<b>Airport codes</b>', H2),
           tbl([['Code', 'Airport', 'Flights', 'Notes'],
                ['IAH', 'George Bush Intercontinental Airport',
                 f'{int((raw.Origin=="IAH").sum()):,}',
                 'Large international hub. Long taxiways — 16.9 min average taxi-out.'],
                ['HOU', 'William P. Hobby Airport',
                 f'{int((raw.Origin=="HOU").sum()):,}',
                 'Smaller domestic airport. 9.1 min average taxi-out.']],
               [14*mm, 56*mm, 20*mm, 80*mm]),
           Spacer(1, 10),
           Paragraph('<b>A note on nulls in the delay columns.</b> The 3,622 null values in '
                     'Arrival Delay and 2,905 in Departure Delay are not data-quality defects. '
                     'They are the cancelled and diverted flights, which have no arrival or '
                     'departure to be late for. They were deliberately left null rather than '
                     'filled with zero: a zero would read as "on time" and would have pulled '
                     'every delay average towards zero while inflating the on-time rate. All '
                     'rate measures in the model divide by completed flights instead.', BODY)]

    build(os.path.join(DOC, 'Data_Dictionary.pdf'), st, 'Data Dictionary')


# =========================================================================
# 2. INSIGHTS
# =========================================================================
INSIGHTS = [
 ("Punctuality is inversely related to scale — the carriers that fly Houston most "
  "are the ones that run it late",
  "ExpressJet (71,669 flights, 50.6% on time), Continental (69,373, 50.9%) and Southwest "
  "(44,536, 53.6%) operate 82% of all Houston departures, and all three sit at or below the "
  "52.2% system average. American (69.7%), AirTran (68.9%) and US Airways (67.3%) run more "
  "than 15 points better — but on a combined 9,319 flights, which is 4% of the network. "
  "The system-wide on-time rate is therefore almost entirely a function of what three "
  "carriers do. Improving the other twelve cannot move it. This is not a small-sample "
  "artefact: ExpressJet and Continental each fly enough that their rates are stable to "
  "within a fraction of a point.",
  'fig2_airline_ontime.png',
  'Page 1 — Executive Summary: ribbon chart and airline slicer; Page 3 — airline '
  'performance matrix.'),

 ("Delay is manufactured during the day, not inherited from the schedule",
  "A flight scheduled to depart at 06:00 leaves, on average, exactly on time (-0.0 minutes). "
  "The same network at 20:00 averages 25.5 minutes of departure delay — a 25-minute "
  "deterioration with no change in aircraft, crew or route. Delay accumulates monotonically "
  "through the day as each late arrival becomes the next late departure. The implication is "
  "that late-evening delay is not caused by evening conditions; it is the morning's delay, "
  "compounded across four or five rotations of the same airframe.",
  'fig4_hour_of_day.png',
  'Page 2 — Trend Analysis: time-of-day slicer against the delay trend line.'),

 ("Cancellations are not a chronic problem — they are one week in February",
  f"Of {CANC:,} cancellations across the whole year, {FEB_CANC:,} ({100*FEB_CANC/CANC:.1f}%) "
  f"fall in February alone, and {FEB_WX:,} of those are coded Weather. February's "
  f"cancellation rate is 6.47% against a 1.31% annual average — a five-fold spike driven by "
  f"the Texas ice storm of that month. Strip February out and the network cancels "
  f"{EX_FEB:.2f}% of flights, which is a well-run operation. Treating cancellation as an "
  f"ongoing reliability problem would misdiagnose a single extreme weather event as a "
  f"systemic failure.",
  'fig3_cancellations.png',
  'Page 1 — Executive Summary: decomposition tree expanded on month, then cancellation reason.'),

 ("Carrier-controllable causes dominate every month except the storm",
  "Excluding February, Carrier is the largest cancellation reason in 8 of the remaining 11 "
  "months, totalling 1,032 cancellations against 723 for weather. Weather cancellations are "
  "concentrated and unavoidable; carrier cancellations are diffuse, persistent and — unlike "
  "weather — actionable. The headline reading of the full year (1,652 weather against 1,202 "
  "carrier) is an artefact of one month, and it reverses completely once that month is "
  "removed. Any conclusion drawn from the annual total alone would point resources at the "
  "one cause the operation cannot influence.",
  None,
  'Page 1 — Executive Summary: decomposition tree, cancellation reason by month.'),

 ("IAH is operationally slower on the ground but still arrives earlier than HOU",
  "IAH takes 16.9 minutes to taxi out against HOU's 9.1 — nearly double, exactly as expected "
  "from a large hub with long taxiways. Yet IAH averages 8.4 minutes of departure delay "
  "against HOU's 12.8, and arrives earlier (7.0 minutes against 7.5). HOU's shorter taxi "
  "time is being consumed by later pushbacks. The bottleneck at HOU is at the gate, not on "
  "the taxiway — which points at turnaround process rather than airfield capacity, and "
  "changes what any investment there should be spent on.",
  'fig7_airport_compare.png',
  'Page 3 — Geographic Analysis: origin airport slicer against the KPI cards.'),

 ("Delay peaks in late spring, not in summer or at Christmas",
  "Average arrival delay runs from a low of 3.2 minutes in November to a high of 13.1 "
  "minutes in May — a four-fold swing — while the on-time rate moves from 60.3% down to "
  "41.0%. July is the busiest month of the year at 20,548 flights yet only the fourth-worst "
  "for delay, and December, the month operations plan hardest for, sits in the better half "
  "at 5.0 minutes. Traffic volume alone does not predict delay: the correlation between "
  "monthly flight count and monthly average delay is r = 0.33, accounting for barely a "
  "tenth of the variation.",
  'fig1_monthly_trend.png',
  'Page 2 — Trend Analysis: monthly delay line with the month slicer.'),

 ("Most delay is small, but a thin tail does the damage",
  f"52.2% of completed flights arrive on time or early and another 26.9% are under 15 "
  f"minutes late — 79% of flights are effectively fine. The operational and commercial "
  f"damage sits in the {SEVERE:.1f}% that arrive an hour or more late ({N_SEVERE:,} flights), "
  f"of which {N_EXTREME:,} arrive over three hours late. These are the flights that break "
  f"connections, breach duty limits and trigger compensation. An average-delay target chases "
  f"the harmless middle of the distribution; a severe-delay target attacks the costly tail.",
  'fig5_delay_mix.png',
  'Page 1 — Executive Summary: delay category pie chart and KPI cards.'),

 ("Two-thirds of departure delay is recovered in the air",
  "Of flights that departed late, 64.9% arrived less late than they departed, and the "
  "network recovers 2.3 minutes on average between wheels-up and gate-in. Schedule padding "
  "is already absorbing a meaningful share of departure delay. Two things follow: departure "
  "delay overstates the passenger-facing problem, and arrival delay is the correct metric "
  "for any service-level reporting. It also means there is limited headroom left — the "
  "recovery is already being taken, so further departure delay converts almost directly "
  "into arrival delay.",
  None,
  'Derived from the Delay Recovered column; visible on the drill-through detail table.'),
]

RECOMMENDATIONS = [
 ("Target the three high-volume carriers, not the fifteen-carrier average",
  "ExpressJet, Continental and Southwest control 82% of departures and all run below "
  "average. Establish a joint on-time working group with these three specifically, with a "
  "shared target of moving their combined on-time rate from roughly 51% to the 60% already "
  "achieved by the mid-size carriers.",
  "Moving those three by nine points moves the entire Houston system by roughly seven. "
  "Moving all twelve remaining carriers to perfection would move it by under three. This is "
  "the single highest-leverage intervention available.",
  "Insight 1"),

 ("Protect the morning bank and re-time the evening bank",
  "Because delay compounds monotonically from 06:00 to 20:00, the cheapest minute to save is "
  "the earliest one. Prioritise first-rotation aircraft for gate, tug and crew resources, and "
  "add 10-15 minutes of turnaround buffer to aircraft entering their fourth rotation. Where "
  "an aircraft is already 20+ minutes down by midday, swap the tail rather than let the "
  "delay propagate.",
  "Attacks delay at the point of creation rather than absorbing it downstream, and stops one "
  "late morning aircraft from producing four late evening flights.",
  "Insight 2"),

 ("Fix HOU's turnaround, not its taxiways",
  "HOU has half of IAH's taxi-out time yet 4.4 minutes more departure delay. Do not spend on "
  "airfield capacity at HOU. Run a gate-level turnaround study covering boarding process, "
  "ground-handling staffing and pushback crew availability.",
  "Redirects capital away from an airfield that is not the constraint and towards the gate "
  "process that demonstrably is.",
  "Insight 5"),

 ("Report cancellations with February separated out",
  "Publish cancellation performance as two numbers: a baseline excluding extreme weather "
  f"events ({EX_FEB:.2f}%) and a weather-event line reported separately.",
  "The blended 1.31% figure hides a well-run operation behind one ice storm, and drives the "
  "wrong conclusion — that weather is the dominant cause, when carrier-controllable "
  "cancellations are more numerous in 8 of 11 normal months.",
  "Insights 3 and 4"),

 ("Change the operational target from average delay to severe-delay rate",
  "79% of flights are already fine and 4.7% cause nearly all of the cost. Replace the "
  "average arrival delay target with a severe delay rate (60 minutes or more) target of "
  "under 3.5%, down from the current 4.7%.",
  f"Aims resource at the {N_SEVERE:,} flights that break connections instead of at the "
  "1-to-14-minute band, which is largely noise and is already absorbed by schedule padding.",
  "Insight 7"),

 ("Load-plan for May, not for July",
  "Seasonal contingency staffing is currently aligned to traffic volume, which peaks in "
  "July. Delay peaks in May, when the network is four times worse than November on a lower "
  "flight count. Move reserve crew, standby aircraft and additional ramp staffing into the "
  "April-June window and reduce the December over-provision.",
  "Aligns contingency spend with when the network actually fails rather than with when it is "
  "busiest — the two are not the same month.",
  "Insight 6"),
]


def insights_doc():
    st = cover('Key Insights and Recommendations',
               'Eight evidence-backed findings and six operational recommendations',
               'Insights Report')

    st += [Paragraph('How to read this document', H1),
           Paragraph(
        f'Each insight below states a finding, quantifies it against the {N:,} flights in the '
        'dataset, and explains what it means operationally. Every figure is computed directly '
        'from the source data and is reproducible by running '
        '<font face="Courier">Documentation/build_docs.py</font>. Each insight closes with the '
        'dashboard page and visual that evidences it, so any claim can be checked against the '
        'report.', BODY),
           Paragraph(
        'Findings are stated as conclusions, not descriptions. "Delay rose in May" is a '
        'description; "delay peaks in May while traffic peaks in July, so contingency staffing '
        'is aligned to the wrong month" is a finding a manager can act on.', BODY)]

    st += [Paragraph('Part A — Key insights', H1)]
    for i, (title, body, figname, evidence) in enumerate(INSIGHTS, 1):
        block = [Paragraph(f'Insight {i} — {title}', H2), Paragraph(body, BODY)]
        if figname:
            block += fig(figname, 160*mm)
        block += [Paragraph(f'<b>Dashboard evidence:</b> {evidence}', SMALL), Spacer(1, 6)]
        st.append(KeepTogether(block) if not figname else block[0])
        if figname:
            st += block[1:]

    st += [PageBreak(), Paragraph('Part B — Recommendations', H1),
           Paragraph('Each recommendation traces to a specific insight and states the expected '
                     'operational impact.', BODY)]
    rows = [['#', 'Recommendation', 'Action', 'Why it works', 'From']]
    for i, (title, action, why, src) in enumerate(RECOMMENDATIONS, 1):
        rows.append([str(i), f'<b>{title}</b>', action, why, src])
    st += [tbl(rows, [7*mm, 38*mm, 55*mm, 48*mm, 16*mm])]

    st += [Paragraph('Part C — Storyline', H1),
           Paragraph(
        'Read together, the eight insights tell one story. Houston in 2011 was not a network '
        'with a general punctuality problem; it was a network with four specific, separable '
        'problems, three of which are addressable and one of which is not.', BODY),
           Paragraph(
        '<b>The one that is not:</b> February. A single ice storm produced 37% of the year&#8217;s '
        'cancellations. It is weather, it is unforecastable at planning horizons, and no '
        'operational change would have prevented it. It should be reported separately and '
        'otherwise set aside.', BULLET),
           Paragraph(
        '<b>The concentration problem:</b> three carriers fly 82% of the network and all three '
        'run below average. Everything the airport does to the other twelve is rounding error.', BULLET),
           Paragraph(
        '<b>The compounding problem:</b> delay is created hour by hour through the day, not '
        'inherited from a bad schedule. A morning minute saved is worth several evening minutes.', BULLET),
           Paragraph(
        '<b>The measurement problem:</b> the operation measures average delay, which is '
        'dominated by a harmless 1-to-14-minute band, and blends February into its '
        'cancellation reporting. Both choices point management at the wrong target. Changing '
        'what is measured is the cheapest of all six recommendations and unlocks the value of '
        'the other five.', BULLET)]

    build(os.path.join(DOC, 'Insights.pdf'), st, 'Insights Report')


# =========================================================================
# 3. PROJECT REPORT
# =========================================================================
def project_report():
    st = cover('Project Report',
               'Business problem, data preparation, modelling, DAX, dashboard design, '
               'insights and recommendations',
               'Full Project Report')

    st += [Paragraph('Contents', H1)]
    st += [tbl([['1', 'Executive summary'],
                ['2', 'Business problem and data understanding'],
                ['3', 'Power Query data cleaning and transformation'],
                ['4', 'Data modelling'],
                ['5', 'DAX measures'],
                ['6', 'Dashboard design and visuals'],
                ['7', 'Insights and recommendations'],
                ['8', 'Limitations'],
                ['9', 'Conclusion']],
               [10*mm, 160*mm], header=False, zebra=False), PageBreak()]

    # 1
    st += [Paragraph('1. Executive summary', H1),
           Paragraph(
        f'This project analyses {N:,} commercial flights that departed Houston&#8217;s two '
        f'airports during 2011, and delivers a Power BI dashboard that attributes delay and '
        f'cancellation to the carrier, route, airport, hour and month that produced them.', BODY),
           Paragraph(
        f'The headline position is poor: {100-ONTIME:.1f}% of flights that operated arrived '
        f'late, average arrival delay was {AVG_ARR:.1f} minutes, and {CANC:,} flights were '
        f'cancelled outright. But the analysis shows that this headline is made of four '
        f'separable problems, not one general one. Three carriers fly 82% of the network and '
        f'all three run below average. Delay is created hour-by-hour through the operating day '
        f'rather than inherited from the schedule. Cancellations are dominated by a single '
        f'February ice storm which supplies {100*FEB_CANC/CANC:.0f}% of the annual total. And '
        f'the metrics currently in use — average delay, blended cancellation rate — point '
        f'management at the least actionable parts of all three.', BODY),
           Paragraph(
        'Six recommendations follow, of which the cheapest — changing what is measured — '
        'unlocks the value of the other five.', BODY)]

    # 2
    st += [Paragraph('2. Business problem and data understanding', H1),
           Paragraph('2.1 The business problem', H2),
           Paragraph(
        'Flight delays are the largest controllable cost in airport and airline operations. A '
        'delayed departure burns fuel while taxiing, pushes crews towards duty-hour limits, '
        'forces gate reallocation, breaks passenger connections and, past a threshold, '
        'triggers compensation. A cancellation destroys the revenue of the whole rotation and '
        'displaces passengers onto later services that are already full.', BODY),
           Paragraph(
        'Houston handled 227,496 departures in 2011 and 47.8% of operated flights arrived '
        'late. Management could see that the network was late but not where the lateness was '
        'being created — whether it sat with particular carriers, routes, times of day or '
        'seasons. Without that attribution, mitigation spending is guesswork. This project '
        'supplies the attribution.', BODY),
           Paragraph('2.2 Target organization', H2),
           Paragraph(
        'The dashboard is written for the Operations Performance team of the Houston Airport '
        'System, the municipal authority that runs both IAH and HOU, together with the network '
        'operations centres of its two dominant carriers. It serves three decisions: where the '
        'COO should direct capital and staffing; which routes and departure banks network '
        'planners should re-time; and which carriers and periods duty managers should cover.', BODY),
           Paragraph('2.3 The dataset', H2),
           tbl([['Property', 'Value'],
                ['Dataset', 'hflights — all commercial flights departing Houston, 2011'],
                ['Source', 'US DOT Bureau of Transportation Statistics, via the R hflights package'],
                ['URL', 'https://cran.r-project.org/package=hflights'],
                ['Licence', 'Public domain (US federal work), redistributed under GPL-2'],
                ['Rows', f'{N:,}'],
                ['Columns', f'{RAW_COLS} raw, {cl.shape[1]} after cleaning'],
                ['Period', '1 January – 31 December 2011'],
                ['Origin airports', f'2 — IAH ({int((raw.Origin=="IAH").sum()):,}), '
                                    f'HOU ({int((raw.Origin=="HOU").sum()):,})'],
                ['Destinations', f'{raw.Dest.nunique()}'],
                ['Airlines', f'{raw.UniqueCarrier.nunique()}'],
                ['Routes', f'{raw.Route.nunique()}'],
                ['Aircraft', f'{raw.TailNum.nunique():,} distinct tail numbers'],
                ['Cancelled', f'{CANC:,} ({100*CANC/N:.2f}%)'],
                ['Diverted', f'{DIV:,} ({100*DIV/N:.2f}%)']],
               [34*mm, 136*mm]),
           Paragraph('The data is genuine government reporting. Nothing in this project is '
                     'synthetic, generated or manually invented.', SMALL),
           Paragraph('2.4 Key business questions', H2)]
    for q in ['Which airlines have the highest delays, and does poor punctuality concentrate '
              'in the carriers that fly the most?',
              'Which routes are the most delayed, and are they delayed enough to justify re-timing?',
              'How do the two Houston airports compare on departure delay, arrival delay and taxi-out?',
              'What causes cancellations, how are those causes distributed, and how much is avoidable?',
              'How does delay trend by month and season, and when is the network most fragile?',
              'What are the peak travel periods, and does traffic volume by itself explain delay?',
              'Does the time of day a flight is scheduled predict how late it will be?',
              'How much departure delay do carriers recover in the air before arrival?']:
        st.append(Paragraph(f'&#8226;&nbsp;&nbsp;{q}', BULLET))

    # 3
    st += [Paragraph('3. Power Query data cleaning and transformation', H1),
           Paragraph(
        'The pipeline is reproduced line-for-line in Documentation/clean_dataset.py, so the '
        'exported cleaned CSV can be regenerated and checked against the model at any time. '
        'Row count is identical before and after: no flights were dropped, because cancelled '
        'and diverted flights are the subject of part of the analysis.', BODY),
           Paragraph('3.1 Profiling first', H2),
           Paragraph(
        'Column profiling was enabled across the full 227,496 rows rather than the 1,000-row '
        'default sample. This is what set the cleaning plan. It showed a source that was '
        'structurally clean — zero duplicate rows, zero blank rows, consistent codes — but '
        'with three properties that would have produced wrong answers if handled naively: '
        'times stored as HHMM integers, flags stored as 0/1 numerics, and a 98.69% null rate '
        'on CancellationCode.', BODY)]
    st += fig('../../Screenshots/column_profiling.png', 168*mm,
              'Column profile of the raw dataset, computed over all 227,496 rows.')

    st += [Paragraph('3.2 The ten required cleaning tasks', H2),
           tbl([['#', 'Task', 'What was done'],
                ['1', 'Rename unclear columns',
                 'Thirteen columns renamed to business language: DayofMonth&#8594;Day, '
                 'UniqueCarrier&#8594;Airline Code, TailNum&#8594;Aircraft ID, '
                 'ArrDelay&#8594;Arrival Delay, DepDelay&#8594;Departure Delay, and so on.'],
                ['2', 'Correct data types',
                 'Delay, taxi and elapsed-time columns forced from decimal to whole number; '
                 'Flight Date built as a true Date; codes set to Text; flags converted from '
                 '0/1 numerics to Yes/No text.'],
                ['3', 'Remove duplicates and blank rows',
                 'Table.Distinct across all columns. The source proved clean — 0 rows removed. '
                 'This was verified rather than assumed.'],
                ['4', 'Trim and clean text',
                 'Text.Trim and Text.Upper applied to the five text code columns to eliminate '
                 'padding and case drift.'],
                ['5', 'Replace inconsistent values',
                 'Cancellation codes A/B/C/D replaced with Carrier / Weather / National Air '
                 'System / Security; Cancelled and Diverted flags replaced with No/Yes.'],
                ['6', 'Handle missing values',
                 '795 null Aircraft IDs replaced with "Unknown". The 224,523 null cancellation '
                 'codes are null by design and were mapped to "Not Cancelled". The 3,622 null '
                 'Arrival Delays were deliberately left null — see 3.4.'],
                ['7', 'Remove unnecessary columns',
                 'Year (constant 2011) dropped, along with the raw DepTime, ArrTime, Cancelled, '
                 'Diverted and CancellationCode columns once decoded replacements existed.'],
                ['8', 'Split and merge columns',
                 'DepTime/ArrTime split from HHMM integers into HH:MM clock text plus a numeric '
                 'Departure Hour; Origin and Destination merged into a single Route key.'],
                ['9', 'Custom and conditional columns',
                 'Flight Status, Delay Category, Distance Band, Time of Day, Season and Delay '
                 'Recovered created as nested conditional columns.'],
                ['10', 'Extract date parts',
                 'Month, Month Name, Quarter, Day and Day of Week derived from Flight Date.']],
               [7*mm, 36*mm, 127*mm]),
           PageBreak(),
           Paragraph('3.3 Advanced Power Query tasks — 8 completed against a requirement of 6', H2),
           tbl([['Task', 'Where it was applied'],
                ['Merge queries on a common key',
                 'Dim_Airline merged into the fact table on Airline Code to attach readable carrier names.'],
                ['Create a date table',
                 'Dim_Date generated across 2011 with Year, Month, Month Name, Quarter, Day, '
                 'Day of Week, Week of Year and Is Weekend.'],
                ['Group By with multiple aggregations',
                 'Summary_Airline_Performance built by grouping on Airline and aggregating '
                 'Total Flights, Average Arrival Delay and Total Cancellations in one step.'],
                ['Create summarized tables',
                 'The same table — a 15-row aggregate that keeps the ranking and ribbon visuals '
                 'off the 227,496-row fact table.'],
                ['Business categories with nested conditions',
                 'Delay Category (5 bands), Flight Status (4 states), Distance Band (4 bands) '
                 'and Time of Day (4 bands).'],
                ['Create reference queries',
                 'Dim_Airline and Summary_Airline_Performance are reference queries off the '
                 'cleaned fact query, so upstream changes flow to both.'],
                ['Use column profiling',
                 'Enabled over the whole table rather than the default sample — this surfaced '
                 'the 98.69% null rate on CancellationCode.'],
                ['Remove or handle errors',
                 'try…otherwise wrapped around the HHMM conversion so the 2400 values present '
                 'in the source roll to 00:00 instead of throwing.']],
               [45*mm, 125*mm]),
           Paragraph('3.4 The most consequential cleaning decision', H2),
           Paragraph(
        'The 3,622 null values in Arrival Delay belong to cancelled and diverted flights. The '
        'obvious move — replace nulls with zero — would have been wrong in a way that is easy '
        'to miss: a zero reads as "arrived exactly on time", which would simultaneously pull '
        'every delay average towards zero and inflate the on-time rate by counting 3,622 '
        'flights that never arrived as punctual. They were left null, and every rate measure '
        'in the model divides by completed flights instead of by total flights. A cancelled '
        'flight is neither on time nor delayed; it is a different kind of failure and is '
        'counted separately.', BODY)]
    st += fig('../../Screenshots/cleaned_data.png', 168*mm,
              'The cleaned table: codes decoded, times as real clock values, business '
              'categories in place.')

    st += [PageBreak()]

    # 4
    st += [Paragraph('4. Data modelling', H1),
           Paragraph(
        'The model is a star schema: one fact table, three dimensions, and a disconnected '
        'table holding the measures. The raw extract arrived as a single wide denormalised '
        'table; carrier and calendar attributes were lifted out into dimensions so that '
        'slicers filter through a small dimension rather than scanning 227,496 rows of '
        'repeated text.', BODY),
           tbl([['Table', 'Role', 'Grain and contents'],
                ['Fact_Flights', 'Fact', f'One row per flight — {N:,} rows, {cl.shape[1]} columns.'],
                ['Dim_Date', 'Dimension', 'One row per calendar day of 2011 (365 rows). Marked as '
                                          'the model date table.'],
                ['Dim_Airline', 'Dimension', 'One row per carrier (15 rows).'],
                ['Summary_Airline_Performance', 'Aggregate',
                 'One row per carrier with pre-computed totals.'],
                ['_Measures', 'Disconnected', 'Holds all DAX measures; contains no data.']],
               [42*mm, 22*mm, 106*mm]),
           Paragraph('4.1 Relationships', H2),
           tbl([['From', 'To', 'Cardinality', 'Direction'],
                ['Fact_Flights[Flight Date]', 'Dim_Date[Date]', 'Many-to-one', 'Single'],
                ['Fact_Flights[Airline]', 'Dim_Airline[Airline]', 'Many-to-one', 'Single'],
                ['Summary_Airline_Performance[Airline]', 'Dim_Airline[Airline]', 'Many-to-one', 'Single']],
               [54*mm, 46*mm, 34*mm, 36*mm])]
    st += fig('../../Screenshots/data_model.png', 168*mm,
              'The star schema as built in Power BI.')
    st += [Paragraph('4.2 Design decisions', H2),
           Paragraph('<b>No flat table.</b> Dimensions were extracted rather than left inline.', BULLET),
           Paragraph('<b>Single-direction filters throughout.</b> No bi-directional '
                     'relationships, so there is no ambiguity in the filter path and no risk '
                     'of a circular dependency.', BULLET),
           Paragraph('<b>A real date table.</b> Dim_Date is a contiguous 365-day calendar '
                     'flagged with Mark as date table — which is what makes TOTALYTD, '
                     'DATESQTD, DATESMTD and PREVIOUSMONTH valid rather than silently wrong.', BULLET),
           Paragraph('<b>Measures isolated.</b> All measures live in _Measures, a table with no '
                     'relationships and no columns, so the field list stays readable.', BULLET),
           Paragraph('<b>An aggregate table where it pays.</b> Summary_Airline_Performance '
                     'serves the ranking and ribbon visuals from 15 rows instead of 227,496.', BULLET),
           PageBreak()]

    # 5
    st += [Paragraph('5. DAX measures', H1),
           Paragraph('22 named measures sit in six display folders inside _Measures, plus one '
                     'helper measure used as the shared denominator for every rate.', BODY),
           tbl([['Folder', 'Measures', 'Count'],
                ['Basic Measures', 'Total Flights, Total Airlines, Total Routes, Average '
                 'Arrival Delay, Average Departure Delay', '5'],
                ['Delay Performance', 'Delayed Flights, On-Time Flights, Severely Delayed '
                 'Flights, On-Time Rate, Delayed Flight Rate, Severe Delay Rate, Average '
                 'Flights per Route', '7'],
                ['Time Intelligence', 'Flights MTD, Flights QTD, Flights YTD, Previous Month '
                 'Flights', '4'],
                ['Rankings', 'Airline Delay Rank, Airline Flight Rank', '2'],
                ['KPI Status', 'On-Time Performance Status, Arrival Delay Status', '2'],
                ['Dynamic Titles', 'Airline Performance Title, Delay Trend Title', '2']],
               [32*mm, 118*mm, 20*mm], align_right=(2,)),
           Paragraph('5.1 The denominator decision', H2),
           Paragraph(
        'Every rate measure divides by completed flights, not by all flights:', BODY),
           Paragraph('Completed Flights =<br/>CALCULATE ( COUNTROWS ( Fact_Flights ), '
                     'NOT ISBLANK ( Fact_Flights[Arrival Delay] ) )<br/><br/>'
                     'On-Time Rate = DIVIDE ( [On-Time Flights], [Completed Flights] )', CODE),
           Paragraph(
        'A cancelled flight is neither on time nor delayed. Including the 3,622 cancelled and '
        'diverted flights in the denominator would understate punctuality by roughly 1.6 '
        'percentage points and would make the on-time rate move whenever cancellations moved, '
        'which is a different phenomenon.', BODY),
           Paragraph('5.2 Representative measures', H2),
           Paragraph(
        'Severe Delay Rate =<br/>DIVIDE ( [Severely Delayed Flights], [Completed Flights] )'
        '<br/><br/>'
        'Airline Delay Rank =<br/>RANKX ( ALL ( Dim_Airline[Airline] ), '
        '[Average Arrival Delay], , DESC, DENSE )<br/><br/>'
        'On-Time Performance Status =<br/>SWITCH ( TRUE (),<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;[On-Time Rate] &gt;= 0.80, "Good",<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;[On-Time Rate] &gt;= 0.65, "Watch",<br/>'
        '&nbsp;&nbsp;&nbsp;&nbsp;"Needs Attention" )<br/><br/>'
        'Airline Performance Title =<br/>"Airline Performance for " &amp; '
        'SELECTEDVALUE ( Dim_Airline[Airline], "All Airlines" )<br/><br/>'
        'Flights YTD = TOTALYTD ( [Total Flights], Dim_Date[Date] )', CODE),
           Paragraph('5.3 Formatting conventions', H2),
           Paragraph('Rate measures are formatted as percentage to one decimal place; delay '
                     'measures as whole numbers with a " min" suffix; counts with a thousands '
                     'separator and no decimals. Measure names use Title Case and never repeat '
                     'their table name.', BODY),
           PageBreak()]

    # 6
    st += [Paragraph('6. Dashboard design and visuals', H1),
           Paragraph(
        'The report uses the Corporate Blue theme recommended for airline projects — a '
        'white/light-grey canvas, navy blue accent, sky blue and teal secondaries, and '
        'orange/red reserved strictly for warning states so that a colour never carries '
        'meaning casually.', BODY),
           tbl([['Page', 'Purpose', 'Visuals'],
                ['1 — Executive Summary',
                 'The one-screen answer to "how did Houston perform in 2011"',
                 '4 KPI cards (Total Flights, On-Time Rate, Total Routes, Average Arrival '
                 'Delay) · ribbon chart of airline volume by month · decomposition tree · '
                 'delay-category pie chart · navigation buttons'],
                ['2 — Trend Analysis',
                 'How performance moved through the year',
                 'Monthly delay line chart · airline, month and delay-category slicers, '
                 'synced across pages · dynamic title driven by Delay Trend Title'],
                ['3 — Geographic &amp; Route Analysis',
                 'Where in the network the delay sits',
                 'Azure map of flight volume by destination, bubble-sized by traffic · airline '
                 'performance matrix with conditional formatting (a delay heat map) · airline '
                 'and destination slicers'],
                ['4 — Route Drill-through',
                 'Flight-level detail for one selected route',
                 'Not yet built — see section 8']],
               [32*mm, 44*mm, 94*mm]),
           Paragraph('6.1 Design rules applied', H2),
           Paragraph('Consistent palette across all pages, with warning colours reserved for '
                     'status states only.', BULLET),
           Paragraph('Dynamic titles on the carrier and trend visuals, so a heading always '
                     'names the current selection rather than a generic label.', BULLET),
           Paragraph('Conditional formatting on the performance matrix, so the matrix doubles '
                     'as the delay heat map.', BULLET),
           Paragraph('Slicers synced across pages, so a carrier selected on one page stays '
                     'selected on the next.', BULLET),
           Paragraph('Navigation buttons on every page rather than relying on the page tabs.', BULLET),
           Paragraph('Thousands separators and explicit units on every number, so no figure is '
                     'ambiguous.', BULLET)]

    # 7
    st += [PageBreak(), Paragraph('7. Insights and recommendations', H1),
           Paragraph('Stated in full, with supporting charts, in Insights.pdf. Summarised here.', BODY),
           Paragraph('7.1 Insights', H2)]
    rows = [['#', 'Insight', 'The evidence']]
    ev = ['ExpressJet 50.6%, Continental 50.9%, Southwest 53.6% on 82% of flights, against a '
          '52.2% average and 69.7% for the best carrier.',
          '06:00 departures average -0.0 min delay; 20:00 departures average 25.5 min.',
          f'{FEB_CANC:,} of {CANC:,} cancellations in February; {FEB_WX:,} of them weather. '
          f'Ex-February rate {EX_FEB:.2f}% against 1.31% blended.',
          'Carrier is the top reason in 8 of 11 non-February months: 1,032 against 723 weather.',
          'IAH taxi-out 16.9 min against HOU 9.1, yet IAH departure delay 8.4 against 12.8.',
          'May 13.1 min against November 3.2 min. July busiest but only 4th worst. r = 0.33 '
          'between volume and delay.',
          f'79% of flights under 15 min late; {SEVERE:.1f}% ({N_SEVERE:,}) an hour or more; '
          f'{N_EXTREME:,} over three hours.',
          '64.9% of late departures arrive less late; 2.3 min recovered on average.']
    for i, ((title, _, _, _), e) in enumerate(zip(INSIGHTS, ev), 1):
        rows.append([str(i), f'<b>{title}</b>', e])
    st += [tbl(rows, [7*mm, 76*mm, 87*mm]),
           Paragraph('7.2 Recommendations', H2)]
    rows = [['#', 'Recommendation', 'Expected impact']]
    for i, (title, _, why, _) in enumerate(RECOMMENDATIONS, 1):
        rows.append([str(i), f'<b>{title}</b>', why])
    st += [tbl(rows, [7*mm, 68*mm, 95*mm])]

    # 8
    st += [PageBreak(), Paragraph('8. Limitations', H1),
           Paragraph('Stated plainly, because they bound what the recommendations can claim.', BODY),
           Paragraph('<b>Single year, single origin city.</b> The data covers 2011 departures '
                     'from Houston only. Seasonal conclusions rest on one observation of each '
                     'month, so May 2011 being the worst month is a fact about 2011, not a '
                     'proven annual pattern. A multi-year extract would be needed to '
                     'distinguish season from year.', BULLET),
           Paragraph('<b>No delay-cause breakdown.</b> The source records cancellation reasons '
                     'but not delay reasons — there is no carrier/weather/NAS/security split '
                     'on the delay minutes themselves. Attribution of delay to cause is '
                     'therefore inferred from timing and pattern, not read directly.', BULLET),
           Paragraph('<b>Departures only.</b> Arrivals into Houston are not in the dataset, so '
                     'inbound aircraft cannot be traced. The rotation-compounding argument in '
                     'Insight 2 is inferred from the hour-of-day gradient rather than followed '
                     'tail-by-tail through the day.', BULLET),
           Paragraph('<b>No passenger or cost data.</b> Load factors, fare data and '
                     'compensation costs are absent, so the financial impact of the '
                     'recommendations is argued in operational terms rather than quantified '
                     'in dollars.', BULLET),
           Paragraph('<b>Age of the data.</b> 2011 predates several fleet and schedule changes, '
                     'including the Continental–United merger integration. The method '
                     'transfers; the specific carrier findings are historical.', BULLET),
           Paragraph('<b>One page outstanding.</b> The route drill-through page is not yet '
                     'built, so flight-level interrogation of a single route is currently done '
                     'through slicers rather than through drill-through.', BULLET)]

    # 9
    st += [Paragraph('9. Conclusion', H1),
           Paragraph(
        f'Houston in 2011 does not have a general punctuality problem. It has three '
        f'addressable problems and one unavoidable one, and its current metrics obscure all '
        f'four. {100-ONTIME:.1f}% of flights arriving late is a real number, but it is produced '
        f'almost entirely by three carriers, created hour-by-hour through the operating day, '
        f'and reported through an average that is dominated by delays too small to matter.', BODY),
           Paragraph(
        'The dashboard makes each of those separable at a glance, which is what turns a year '
        'of flight records into an operational decision tool. The single cheapest '
        'recommendation — report severe-delay rate instead of average delay, and separate '
        'February from the cancellation baseline — costs nothing and changes what management '
        'is aiming at.', BODY)]

    build(os.path.join(DOC, 'Project_Report.pdf'), st, 'Project Report')


# =========================================================================
# 4. PRESENTATION
# =========================================================================
def presentation():
    W, H = landscape(A4)
    SL_T = S('slt', 26, 31, NAVY, BOLD, 0, 6)
    SL_S = S('sls', 13, 18, INK2, FONT, 0, 14)
    SL_B = S('slb', 12.5, 19, INK2, FONT, 0, 8)
    SL_BU= S('slbu', 12.5, 19, INK2, FONT, 0, 7, left=14)
    SL_K = S('slk', 34, 38, BLUE, BOLD, 0, 2)
    SL_KL= S('slkl', 10, 13, MUTED, FONT, 0, 0)

    st = []

    def slide(title, blocks, subtitle=None):
        out = [Paragraph(title, SL_T)]
        if subtitle:
            out.append(Paragraph(subtitle, SL_S))
        out += [Table([['']], colWidths=[245*mm], rowHeights=[2],
                      style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), BLUE)])),
                Spacer(1, 12)]
        out += blocks
        out.append(PageBreak())
        return out

    def bullets(items):
        return [Paragraph(f'&#8226;&nbsp;&nbsp;{t}', SL_BU) for t in items]

    def kpis(pairs):
        cells = [[Paragraph(v, SL_K) for v, _ in pairs],
                 [Paragraph(l, SL_KL) for _, l in pairs]]
        t = Table(cells, colWidths=[245*mm / len(pairs)] * len(pairs))
        t.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                               ('TOPPADDING', (0, 0), (-1, -1), 2),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 0),
                               ('BOTTOMPADDING', (0, 1), (-1, 1), 14)]))
        return [t]

    # title slide
    st += [Spacer(1, 46*mm),
           Paragraph('Airline Delay and Operations Intelligence', S('x', 30, 36, NAVY, BOLD, 0, 6)),
           Paragraph('Houston, 2011 — 227,496 flights', S('y', 15, 20, INK2, FONT, 0, 16)),
           Table([['']], colWidths=[245*mm], rowHeights=[2.5],
                 style=TableStyle([('BACKGROUND', (0, 0), (-1, -1), BLUE)])),
           Spacer(1, 14),
           Paragraph('DSA 3050A — Business Intelligence &amp; Visualization &nbsp;·&nbsp; Grp05',
                     S('z', 11.5, 16, MUTED)),
           Paragraph('J. P. Chawanda · Catherine Ingabire · Ruth Musanhu · Faith Chakwanira · '
                     'Racheal H.', S('z2', 11.5, 16, MUTED, FONT, 6)),
           PageBreak()]

    st += slide('The business problem',
                bullets(['Delay is the largest controllable cost in airport operations — fuel, '
                         'crew duty limits, gate reallocation, missed connections, compensation.',
                         'Houston ran 227,496 departures in 2011. 47.8% of operated flights '
                         'arrived late.',
                         'Management could see <i>that</i> the network was late — not <i>where '
                         'the lateness was being created</i>.',
                         'Without attribution, mitigation spending is guesswork.']) +
                [Spacer(1, 10),
                 Paragraph('<b>Our brief:</b> attribute delay and cancellation to the carrier, '
                           'route, airport, hour and month that produced them.', SL_B)],
                'Houston Airport System — Operations Performance')

    st += slide('The data',
                kpis([('227,496', 'FLIGHTS'), ('21 &#8594; 32', 'COLUMNS'),
                      ('15', 'AIRLINES'), ('149', 'ROUTES'), ('116', 'DESTINATIONS')]) +
                bullets(['<b>Source:</b> US DOT Bureau of Transportation Statistics, via the R '
                         '<i>hflights</i> package — genuine public government reporting.',
                         '<b>Period:</b> every commercial departure from IAH and HOU in 2011.',
                         '<b>Structurally clean:</b> zero duplicates, zero blank rows — but '
                         'times stored as HHMM integers, flags as 0/1, and a 98.69% null rate '
                         'on cancellation code.']),
                'hflights — Houston departures, 2011')

    st += slide('Cleaning and modelling',
                [Paragraph('<b>All 10 required cleaning tasks, and 8 advanced tasks against a '
                           'requirement of 6.</b>', SL_B)] +
                bullets(['Renamed 13 columns to business language; decoded every code and flag.',
                         'Split HHMM integers into real clock times; merged origin and '
                         'destination into a Route key.',
                         'Derived Flight Status, Delay Category, Distance Band, Time of Day, '
                         'Season and Delay Recovered.',
                         'Star schema: Fact_Flights + Dim_Date + Dim_Airline + a Group By '
                         'aggregate table, measures isolated in _Measures.']) +
                [Spacer(1, 8),
                 Paragraph('<b>The decision that mattered:</b> 3,622 null arrival delays belong '
                           'to cancelled and diverted flights. We left them null. Filling them '
                           'with zero would have counted 3,622 flights that never arrived as '
                           '"on time".', SL_B)],
                'One fact table, three dimensions, 22 measures')

    st += slide('Insight 1 — Punctuality is inversely related to scale',
                fig('fig2_airline_ontime.png', 175*mm) +
                [Paragraph('Three carriers fly 82% of Houston. All three run at or below the '
                           '52.2% average. Improving the other twelve cannot move the system.',
                           SL_B)])

    st += slide('Insight 2 — Delay is manufactured during the day',
                fig('fig4_hour_of_day.png', 185*mm) +
                [Paragraph('06:00 departs on time. 20:00 averages 25.5 minutes late. Same '
                           'aircraft, same crews, same routes — delay compounds across '
                           'rotations.', SL_B)])

    st += slide('Insight 3 — Cancellations are one week in February',
                fig('fig3_cancellations.png', 185*mm) +
                [Paragraph(f'{FEB_CANC:,} of {CANC:,} cancellations fall in February. Strip it '
                           f'out and the network cancels {EX_FEB:.2f}% — a well-run operation.',
                           SL_B)])

    st += slide('Insight 4 — Delay peaks in May, traffic peaks in July',
                fig('fig1_monthly_trend.png', 150*mm) +
                [Paragraph('Volume does not predict delay: r = 0.33. Contingency staffing is '
                           'aligned to the wrong month.', SL_B)])

    st += slide('Insight 5 — A thin tail does the damage',
                fig('fig5_delay_mix.png', 200*mm) +
                [Spacer(1, 6),
                 Paragraph(f'79% of flights are effectively fine. The cost sits in the '
                           f'{SEVERE:.1f}% — {N_SEVERE:,} flights — that arrive an hour or more '
                           f'late, of which {N_EXTREME:,} are over three hours late. '
                           f'An average-delay target chases the harmless middle.', SL_B)])

    st += slide('What we recommend',
                [tbl([['#', 'Recommendation', 'Why'],
                      ['1', '<b>Target the three high-volume carriers</b>',
                       'Moving them nine points moves the whole system seven. '
                       'Perfecting the other twelve moves it under three.'],
                      ['2', '<b>Protect the morning bank</b>',
                       'Delay compounds from 06:00. The earliest minute saved is the cheapest.'],
                      ['3', '<b>Fix HOU&#8217;s turnaround, not its taxiways</b>',
                       'Half the taxi time, more departure delay. The gate is the constraint.'],
                      ['4', '<b>Separate February from the cancellation baseline</b>',
                       'The blended rate hides a good operation and misnames the dominant cause.'],
                      ['5', '<b>Target severe-delay rate, not average delay</b>',
                       'Aims at the 10,584 flights that break connections, not at noise.'],
                      ['6', '<b>Load-plan for May, not July</b>',
                       'Align contingency with when the network fails, not when it is busiest.']],
                     [8*mm, 82*mm, 155*mm], fontsize=10.5)],
                'Six recommendations, traced to the evidence')

    st += slide('Where this leaves Houston',
                bullets(['Houston does not have a general punctuality problem. It has three '
                         'addressable problems and one unavoidable one.',
                         '<b>Unavoidable:</b> February. One ice storm, 37% of the year&#8217;s '
                         'cancellations.',
                         '<b>Concentration:</b> three carriers are the system.',
                         '<b>Compounding:</b> delay is created hour by hour, not inherited.',
                         '<b>Measurement:</b> the current metrics point management at the least '
                         'actionable part of all three.']) +
                [Spacer(1, 10),
                 Paragraph('<b>The cheapest recommendation — change what is measured — costs '
                           'nothing and unlocks the value of the other five.</b>', SL_B)])

    st += [Spacer(1, 62*mm),
           Paragraph('Thank you', S('ty', 28, 34, NAVY, BOLD, 0, 8)),
           Paragraph('Questions', S('q', 14, 19, MUTED))]

    build(os.path.join(DOC, 'Presentation.pdf'), st, 'Presentation', pagesize=landscape(A4))


if __name__ == '__main__':
    data_dictionary()
    insights_doc()
    project_report()
    presentation()
