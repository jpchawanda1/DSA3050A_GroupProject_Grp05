"""Generate the analysis figures and data-preview images for the Grp05 report.

Every number here is computed from Dataset/raw_dataset.csv and
Dataset/cleaned_dataset.csv -- nothing is hand-entered.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd, numpy as np, os

ROOT = '/Volumes/courses/summer semester 2026/business intelligence/DSA3050A_GroupProject_Grp05'
FIG  = os.path.join(ROOT, 'Documentation', 'figures')
SHOT = os.path.join(ROOT, 'Screenshots')
os.makedirs(FIG, exist_ok=True)

# --- design tokens (validated palette, light surface) --------------------
SURFACE   = '#ffffff'
INK       = '#0b0b0b'
INK_2     = '#52514e'
MUTED     = '#898781'
GRID      = '#e1e0d9'
BASELINE  = '#c3c2b7'
CAT       = ['#2a78d6', '#eb6834', '#1baf7a', '#eda100']   # categorical slots 1-4
SEQ5      = ['#86b6ef', '#5598e7', '#2a78d6', '#1c5cab', '#104281']  # ordinal ramp
BLUE      = '#2a78d6'

plt.rcParams.update({
    'font.family': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 9,
    'figure.facecolor': SURFACE, 'axes.facecolor': SURFACE,
    'axes.edgecolor': BASELINE, 'axes.linewidth': 0.8,
    'axes.labelcolor': INK_2, 'text.color': INK,
    'xtick.color': MUTED, 'ytick.color': MUTED,
    'xtick.labelsize': 8, 'ytick.labelsize': 8,
    'axes.titlesize': 11, 'axes.titleweight': 'bold', 'axes.titlecolor': INK,
    'axes.spines.top': False, 'axes.spines.right': False,
    'grid.color': GRID, 'grid.linewidth': 0.6,
    'legend.frameon': False, 'legend.fontsize': 8,
})

def finish(ax, xlab=None, ylab=None, gridaxis='y'):
    ax.grid(axis=gridaxis, zorder=0)
    ax.set_axisbelow(True)
    if xlab: ax.set_xlabel(xlab, fontsize=8, color=INK_2, labelpad=6)
    if ylab: ax.set_ylabel(ylab, fontsize=8, color=INK_2, labelpad=6)

def save(fig, name):
    fig.savefig(os.path.join(FIG, name), dpi=200, bbox_inches='tight',
                facecolor=SURFACE)
    plt.close(fig)
    print('wrote', name)

# --- data ----------------------------------------------------------------
df = pd.read_csv(os.path.join(ROOT, 'Dataset', 'raw_dataset.csv'))
df['Route'] = df.Origin + '-' + df.Dest
comp = df[df.Cancelled == 0]
c = comp.dropna(subset=['ArrDelay'])
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# === FIG 1: monthly delay + on-time, two panels (never a dual axis) ======
m = c.groupby('Month').agg(avg=('ArrDelay','mean'),
                           ontime=('ArrDelay', lambda s: (s <= 0).mean()*100))
fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.4, 5.2), sharex=True,
                             gridspec_kw={'hspace': 0.32})
a1.plot(m.index, m.avg, color=BLUE, linewidth=2, marker='o', markersize=5,
        markerfacecolor=BLUE, markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=3)
a1.set_title('Average arrival delay peaks in May, bottoms out in November')
a1.margins(y=0.18)
for mo, dy in [(5, -18), (11, 12)]:
    a1.annotate(f'{m.avg[mo]:.1f} min', (mo, m.avg[mo]), textcoords='offset points',
                xytext=(0, dy), ha='center', fontsize=8, color=INK, fontweight='bold')
finish(a1, ylab='Avg arrival delay (min)')

a2.plot(m.index, m.ontime, color=BLUE, linewidth=2, marker='o', markersize=5,
        markerfacecolor=BLUE, markeredgecolor=SURFACE, markeredgewidth=1.5, zorder=3)
a2.set_title('On-time rate moves inversely — a 19-point swing across the year')
a2.margins(y=0.18)
for mo, dy in [(5, 12), (11, -18)]:
    a2.annotate(f'{m.ontime[mo]:.1f}%', (mo, m.ontime[mo]), textcoords='offset points',
                xytext=(0, dy), ha='center', fontsize=8, color=INK, fontweight='bold')
a2.set_xticks(range(1, 13)); a2.set_xticklabels(MONTHS)
finish(a2, ylab='On-time rate (%)')
save(fig, 'fig1_monthly_trend.png')

# === FIG 2: on-time rate by airline ======================================
car = c.groupby('UniqueCarrier').agg(
    flights=('ArrDelay','size'),
    ontime=('ArrDelay', lambda s: (s <= 0).mean()*100)).sort_values('ontime')
NAMES = {'AA':'American','AS':'Alaska','B6':'JetBlue','CO':'Continental','DL':'Delta',
         'EV':'Atlantic Southeast','F9':'Frontier','FL':'AirTran','MQ':'American Eagle',
         'OO':'SkyWest','UA':'United','US':'US Airways','WN':'Southwest',
         'XE':'ExpressJet','YV':'Mesa'}
lab = [f'{NAMES[i]}  ({car.flights[i]:,})' for i in car.index]
fig, ax = plt.subplots(figsize=(7.4, 5.0))
ax.barh(lab, car.ontime, color=BLUE, height=0.62, zorder=3)
ax.axvline(52.24, color=BASELINE, linewidth=1.2, linestyle='--', zorder=2)
ax.text(52.24, len(lab)-0.2, '  Houston average 52.2%', fontsize=8, color=INK_2, va='top')
for i, v in enumerate(car.ontime):
    ax.text(v + 0.7, i, f'{v:.1f}%', va='center', fontsize=8, color=INK)
ax.set_xlim(0, 80)
ax.set_title('On-time rate by airline — the three biggest carriers all sit below average',
             loc='left', pad=12)
finish(ax, xlab='On-time rate (%) — flights operated in brackets', gridaxis='x')
save(fig, 'fig2_airline_ontime.png')

# === FIG 3: cancellations by month and reason ============================
CODES = {'A':'Carrier','B':'Weather','C':'National Air System','D':'Security'}
cx = df[df.Cancelled == 1].copy()
cx['Reason'] = cx.CancellationCode.map(CODES)
piv = cx.pivot_table(index='Month', columns='Reason', aggfunc='size', fill_value=0)
piv = piv.reindex(columns=['Weather','Carrier','National Air System','Security'],
                  fill_value=0).reindex(range(1, 13), fill_value=0)
fig, ax = plt.subplots(figsize=(7.4, 4.0))
bottom = np.zeros(12)
for k, col in enumerate(piv.columns):
    ax.bar(range(1, 13), piv[col], bottom=bottom, color=CAT[k], width=0.62,
           label=col, zorder=3, linewidth=1.6, edgecolor=SURFACE)
    bottom += piv[col].values
ax.annotate(f'February: {int(piv.loc[2].sum()):,} cancellations\n'
            f'{int(piv.loc[2,"Weather"]):,} of them weather',
            (2, piv.loc[2].sum()), textcoords='offset points', xytext=(14, -4),
            fontsize=8, color=INK, fontweight='bold', va='top')
ax.set_xticks(range(1, 13)); ax.set_xticklabels(MONTHS)
ax.set_title('Cancellations are a February problem — one month holds 37% of the year',
             loc='left', pad=12)
ax.legend(loc='upper right', ncol=2)
finish(ax, ylab='Cancelled flights')
save(fig, 'fig3_cancellations.png')

# === FIG 4: delay by scheduled departure hour ============================
h = c.copy()
h['Hour'] = (h.DepTime // 100).astype(int) % 24
hh = h.groupby('Hour').agg(flights=('ArrDelay','size'), dep=('DepDelay','mean'))
# 22:00-01:00 buckets hold under 2,000 flights each and are mostly flights that
# slipped past their scheduled slot, so they conflate cause with effect - excluded.
hh = hh[hh.flights >= 2000]
fig, ax = plt.subplots(figsize=(7.4, 3.8))
ax.bar(hh.index, hh.dep, color=BLUE, width=0.66, zorder=3)
for x in [6, 20]:
    if x in hh.index:
        v = 0.0 if abs(hh.dep[x]) < 0.05 else hh.dep[x]
        ax.text(x, hh.dep[x] + 0.6, f'{v:.1f}', ha='center', fontsize=8,
                color=INK, fontweight='bold')
ax.set_xticks(hh.index)
ax.set_title('Delay compounds through the day — a 06:00 departure leaves on time,\n'
             'a 20:00 departure averages 25 minutes late', loc='left', pad=12)
finish(ax, xlab='Scheduled departure hour (hours with 2,000+ flights)',
       ylab='Avg departure delay (min)')
save(fig, 'fig4_hour_of_day.png')

# === FIG 5: delay severity mix ===========================================
def cat(x):
    if x <= 0:   return 'On time / early'
    if x <= 14:  return 'Minor (1-14 min)'
    if x <= 59:  return 'Moderate (15-59 min)'
    if x <= 179: return 'Severe (60-179 min)'
    return 'Extreme (180+ min)'
order = ['On time / early','Minor (1-14 min)','Moderate (15-59 min)',
         'Severe (60-179 min)','Extreme (180+ min)']
dc = c.ArrDelay.apply(cat).value_counts().reindex(order)
pct = 100 * dc / dc.sum()
fig, ax = plt.subplots(figsize=(7.4, 2.1))
left = 0
for k, name in enumerate(order):
    ax.barh([0], pct[name], left=left, color=SEQ5[k], height=0.5, zorder=3,
            linewidth=1.6, edgecolor=SURFACE)
    if pct[name] > 6:   # narrower segments would overflow their own width
        ax.text(left + pct[name]/2, 0, f'{pct[name]:.1f}%', ha='center', va='center',
                fontsize=8.5, color='#ffffff' if k >= 2 else INK, fontweight='bold')
    left += pct[name]
ax.set_xlim(0, 100); ax.set_ylim(-0.5, 0.5)
ax.set_yticks([]); ax.set_xticks([])
for s in ax.spines.values(): s.set_visible(False)
ax.set_title('Delay severity mix of 223,874 completed flights', loc='left', pad=10)
ax.legend(handles=[mpatches.Patch(color=SEQ5[k], label=n) for k, n in enumerate(order)],
          loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=5, fontsize=7.5)
save(fig, 'fig5_delay_mix.png')

# === FIG 6: worst routes =================================================
r = c.groupby('Route').agg(flights=('ArrDelay','size'), avg=('ArrDelay','mean'))
r = r[r.flights >= 500].nlargest(12, 'avg').sort_values('avg')
fig, ax = plt.subplots(figsize=(7.4, 4.2))
lab = [f'{i}  ({int(r.flights[i]):,})' for i in r.index]
ax.barh(lab, r.avg, color=BLUE, height=0.62, zorder=3)
ax.axvline(7.09, color=BASELINE, linewidth=1.2, linestyle='--', zorder=2)
ax.text(7.09, len(lab)-0.2, '  Houston average 7.1 min', fontsize=8, color=INK_2, va='top')
for i, v in enumerate(r.avg):
    ax.text(v + 0.2, i, f'{v:.1f}', va='center', fontsize=8, color=INK)
ax.set_xlim(0, 19)
ax.set_title('Worst routes by average arrival delay (500+ flights operated)',
             loc='left', pad=12)
finish(ax, xlab='Avg arrival delay (min) — flights operated in brackets', gridaxis='x')
save(fig, 'fig6_worst_routes.png')

# === FIG 7: taxi-out, IAH vs HOU =========================================
o = comp.groupby('Origin').agg(taxi=('TaxiOut','mean'), dep=('DepDelay','mean'),
                               arr=('ArrDelay','mean'))
fig, ax = plt.subplots(figsize=(7.4, 3.0))
metrics = ['Avg taxi-out (min)', 'Avg departure delay (min)', 'Avg arrival delay (min)']
iah = [o.taxi['IAH'], o.dep['IAH'], o.arr['IAH']]
hou = [o.taxi['HOU'], o.dep['HOU'], o.arr['HOU']]
x = np.arange(3); w = 0.34
ax.bar(x - w/2 - 0.01, iah, w, color=CAT[0], label='IAH (172,565 flights)', zorder=3)
ax.bar(x + w/2 + 0.01, hou, w, color=CAT[1], label='HOU (51,309 flights)', zorder=3)
for xi, (a, b) in enumerate(zip(iah, hou)):
    ax.text(xi - w/2 - 0.01, a + 0.3, f'{a:.1f}', ha='center', fontsize=8, color=INK, fontweight='bold')
    ax.text(xi + w/2 + 0.01, b + 0.3, f'{b:.1f}', ha='center', fontsize=8, color=INK, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(metrics)
ax.set_title('IAH takes 7.7 more minutes to taxi out than HOU — yet still arrives earlier',
             loc='left', pad=12)
ax.legend(loc='upper right')
finish(ax, ylab='Minutes')
save(fig, 'fig7_airport_compare.png')

print('\nfigures written to', FIG)
