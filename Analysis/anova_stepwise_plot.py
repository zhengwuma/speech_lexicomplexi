!pip install stepwise-regression --quiet
!pip install plotnine --quiet

import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
import scipy.stats as stats
from stepwise_regression import step_reg
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *
from plotnine import ggplot, aes, geom_point, geom_errorbarh, scale_x_continuous, labs, scale_color_manual, theme_classic
import subprocess

repository_url = 'https://github.com/zhengwuma/speech_lexicomplexi.git'
subprocess.run(['git', 'clone', repository_url])

DIR = '/content/LexicalComplexity_RatedQuality/Analysis'
os.chdir(DIR)

df_measure = pd.read_csv(f'LC_measure.csv')
df_measure

"""# One-way ANOVA by Python"""

# One-way ANOVA between scale & index by Python
df_measure1 = df_measure

df_measure1 = df_measure1.drop('HS', axis=1)
df_measure1 = df_measure1.drop('Filename', axis=1)

group1 = df_measure1.loc[df_measure['Scale'] == 1].iloc[:, 1:].values
group2 = df_measure1.loc[df_measure['Scale'] == 2].iloc[:, 1:].values
group3 = df_measure1.loc[df_measure['Scale'] == 3].iloc[:, 1:].values

results = []
for i, col in enumerate(df_measure1.columns[1:]):
    fvalue, pvalue = stats.f_oneway(group1[:, i], group2[:, i], group3[:, i])
    if pvalue <= 0.05:
        results.append({'index': col, 'P-value': pvalue})

results_df = pd.DataFrame(results)
print(results_df)

# One-way ANOVA between comprehensibility & index by Python
df_measure2 = df_measure
col_hs = df_measure2['HS']
df_measure2 = df_measure2.drop('HS', axis=1)

group1 = df_measure2.loc[df_measure2['C'] == 4].iloc[:, 1:].values
group2 = df_measure2.loc[df_measure2['C'] == 5].iloc[:, 1:].values
group3 = df_measure2.loc[df_measure2['C'] == 6].iloc[:, 1:].values
group4 = df_measure2.loc[df_measure2['C'] == 7].iloc[:, 1:].values

results_c = []
for i, col in enumerate(df_measure2.columns[1:]):
    fvalue, pvalue = stats.f_oneway(group1[:, i], group2[:, i], group3[:, i], group4[:, i])
    if pvalue <= 0.05:
        results_c.append({'index': col, 'P-value': pvalue})

df_measure2['HS'] = col_hs
results_c = pd.DataFrame(results_c)
print(results_c)

# One-way ANOVA between lexical appropriateness & index
df_measure3 = df_measure

col_hs = df_measure3['HS']
df_measure3 = df_measure3.drop('HS', axis=1)

group1 = df_measure3.loc[df_measure3['LA'] == 4].iloc[:, 1:].values
group2 = df_measure3.loc[df_measure3['LA'] == 5].iloc[:, 1:].values
group3 = df_measure3.loc[df_measure3['LA'] == 6].iloc[:, 1:].values
group4 = df_measure3.loc[df_measure3['LA'] == 7].iloc[:, 1:].values

results_la = []
for i, col in enumerate(df_measure3.columns[1:]):
    fvalue, pvalue = stats.f_oneway(group1[:, i], group2[:, i], group3[:, i], group4[:, i])
    if pvalue <= 0.05:
        results_la.append({'index': col, 'P-value': pvalue})

df_measure3['HS'] = col_hs
results_la = pd.DataFrame(results_la)
print(results_la)

"""# One-way ANOVA results plots (data loaded from SPSS)"""

# One-way ANOVA plot: scale & index (data load from spss)
data_scale = np.load('data_scale.npy')
measure, group1, group2, group3, sig = data_scale
df_scale = pd.DataFrame({'Measure': measure, 'group 1': group1, 'group 2': group2, 'group 3': group3, 'Sig.': sig})

fig, ax = plt.subplots(figsize=(5,5))
color_vec = ['#ff8357','#ff9f97','#fac172','#98b6ec',
             '#89d5c9','#adc865','#ffacbb','#fed7dd',
             '#f6d7c3','#cdd885','#acbfea','#c5d6ac',
             '#ad7b9d','#fdc441','#ef852f', '#823d32', '#e3cfb4']

