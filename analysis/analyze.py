"""Rebuild all statistical tables and standalone figures. No bootstrap methods."""
from pathlib import Path
import os, json, hashlib, platform
os.environ.setdefault('MPLCONFIGDIR','/tmp/typing-handwriting-mpl')
import numpy as np
import pandas as pd
import scipy
from scipy import stats, optimize, integrate
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parents[1]
for folder in ['results','visualizations']: (P/folder).mkdir(exist_ok=True)
d=pd.read_csv(P/'data/laptop_urry.csv')
assert d.shape==(142,6) and d.pid.nunique()==142 and not d.isna().any().any()
assert set(d.condition)=={'laptop','longhand'} and d.talk.nunique()==5
assert d[['overall','factual','conceptual']].apply(lambda s:s.between(0,100).all()).all()
d['typing']=(d.condition=='laptop').astype(int)
d['gap']=d.conceptual-d.factual
G=['laptop','longhand']; L=['Typing','Handwriting']; C=['#2563a6','#b45332']
plt.rcParams.update({'font.size':11,'axes.spines.top':False,'axes.spines.right':False,'figure.dpi':130,'savefig.bbox':'tight'})
figures=[]
def save(name,title,caption):
 fig=plt.gcf();fig.suptitle(title,fontsize=15,fontweight='bold');fig.tight_layout(rect=(0,0,1,.94))
 for ext in ['png','svg']:fig.savefig(P/'visualizations'/f'{name}.{ext}',dpi=190)
 plt.close(fig);figures.append(dict(name=name,title=title,caption=caption))
def csv(name,rows):pd.DataFrame(rows).to_csv(P/'results'/f'{name}.csv',index=False)
def welch(a,b):
 a,b=np.asarray(a),np.asarray(b);u,v=a.var(ddof=1)/len(a),b.var(ddof=1)/len(b)
 se=np.sqrt(u+v);df=(u+v)**2/(u*u/(len(a)-1)+v*v/(len(b)-1));diff=a.mean()-b.mean();t=diff/se;q=stats.t.ppf(.975,df)
 ref=stats.ttest_ind(a,b,equal_var=False);assert np.allclose([t,2*stats.t.sf(abs(t),df)],[ref.statistic,ref.pvalue])
 return dict(estimate=diff,se=se,t=t,df=df,p=ref.pvalue,lower=diff-q*se,upper=diff+q*se)
summary=[]; intervals=[]
for outcome in ['overall','factual','conceptual','gap']:
 for g,l in zip(G,L):
  a=d.loc[d.condition==g,outcome].to_numpy();n=len(a);sd=a.std(ddof=1);q1,med,q3=np.quantile(a,[.25,.5,.75]);se=sd/np.sqrt(n);tc=stats.t.ppf(.975,n-1)
  summary.append(dict(outcome=outcome,group=l,n=n,mean=a.mean(),median=med,sd=sd,variance=sd**2,se=se,min=a.min(),q1=q1,q3=q3,iqr=q3-q1,max=a.max(),skew=stats.skew(a,bias=False),outlier_flags=int(((a<q1-1.5*(q3-q1))|(a>q3+1.5*(q3-q1))).sum())))
  if outcome=='overall':
   # Exact two-sided normal tolerance factor: integrate over independent normal mean and chi-square variance.
   def coverage(k):
    def f(z):
     m=z/np.sqrt(n)
     r=optimize.brentq(lambda r:stats.norm.cdf(m+r)-stats.norm.cdf(m-r)-.90,.01,10)
     return stats.chi2.sf((n-1)*(r/k)**2,n-1)*stats.norm.pdf(z)
    return integrate.quad(f,-8,8,epsabs=1e-7)[0]
   k=optimize.brentq(lambda k:coverage(k)-.95,1,4,xtol=1e-7)
   intervals.append(dict(group=l,mean_low=a.mean()-tc*se,mean_high=a.mean()+tc*se,sd_low=np.sqrt((n-1)*sd**2/stats.chi2.ppf(.975,n-1)),sd_high=np.sqrt((n-1)*sd**2/stats.chi2.ppf(.025,n-1)),prediction_low=a.mean()-tc*sd*np.sqrt(1+1/n),prediction_high=a.mean()+tc*sd*np.sqrt(1+1/n),tolerance_low=a.mean()-k*sd,tolerance_high=a.mean()+k*sd,tolerance_factor=k))
