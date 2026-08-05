"""Reference implementation of the Power Query pipeline.

Each numbered step below corresponds one-to-one with an Applied Step in the
Power Query Editor of PowerBI/GroupProject.pbix. Running this file regenerates
Dataset/cleaned_dataset.csv, Dataset/dim_airline.csv and Dataset/dim_date.csv
exactly as the .pbix produces them, so the exported CSV can always be checked
against the model.

    python3 Documentation/clean_dataset.py
"""
import pandas as pd, numpy as np, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'Dataset')

AIRLINES = {
    'AA': 'American Airlines',   'AS': 'Alaska Airlines',
    'B6': 'JetBlue Airways',     'CO': 'Continental Airlines',
    'DL': 'Delta Air Lines',     'EV': 'Atlantic Southeast Airlines',
    'F9': 'Frontier Airlines',   'FL': 'AirTran Airways',
    'MQ': 'American Eagle Airlines', 'OO': 'SkyWest Airlines',
    'UA': 'United Airlines',     'US': 'US Airways',
    'WN': 'Southwest Airlines',  'XE': 'ExpressJet Airlines',
    'YV': 'Mesa Airlines',
}
CANCEL = {'A': 'Carrier', 'B': 'Weather',
          'C': 'National Air System', 'D': 'Security'}

df = pd.read_csv(os.path.join(DATA, 'raw_dataset.csv'))

# 4. Trim and clean text columns -- Text.Trim + Text.Upper
for col in ['UniqueCarrier', 'TailNum', 'Origin', 'Dest', 'CancellationCode']:
    df[col] = df[col].astype('string').str.strip().str.upper()

# 3. Remove duplicates -- Table.Distinct (source proved clean: 0 removed)
before = len(df)
df = df.drop_duplicates()
print(f'duplicates removed: {before - len(df)}')

# 10. Extract date parts -- build a real Date from Year/Month/DayofMonth
df['Flight Date'] = pd.to_datetime(dict(year=df.Year, month=df.Month, day=df.DayofMonth))