for i in range(1, 4):
    mean_col = f"group {i}"
    sd_col = f"group {i}"
    df_scale['Mean'] = df_scale[mean_col].apply(lambda x:float(x.split()[0]))
    df_scale['SD'] = df_scale[sd_col].apply(lambda x: float(x.split()[1][1:-1]))
    for j, measure in enumerate(df_scale['Measure']):
        sig_level = df_scale.loc[j, 'Sig.']
        if float(sig_level) <= 0:
            marker = 'd'
        elif 0 < float(sig_level) <= 0.001:
            marker = '^'
        else:
            marker = 'o'
        ax.errorbar(measure,
                    df_scale['Mean'][j],
                    yerr=df_scale['SD'][j],
                    fmt=marker,
                    color=color_vec[j],
                    markersize=15,
                    markeredgecolor='gray',
                    markeredgewidth=0.1,
                    elinewidth=0.8)

ax.set_xticklabels(df_scale['Measure'], rotation=90)
ax.set_yticks([0, 20, 40])
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)

plt.subplots_adjust(left=0.1, bottom=0.26, right=0.97, top=0.99)
plt.show()
plt.savefig('sig_scale.png', dpi=300)

# One-way ANOVA plot: comprehensibility & index (data load from spss)
data_c = np.load('data_c.npy')
measure, group1, group2, group3, group4, sig = data_c
df_c = pd.DataFrame({'Measure': measure, 'group 1': group1, 'group 2': group2, 'group 3': group3, 'group 4': group4, 'Sig.': sig})

fig, ax = plt.subplots(figsize=(4,4))
color_vec = ['#ff9f97', '#e25b45', '#fac172', '#98b6ec',
             '#89d5c9', '#adc865', '#ffacbb','#fed7dd',
             '#f6d7c3','#acbfea', '#ad7b9d']

for i in range(1, 5):
    mean_col = f"group {i}"
    sd_col = f"group {i}"
    df_c['Mean'] = df_c[mean_col].apply(lambda x:float(x.split()[0]))
    df_c['SD'] = df_c[sd_col].apply(lambda x: float(x.split()[1][1:-1]))
    for j, measure in enumerate(df_c['Measure']):
        sig_level = df_c.loc[j, 'Sig.']
        if float(sig_level) <= 0:
            marker = 'd'
        elif 0 < float(sig_level) <= 0.001:
            marker = '^'
        else:
            marker = 'o'
        ax.errorbar(measure,
                    df_c['Mean'][j],
                    yerr=df_c['SD'][j],
                    fmt=marker,
                    color=color_vec[j],
                    markersize=15,
                    markeredgecolor='gray',
                    markeredgewidth=0.1,
                    elinewidth=0.8)

ax.set_xticklabels(df_c['Measure'], rotation=90)
ax.set_ylim(-5,50)
ax.set_yticks([0, 20, 40])
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)

plt.subplots_adjust(left=0.1, bottom=0.25, right=0.97, top=0.99)
plt.savefig('sig_c.png', dpi=300)

### plot the spss results
data_la = np.load('data_la.npy')
measure, group1, group2, group3, group4, sig = data_la
df_la = pd.DataFrame({'Measure': measure, 'group 1': group1, 'group 2': group2, 'group 3': group3, 'group 4': group4, 'Sig.': sig})

fig, ax = plt.subplots(figsize=(4,4))
color_vec = ['#e25b45', '#ff8357', '#fac172', '#89d5c9', '#adc865', '#ffacbb', '#fed7dd', '#f6d7c3', '#acbfea', '#a1dcd8', '#c5d6ac', '#ad7b9d', '#e2d0dc']

for i in range(1, 5):
    mean_col = f"group {i}"
    sd_col = f"group {i}"
    df_la['Mean'] = df_la[mean_col].apply(lambda x:float(x.split()[0]))
    df_la['SD'] = df_la[sd_col].apply(lambda x: float(x.split()[1][1:-1]))
    for j, measure in enumerate(df_la['Measure']):
        sig_level = df_la.loc[j, 'Sig.']
        if float(sig_level) <= 0:
            marker = 'd'
        elif 0 < float(sig_level) <= 0.001:
            marker = '^'
        else:
            marker = 'o'
        ax.errorbar(measure,
                    df_la['Mean'][j],
                    yerr=df_la['SD'][j],
                    fmt=marker,
                    color=color_vec[j],
                    markersize=15,
                    markeredgecolor='gray',
                    markeredgewidth=0.1,
                    elinewidth=0.8)

ax.set_xticklabels(df_la['Measure'], rotation=90)
ax.set_ylim(-10,135)
ax.set_yticks([0, 40, 80, 120])
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(True)
ax.spines['bottom'].set_visible(True)
plt.subplots_adjust(left=0.1, bottom=0.25, right=0.97, top=0.99)
plt.savefig('sig_la.png', dpi=300)