csv('descriptive_statistics',summary);csv('normal_model_intervals',intervals)
audit={'rows':len(d),'unique_participants':d.pid.nunique(),'missing_cells':int(d.isna().sum().sum()),'rows_removed':0,'data_sha256':hashlib.sha256((P/'data/laptop_urry.csv').read_bytes()).hexdigest()}
(P/'results/data_audit.json').write_text(json.dumps(audit,indent=2))
counts=pd.crosstab(d.talk,d.condition).reindex(columns=G);counts.to_csv(P/'results/lecture_counts.csv')
tests=[]
for outcome in ['overall','factual','conceptual','gap']:
 tests.append(dict(outcome=outcome,**welch(*(d.loc[d.condition==g,outcome] for g in G))))
# Holm family is the three secondary tests, never the primary overall contrast.
ps=np.array([x['p'] for x in tests[1:]]);order=np.argsort(ps);adjusted=np.empty(3);adjusted[order]=np.minimum(1,np.maximum.accumulate(ps[order]*np.arange(3,0,-1)))
for x,p in zip(tests[1:],adjusted):x['holm_p']=p
csv('welch_tests',tests)
primary=tests[0];a,b=(d.loc[d.condition==g,'overall'].to_numpy() for g in G)
sp=np.sqrt(((len(a)-1)*a.var(ddof=1)+(len(b)-1)*b.var(ddof=1))/(len(d)-2));hedges=(1-3/(4*(len(d)-2)-1))*primary['estimate']/sp
rank=stats.mannwhitneyu(a,b,alternative='two-sided',method='asymptotic')
lev=stats.levene(a,b,center='median')
csv('distribution_checks',[dict(method='Mann-Whitney (tie-corrected asymptotic)',statistic=rank.statistic,p=rank.pvalue),dict(method='Brown-Forsythe variance check',statistic=lev.statistic,p=lev.pvalue)]+[dict(method='Shapiro-Wilk '+l,statistic=stats.shapiro(x).statistic,p=stats.shapiro(x).pvalue) for x,l in zip([a,b],L)])
def ols(X,y,names):
 X=np.asarray(X,float);y=np.asarray(y,float);beta=np.linalg.lstsq(X,y,rcond=None)[0];res=y-X@beta;df=len(y)-X.shape[1];sse=res@res;v=np.linalg.inv(X.T@X);se=np.sqrt(np.diag(v)*sse/df);h=np.einsum('ij,jk,ik->i',X,v,X);rob=v@(X.T@np.diag(res**2/(1-h)**2)@X)@v
 out=pd.DataFrame(dict(term=names,estimate=beta,se=se,t=beta/se,p=2*stats.t.sf(abs(beta/se),df),lower=beta-stats.t.ppf(.975,df)*se,upper=beta+stats.t.ppf(.975,df)*se,HC3_se=np.sqrt(np.diag(rob))))
 out['HC3_lower']=beta-stats.norm.ppf(.975)*out.HC3_se
 out['HC3_upper']=beta+stats.norm.ppf(.975)*out.HC3_se
 out['HC3_p_normal']=2*stats.norm.sf(abs(beta/out.HC3_se))
 return dict(X=X,beta=beta,res=res,df=df,sse=sse,h=h,cov=v*sse/df,table=out,r2=1-sse/np.sum((y-y.mean())**2))
