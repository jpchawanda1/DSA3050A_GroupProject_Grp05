"""Render data-preview and column-profiling images straight from the CSV files.

These are faithful renderings of the actual files in Dataset/ -- they are NOT
Power BI screen captures, and each one says so in its caption.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd, numpy as np, os

ROOT = '/Volumes/courses/summer semester 2026/business intelligence/DSA3050A_GroupProject_Grp05'
SHOT = os.path.join(ROOT, 'Screenshots')

SURFACE, INK, INK_2, MUTED = '#ffffff', '#0b0b0b', '#52514e', '#898781'
GRID, HEAD = '#e1e0d9', '#eef4fc'
plt.rcParams.update({'font.family': ['Helvetica', 'Arial', 'DejaVu Sans']})


def table_image(df, path, title, caption, colw=None, fontsize=6.2, rowh=0.26):
    n_rows, n_cols = df.shape
    width = sum(colw) if colw else n_cols * 1.0
    fig, ax = plt.subplots(figsize=(width, 1.15 + n_rows * rowh))
    ax.axis('off')
    tbl = ax.table(cellText=df.astype(str).values, colLabels=df.columns,
                   cellLoc='left', colLoc='left', loc='upper center',
                   colWidths=[c / width for c in colw] if colw else None)
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(fontsize)
    for (r, c), cell in tbl.get_celld().items():
        cell.set_edgecolor(GRID)
        cell.set_linewidth(0.5)
        cell.set_height(rowh / (1.15 + n_rows * rowh) * 1.55)
        cell.PAD = 0.04
        if r == 0:
            cell.set_facecolor(HEAD)
            cell.set_text_props(weight='bold', color=INK, fontsize=fontsize)
        else:
            cell.set_facecolor(SURFACE if r % 2 else '#fafafa')
            cell.set_text_props(color=INK_2)
    ax.set_title(title, loc='left', fontsize=11, fontweight='bold', color=INK, pad=22)
    ax.text(0, 1.012, caption, transform=ax.transAxes, fontsize=7.4, color=MUTED,
            va='bottom')
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor=SURFACE)
    plt.close(fig)
    print('wrote', os.path.basename(path))


# --- 1. raw data preview -------------------------------------------------
raw = pd.read_csv(os.path.join(ROOT, 'Dataset', 'raw_dataset.csv'), nrows=14)
raw_disp = raw.copy()
for c in raw_disp.columns:
    if raw_disp[c].dtype == float:
        raw_disp[c] = raw_disp[c].map(lambda v: '' if pd.isna(v) else f'{v:g}')
raw_disp = raw_disp.fillna('')
table_image(
    raw_disp, os.path.join(SHOT, 'raw_data.png'),
    'Raw dataset — 227,496 rows x 21 columns, before any cleaning',
    'Rendered directly from Dataset/raw_dataset.csv (first 14 rows). Note the blank '
    'CancellationCode, HHMM times stored as numbers, and 0/1 flag columns.',
    colw=[0.42,0.46,0.68,0.62,0.55,0.5,0.75,0.6,0.6,0.85,0.5,0.52,0.56,0.48,0.42,0.5,0.45,0.52,0.55,0.85,0.5],
    fontsize=5.6)

# --- 2. cleaned data preview --------------------------------------------
cl = pd.read_csv(os.path.join(ROOT, 'Dataset', 'cleaned_dataset.csv'), nrows=14)
show = ['Flight Date','Month Name','Quarter','Season','Day of Week','Airline',
        'Aircraft ID','Route','Distance Band','Departure Time','Time of Day',
        'Departure Delay','Arrival Delay','Delay Category','Flight Status',
        'Cancellation Reason']
table_image(
    cl[show].fillna(''), os.path.join(SHOT, 'cleaned_data.png'),
    'Cleaned dataset — 227,496 rows x 32 columns after Power Query transformation',
    'Rendered directly from Dataset/cleaned_dataset.csv (first 14 rows, 16 of 32 columns '
    'shown). Codes are decoded to names, times are real clock values, and the derived '
    'business categories are in place.',
    colw=[0.85,0.78,0.52,0.58,0.75,1.25,0.68,0.65,0.8,0.88,0.68,0.92,0.82,0.85,0.72,1.15],
    fontsize=6.0)

# --- 3. column profiling -------------------------------------------------
raw_full = pd.read_csv(os.path.join(ROOT, 'Dataset', 'raw_dataset.csv'))
rows = []
for col in raw_full.columns:
    s = raw_full[col]
    nulls = int(s.isna().sum())
    if pd.api.types.is_numeric_dtype(s):
        lo, hi = s.min(), s.max()
        rng = f'{lo:g} to {hi:g}'
    else:
        vals = s.dropna().astype(str)
        rng = f'{sorted(vals.unique())[0]} to {sorted(vals.unique())[-1]}' if len(vals) else ''
    rows.append([col, str(s.dtype), f'{nulls:,}', f'{100*nulls/len(s):.2f}%',
                 f'{s.nunique():,}', rng])
prof = pd.DataFrame(rows, columns=['Column','Detected type','Null count','Null %',
                                   'Distinct values','Value range'])
table_image(
    prof, os.path.join(SHOT, 'column_profiling.png'),
    'Column profile of the raw dataset (all 21 columns)',
    'Computed from Dataset/raw_dataset.csv. This is the profile that drove the cleaning '
    'plan: CancellationCode is 98.69% null by design, and the delay/time columns carry '
    'the cancelled and diverted flights as nulls.',
    colw=[1.75,1.15,0.95,0.75,1.15,2.4], fontsize=7.0, rowh=0.30)
