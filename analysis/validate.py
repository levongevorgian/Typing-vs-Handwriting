"""Independent statistical and artifact checks, using committed or rebuilt results."""
from pathlib import Path
import hashlib,json,csv,re
import numpy as np
import pandas as pd
from scipy import stats
P=Path(__file__).resolve().parents[1]
r=json.loads((P/'results/analysis.json').read_text());d=pd.read_csv(P/'data/laptop_urry.csv');a=d.loc[d.condition=='laptop','overall'];b=d.loc[d.condition=='longhand','overall']
assert d.shape==(142,6) and d.pid.nunique()==142 and not d.isna().any().any()
assert hashlib.sha256((P/'data/laptop_urry.csv').read_bytes()).hexdigest()==r['audit']['data_sha256']
ref=stats.ttest_ind(a,b,equal_var=False);ci=ref.confidence_interval(.95)
assert np.allclose([ref.statistic,ref.pvalue,ci.low,ci.high],[r['primary'][x] for x in ['t','p','lower','upper']])
assert np.isclose(r['primary']['estimate'],1.9917396322333332)
# A separate within-lecture centering calculation verifies the adjusted condition coefficient.
g=(d.condition=='laptop').astype(float);gc=g-g.groupby(d.talk).transform('mean');yc=d.overall-d.groupby('talk').overall.transform('mean');coef=(gc@yc)/(gc@gc)
assert np.isclose(coef,r['adjusted']['estimate'])
assert np.allclose([r['adjusted']['HC3_lower'],r['adjusted']['HC3_upper']],[-3.427464900874738,6.7343341680386635])
for z in r['tests']:
 assert z['lower']<z['estimate']<z['upper'] and ((z['lower']<=0<=z['upper'])==(z['p']>=.05))
sec=r['tests'][1:];assert all(x['holm_p']>=x['p']-1e-12 for x in sec)
assert len(r['figures'])==13
for z in r['figures']:
 for ext in ['png','svg']:assert (P/'visualizations'/f'{z["name"]}.{ext}').stat().st_size>1000
for rel in ['reports/analysis_report.pdf','reports/analysis_report.html','README.md','docs/methods.md','docs/course_mapping.md']:
 assert (P/rel).stat().st_size>100
for target in re.findall(r'(?:src|href)="([^"]+)"',(P/'reports/analysis_report.html').read_text()):
 if not target.startswith(('http','#')):assert (P/'reports'/target).exists(),target
print('PASS: data integrity, independent Welch/CI and adjusted coefficient, HC3 continuity, secondary tests, 26 figure files, report outputs and HTML links.')