y=d.overall.to_numpy();talk=pd.get_dummies(d.talk,drop_first=True,dtype=float);X=np.column_stack([np.ones(len(d)),d.typing,talk]);names=['Intercept','Typing']+list(talk.columns)
m=ols(X,y,names);simple=ols(np.column_stack([np.ones(len(d)),d.typing]),y,['Intercept','Typing'])
interaction=ols(np.column_stack([X,talk.to_numpy()*d.typing.to_numpy()[:,None]]),y,names+['Typing x '+x for x in talk.columns])
m['table'].to_csv(P/'results/lecture_regression.csv',index=False);simple['table'].to_csv(P/'results/simple_regression.csv',index=False)
F=((m['sse']-interaction['sse'])/4)/(interaction['sse']/interaction['df']);interaction_p=stats.f.sf(F,4,interaction['df'])
f_condition=(m['table'].iloc[1].t)**2
csv('model_comparisons',[dict(comparison='Condition adjusted for lecture (partial F)',F=f_condition,df1=1,df2=m['df'],p=stats.f.sf(f_condition,1,m['df'])),dict(comparison='Condition by lecture interaction',F=F,df1=4,df2=interaction['df'],p=interaction_p)])
# Breusch-Pagan auxiliary regression: asymptotic diagnostic, not a gate for choosing Welch.
bp=ols(X,m['res']**2,names);bpstat=len(d)*bp['r2'];bpp=stats.chi2.sf(bpstat,X.shape[1]-1)
rc=m['res']/np.sqrt((m['sse']/m['df'])*(1-m['h']));cook=rc**2*m['h']/(X.shape[1]*(1-m['h']))
pd.DataFrame(dict(pid=d.pid,residual=m['res'],fitted=y-m['res'],leverage=m['h'],studentized_residual=rc,cooks_distance=cook)).to_csv(P/'results/regression_diagnostics.csv',index=False)
cor=[]
for g,l in [('all','All participants'),*zip(G,L)]:
 z=d if g=='all' else d[d.condition==g];r,p=stats.pearsonr(z.factual,z.conceptual);rho,ps=stats.spearmanr(z.factual,z.conceptual);ci=np.tanh(np.arctanh(r)+np.array([-1,1])*stats.norm.ppf(.975)/np.sqrt(len(z)-3))
 cor.append(dict(group=l,n=len(z),pearson_r=r,p=p,lower=ci[0],upper=ci[1],spearman_rho=rho,spearman_p=ps))
csv('correlations',cor)
# Illustrative threshold, not an official pass mark.
tab=np.array([[(x>=70).sum(),(x<70).sum()] for x in [a,b]]);chi,pchi,_,expected=stats.chi2_contingency(tab,correction=False);pooled=tab[:,0].sum()/len(d);se0=np.sqrt(pooled*(1-pooled)*(1/len(a)+1/len(b)));z=(tab[0,0]/len(a)-tab[1,0]/len(b))/se0
props=[]
for x,l in zip([a,b],L):
 n=len(x);s=int((x>=70).sum());p=s/n;zz=stats.norm.ppf(.975);center=(p+zz**2/(2*n))/(1+zz**2/n);half=zz*np.sqrt(p*(1-p)/n+zz**2/(4*n*n))/(1+zz**2/n)
 props.append(dict(group=l,n=n,at_least_70=s,proportion=p,wilson_lower=center-half,wilson_upper=center+half))
csv('illustrative_proportions',props)
csv('categorical_test',[dict(threshold=70,z=z,p=2*stats.norm.sf(abs(z)),chi_square=chi,chi_square_p=pchi,min_expected=expected.min())]);assert np.allclose(z*z,chi)
# Prospective normal planning approximation, assuming common SD estimated here.
def power(delta,n1,n2):
 nc=delta/(sp*np.sqrt(1/n1+1/n2));crit=stats.norm.ppf(.975)
 return stats.norm.sf(crit-nc)+stats.norm.cdf(-crit-nc)
planning=[]
for delta in [3,5,8,10]:
 n=int(np.ceil(2*((stats.norm.ppf(.975)+stats.norm.ppf(.8))*sp/delta)**2))
 planning.append(dict(assumed_difference=delta,assumed_sd=sp,approx_power_current_n=power(delta,len(a),len(b)),approx_n_per_group_80pct=n))
csv('power_planning',planning)
# Visualizations
rng=np.random.default_rng(324)
fig,axs=plt.subplots(1,3,figsize=(13,4),sharey=True)
for ax,out in zip(axs,['overall','factual','conceptual']):
 vals=[d.loc[d.condition==g,out] for g in G]
 ax.boxplot(vals,positions=[0,1],widths=.45,showfliers=False)
 for i,x in enumerate(vals):ax.scatter(i+rng.uniform(-.16,.16,len(x)),x,alpha=.45,s=17,color=C[i]);ax.scatter(i,np.mean(x),marker='D',color='black',s=35,zorder=5)
 ax.set(xticks=[0,1],xticklabels=L,title=out.title(),ylim=(-3,103));ax.grid(axis='y',alpha=.2)