# 8. Split columns -- HHMM integers into clock text + a numeric hour.
#    2400 rolls to 00:00 rather than throwing (step 'Remove or handle errors').
def hhmm(s):
    s = pd.to_numeric(s, errors='coerce')
    h = (s // 100).where(s.notna())
    m = (s % 100).where(s.notna())
    h = h.where(h != 24, 0)
    return (h.astype('Int64').astype('string').str.zfill(2) + ':' +
            m.astype('Int64').astype('string').str.zfill(2))

df['Departure Time'] = hhmm(df.DepTime)
df['Arrival Time']   = hhmm(df.ArrTime)
df['Departure Hour'] = (pd.to_numeric(df.DepTime, errors='coerce') // 100).mod(24).astype('Int64')

# 1. Rename unclear columns
df = df.rename(columns={
    'DayofMonth': 'Day',                 'UniqueCarrier': 'Airline Code',
    'FlightNum': 'Flight Number',        'TailNum': 'Aircraft ID',
    'ActualElapsedTime': 'Elapsed Time', 'AirTime': 'Air Time',
    'ArrDelay': 'Arrival Delay',         'DepDelay': 'Departure Delay',
    'Origin': 'Origin Airport',          'Dest': 'Destination Airport',
    'Distance': 'Distance (Miles)',      'TaxiIn': 'Taxi In',
    'TaxiOut': 'Taxi Out'})

# Advanced: merge queries on a common key -- attach readable carrier names
df['Airline'] = df['Airline Code'].map(AIRLINES)

# 5. Replace inconsistent values -- decode codes and 0/1 flags
df['Cancellation Reason'] = df.CancellationCode.map(CANCEL).fillna('Not Cancelled')
df['Is Cancelled'] = np.where(df.Cancelled == 1, 'Yes', 'No')
df['Is Diverted']  = np.where(df.Diverted == 1, 'Yes', 'No')

# 8. Merge columns -- a single route key
df['Route'] = df['Origin Airport'] + '-' + df['Destination Airport']

# 9. Custom and conditional columns -- nested business categories
def flight_status(r):
    if r.Cancelled == 1: return 'Cancelled'
    if r.Diverted == 1:  return 'Diverted'
    if pd.isna(r['Arrival Delay']): return 'Unknown'
    return 'On Time' if r['Arrival Delay'] <= 0 else 'Delayed'

df['Flight Status'] = df.apply(flight_status, axis=1)

# right-closed bins so a 0-minute arrival delay reads On Time, matching Flight Status
df['Delay Category'] = pd.cut(
    df['Arrival Delay'], bins=[-np.inf, 0, 14, 59, 179, np.inf],
    labels=['On Time / Early', 'Minor Delay', 'Moderate Delay',
            'Severe Delay', 'Extreme Delay'])
df['Delay Category'] = df['Delay Category'].cat.add_categories('Not Completed').fillna('Not Completed')

df['Distance Band'] = pd.cut(
    df['Distance (Miles)'], bins=[0, 499, 999, 1499, np.inf],
    labels=['Short Haul', 'Medium Haul', 'Long Haul', 'Extended Haul'])

df['Time of Day'] = pd.cut(
    df['Departure Hour'].astype('float'), bins=[-.1, 5.99, 11.99, 17.99, 23.99],
    labels=['Night', 'Morning', 'Afternoon', 'Evening'])

# 10. Extract date parts
df['Month Name']  = df['Flight Date'].dt.strftime('%b')
df['Quarter']     = 'Q' + df['Flight Date'].dt.quarter.astype(str)
df['Day of Week'] = df['Flight Date'].dt.strftime('%a')
df['Season'] = df.Month.map({12: 'Winter', 1: 'Winter', 2: 'Winter',
                             3: 'Spring', 4: 'Spring', 5: 'Spring',
                             6: 'Summer', 7: 'Summer', 8: 'Summer',
                             9: 'Autumn', 10: 'Autumn', 11: 'Autumn'})

# 6. Handle missing values.
#    Aircraft ID gets a placeholder; Arrival/Departure Delay nulls are LEFT null --
#    they belong to cancelled and diverted flights, and imputing them would
#    corrupt every delay average. The DAX excludes them instead.
df['Aircraft ID'] = df['Aircraft ID'].fillna('Unknown')

df['Delay Recovered'] = df['Departure Delay'] - df['Arrival Delay']

# 2. Correct data types
for c in ['Elapsed Time', 'Air Time', 'Arrival Delay', 'Departure Delay',
          'Taxi In', 'Taxi Out', 'Delay Recovered']:
    df[c] = df[c].round(0).astype('Int64')

# 7. Remove unnecessary columns
df = df.drop(columns=['Year', 'DepTime', 'ArrTime', 'CancellationCode',
                      'Cancelled', 'Diverted'])

COLS = ['Flight Date', 'Month', 'Month Name', 'Quarter', 'Season', 'Day', 'Day of Week',
        'Airline Code', 'Airline', 'Flight Number', 'Aircraft ID',
        'Origin Airport', 'Destination Airport', 'Route', 'Distance (Miles)', 'Distance Band',
        'Departure Time', 'Departure Hour', 'Time of Day', 'Arrival Time',
        'Departure Delay', 'Arrival Delay', 'Delay Recovered', 'Delay Category',
        'Elapsed Time', 'Air Time', 'Taxi In', 'Taxi Out',
        'Flight Status', 'Is Cancelled', 'Is Diverted', 'Cancellation Reason']
df[COLS].to_csv(os.path.join(DATA, 'cleaned_dataset.csv'), index=False,
                date_format='%Y-%m-%d')

# Advanced: reference query -- the carrier dimension
pd.DataFrame({'Airline Code': list(AIRLINES),
              'Airline': list(AIRLINES.values())}
             ).to_csv(os.path.join(DATA, 'dim_airline.csv'), index=False)

# Advanced: create a date table
d = pd.DataFrame({'Date': pd.date_range('2011-01-01', '2011-12-31')})
d['Year']         = d.Date.dt.year
d['Month']        = d.Date.dt.month
d['Month Name']   = d.Date.dt.strftime('%B')
d['Quarter']      = 'Q' + d.Date.dt.quarter.astype(str)
d['Day']          = d.Date.dt.day
d['Day of Week']  = d.Date.dt.day_name()
d['Week of Year'] = d.Date.dt.isocalendar().week.astype(int)
d['Is Weekend']   = np.where(d.Date.dt.dayofweek >= 5, 'Yes', 'No')
d.to_csv(os.path.join(DATA, 'dim_date.csv'), index=False, date_format='%Y-%m-%d')

print(f'cleaned_dataset.csv written: {df[COLS].shape[0]:,} rows x {df[COLS].shape[1]} columns')