"""# Model Check"""

### Whole model with all predictors
y = df_measure['HS']
X = df_measure.drop(columns=['Filename', 'Scale', 'HS']) #include comprehensibility and lexical appropriateness
X = sm.add_constant(X)
model = sm.OLS(y, X)
results = model.fit()

results.summary()

"""# Stepwise regression, forward"""

### Stepwise regression modeling, HS_index
# forwward_regression
y = df_measure['HS']
X1 = df_measure.drop(columns=['Filename', 'Scale', 'HS', 'LD']) # C, LA included
X2 = df_measure.drop(columns=['Filename', 'Scale', 'HS', 'LD', 'C', 'LA'])  # C, LA excluded
model_in = step_reg.forward_regression(X1, y, 0.05,verbose=False)
model_ex = step_reg.forward_regression(X2, y, 0.05,verbose=False)

model_in

model_ex

# HS_index model check
X_model_in = df_measure[model_in]
X_model_in_check = sm.add_constant(X_model_in)
model_in_check = sm.OLS(y, X_model_in_check)
model_in_results = model_in_check.fit()

model_in_results.summary()

X_model_ex = df_measure[model_ex]
X_model_ex_check = sm.add_constant(X_model_ex)
model_ex_check = sm.OLS(y, X_model_ex_check)
model_ex_results = model_ex_check.fit()

model_ex_results.summary()

# C_indesx regression

y_c = df_measure['C']
X_c = df_measure.drop(columns=['Filename', 'Scale', 'HS', 'LD', 'C','LA'])
model_c = step_reg.forward_regression(X_c, y_c, 0.05,verbose=False)

model_c

X_model_c = df_measure[model_c]
X_model_c_check = sm.add_constant(X_model_c)
model_c_check = sm.OLS(y, X_model_c_check)
model_c_results = model_c_check.fit()

model_c_results.summary()

# LA_index regression

y_la = df_measure['LA']
X_la = df_measure.drop(columns=['Filename', 'Scale', 'HS', 'LD', 'C','LA'])
model_la = step_reg.forward_regression(X_la, y_la, 0.05,verbose=False)

X_model_la = df_measure[model_la]
X_model_la_check = sm.add_constant(X_model_la)
model_la_check = sm.OLS(y, X_model_la_check)
model_la_results = model_la_check.fit()

model_la_results.summary()

"""# Plot the model coefficient"""

model_name = ['model_in', 'model_ex', 'model_c', 'model_la']

for name in model_name:
  # Standardized Regression Coefficients
  results = globals()[name + '_results']
  beta_std = results.params / results.params.std()
  coef_df = pd.DataFrame({'beta': beta_std, 'se': results.bse / results.params.std()}).reset_index()
  coef_df.columns = ['variable', 'beta', 'se']
  coef_df = coef_df[coef_df['variable'] != 'const']
  coef_df['color'] = coef_df['beta'].apply(lambda x: 'blue' if x < 0 else 'red')

  plt = (ggplot(coef_df, aes(x='beta', y='variable', color='color')) +
      geom_point(size=3) +
      geom_errorbarh(aes(xmin='beta - 1.96 * se', xmax='beta + 1.96 * se'), height=0.1, size=0.5) +
      geom_vline(xintercept=0, linetype='dashed', color='gray', size=0.25) +
      scale_x_continuous(expand=(0, 0), limits=(-5, 1)) +  ### !!! change according to β !!!
      labs(x='β Coefficient', y=None) +
      scale_color_manual(values={'blue': '#98b6ec', 'red': '#ff9f97'}) +
      theme_classic())

  filename = name + "_coef_plot.png"
  print(name + ":\n", beta_std)
  plt.save(filename, dpi=300, width=6, height=4, units='in')

"""# Plot model regressors' correlation"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

model_name = ['model_in', 'model_ex', 'model_c', 'model_la']

for name in model_name:
    predictors_variable_name = f'X_{name}'
    predictors = globals()[predictors_variable_name]
    correlation_matrix = predictors.corr()
    font = 'DejaVu Sans'
    plt.rcParams['font.family'] = font

    num_indices = len(correlation_matrix.columns)
    fig_size = (min(max(num_indices * 0.5, 8), 12), min(max(num_indices * 0.5, 6), 10))

    font_scale = 1.2
    if name == 'model_la':
        font_scale = 0.8
    sns.set(font_scale=font_scale)
    plt.figure(figsize=fig_size)

    ax = plt.gca()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", alpha=0.9, ax=ax)

    filename = name + "_reg_corr.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.show()