axs[0].set_ylabel('Quiz score (0-100)');save('01_score_distributions','Individual scores overlap substantially','Dots: participants; boxes: middle 50%; line: median; diamond: mean. All observations retained.')
fig,axs=plt.subplots(1,2,figsize=(10,4),sharex=True,sharey=True)
for ax,x,l,c in zip(axs,[a,b],L,C):ax.hist(x,bins=np.arange(0,101,10),color=c,edgecolor='white');ax.set(title=l,xlabel='Overall score',ylabel='Participants')
save('02_histograms','Overall score distributions','Identical bins and axes; the last bin includes 100.')
fig,axs=plt.subplots(1,2,figsize=(10,4))
for ax,x,l in zip(axs,[a,b],L):stats.probplot(x,dist='norm',plot=ax);ax.set(title=l,xlabel='Theoretical normal quantile',ylabel='Observed score')
save('03_normal_probability','Check the normal distribution assumption','Tail departures and bounded scores matter especially for individual prediction, variance and tolerance intervals.')
fig,ax=plt.subplots(figsize=(9,4))
contrasts=[('Overall (primary)',tests[0]),('Factual (secondary)',tests[1]),('Conceptual (secondary)',tests[2]),('Question-type gap',tests[3])]
for i,(label,r) in enumerate(contrasts):ax.errorbar(r['estimate'],i,xerr=[[r['estimate']-r['lower']],[r['upper']-r['estimate']]],fmt='o',capsize=4,color=C[0])
ax.axvline(0,color='gray',ls='--');ax.set(yticks=range(4),yticklabels=[x[0] for x in contrasts],xlabel='Typing minus handwriting (points), marginal 95% CI');ax.invert_yaxis()
save('04_mean_difference_intervals','How large could the mean differences be?','Intervals are individual 95% intervals, not simultaneous family intervals. Secondary p-values are Holm-adjusted separately.')
fig,ax=plt.subplots(figsize=(9,4));xx=np.linspace(-4,4,500);ax.plot(xx,stats.t.pdf(xx,primary['df']),color=C[0]);tail=abs(primary['t']);ax.fill_between(xx,stats.t.pdf(xx,primary['df']),where=abs(xx)>=tail,color=C[1],alpha=.4);ax.axvline(primary['t'],color=C[0],ls='--');ax.set(xlabel='t statistic under equal population means',ylabel='Density')
save('05_hypothesis_test','Main two-sided test: p = %.3f'%primary['p'],'Shading represents both tails at least as far from zero as the observed statistic. The p-value is not the probability that the null is true.')
fig,ax=plt.subplots(figsize=(8,4))
for i,g in enumerate(G):
 z=d[d.condition==g];means=[z.factual.mean(),z.conceptual.mean()];ax.plot([0,1],means,'o-',color=C[i],label=L[i])
ax.set(xticks=[0,1],xticklabels=['Factual','Conceptual'],ylabel='Mean score',ylim=(50,85));ax.legend();save('06_question_type','Does the group difference change with question type?','Lines summarize means, not individual change over time. The formal comparison uses conceptual minus factual within each participant.')
fig,ax=plt.subplots(figsize=(10,4))
for i,g in enumerate(G):
 z=d[d.condition==g].groupby('talk').overall.agg(['mean','count','std']).reindex(counts.index);ax.errorbar(np.arange(5)+(-.1 if i==0 else .1),z['mean'],yerr=stats.t.ppf(.975,z['count']-1)*z['std']/np.sqrt(z['count']),fmt='o',capsize=3,label=L[i],color=C[i])
ax.set(xticks=range(5),xticklabels=counts.index,ylabel='Mean overall score; 95% CI');ax.legend();save('07_lecture_means','Lecture-specific samples differ','Small subgroups have wide intervals. These are descriptive means with marginal t intervals, not five independent confirmatory tests.')
fig,ax=plt.subplots(figsize=(8,3.5))
adj=m['table'].iloc[1]
for i,(name,est,lo,hi) in enumerate([('Unadjusted Welch',primary['estimate'],primary['lower'],primary['upper']),('Adjusted for lecture',adj.estimate,adj.HC3_lower,adj.HC3_upper)]):ax.errorbar(est,i,xerr=[[est-lo],[hi-est]],fmt='o',capsize=5,color=C[i])
ax.set(yticks=[0,1],yticklabels=['Unadjusted Welch','Adjusted for lecture'],xlabel='Typing minus handwriting (points), 95% CI');ax.axvline(0,color='gray',ls='--');save('08_adjusted_comparison','Accounting for lecture leaves the answer uncertain','Adjusted result uses an additive model with lecture indicators and a common typing effect; its approximate 95% interval uses HC3 standard errors and a normal critical value.')
fig,axs=plt.subplots(1,3,figsize=(13,4));axs[0].scatter(y-m['res'],m['res'],alpha=.6);axs[0].axhline(0,color='gray');axs[0].set(xlabel='Fitted overall score',ylabel='Residual');stats.probplot(m['res'],plot=axs[1]);axs[1].set(title='Residual normal probability');axs[2].stem(range(len(d)),cook,markerfmt=' ');axs[2].axhline(4/len(d),ls='--',color=C[1]);axs[2].set(xlabel='Row index',ylabel="Cook's distance")
save('09_regression_diagnostics','Check the lecture-adjusted model','Residual shape, unequal spread and influential observations limit model accuracy. Dashed Cook threshold 4/n is a screening rule, not an exclusion rule.')
fig,ax=plt.subplots(figsize=(8,4))
for g,l,c in zip(G,L,C):
 z=d[d.condition==g];ax.scatter(z.factual,z.conceptual,label=l,color=c,alpha=.65)
ax.set(xlabel='Factual score',ylabel='Conceptual score',xlim=(-2,102),ylim=(-2,102));ax.legend();save('10_factual_conceptual','Are factual and conceptual scores associated?','Each point is one participant. Correlation is exploratory and does not demonstrate causation; overall is not correlated with its own components.')
fig,ax=plt.subplots(figsize=(7,4))
for i,r in enumerate(props):ax.errorbar(i,r['proportion'],yerr=[[r['proportion']-r['wilson_lower']],[r['wilson_upper']-r['proportion']]],fmt='o',capsize=5,color=C[i])
ax.set(xticks=[0,1],xticklabels=L,ylabel='Proportion scoring at least 70',ylim=(0,1));save('11_illustrative_threshold','An illustrative categorical comparison','70 is an exploratory threshold, not an official pass mark. Error bars are Wilson 95% confidence intervals.')
fig,ax=plt.subplots(figsize=(9,4));xx=np.linspace(0,12,150);ax.plot(xx,[power(x,len(a),len(b)) for x in xx]);ax.axhline(.8,ls='--',color='gray');ax.set(xlabel='Assumed true mean difference (points)',ylabel='Approximate power',ylim=(0,1));save('12_power_planning','Small effects need larger future studies','Normal planning approximation at two-sided alpha .05, with common SD estimated from this sample. This is scenario analysis, not evidence for the null.')
fig,ax=plt.subplots(figsize=(10,4))
for i,r in enumerate(intervals):
 for j,(label,lo,hi,c) in enumerate([('Mean CI',r['mean_low'],r['mean_high'],C[0]),('Individual prediction',r['prediction_low'],r['prediction_high'],C[1]),('90% content tolerance',r['tolerance_low'],r['tolerance_high'],'#507c48')]):
  yy=i*4+j;ax.plot([lo,hi],[yy,yy],'-o',color=c,label=label if i==0 else None)
ax.set(yticks=[1,5],yticklabels=L,xlabel='Overall score (normal-model intervals)');ax.axvline(100,color='gray',ls=':');ax.legend(fontsize=9);save('13_interval_purposes','Mean uncertainty differs from individual variation','Mean CIs and prediction intervals are 95%; tolerance intervals have 90% population content and 95% confidence under normality. Values beyond 100 expose the normal model limitation; they are not clipped.')
results=dict(primary=primary,hedges_g=hedges,adjusted=adj.to_dict(),r_squared=m['r2'],interaction_p=interaction_p,bp_statistic=bpstat,bp_p=bpp,rank_p=rank.pvalue,correlations=cor,planning=planning,tests=tests,intervals=intervals,proportions=props,categorical_p=pchi,figures=figures,audit=audit,versions=dict(python=platform.python_version(),numpy=np.__version__,pandas=pd.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__))
(P/'results/analysis.json').write_text(json.dumps(results,indent=2,default=lambda x:x.item()))
print(json.dumps({k:results[k] for k in ['primary','hedges_g','interaction_p','bp_p','rank_p','planning']},indent=2))
