import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from astropy import modeling
import pandas as pd
from scipy.stats import norm
from scipy.stats import poisson
import numpy as np

plt.style.use('classic')
# plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
import matplotlib as mpl
import matplotlib.font_manager as font_manager
mpl.rcParams['font.family']='serif'
cmfont = font_manager.FontProperties(fname=mpl.get_data_path() + '/fonts/ttf/cmr10.ttf')
mpl.rcParams['font.serif']=cmfont.get_name()
mpl.rcParams['mathtext.fontset']='cm'
mpl.rcParams['axes.unicode_minus']=False
colors = ['green', 'orange', 'cyan', 'darkred']
plt.rcParams.update({'font.size': 12})



_affluence_data_fpath = './data/PovertyEstimates.csv'
affluence_data_pd = pd.read_csv(_affluence_data_fpath)
counties = affluence_data_pd['Area_name']
pctpov = affluence_data_pd['PCTPOV017_2018']

affluence_dict = {}
for idx, county in enumerate(counties):
    affluence_dict[county.split(' ')[0].lower()] = pctpov[idx]

plt.hist(pctpov, bins=50, density=True, edgecolor='black', color='blue', alpha=0.5, label='Percentage by county')
mean,std=norm.fit(pctpov)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
y = norm.pdf(x, mean, std)
plt.plot(x, y, c='black', linestyle='-.', linewidth=2, label="Gaussian model fit")
plt.text(27.7, 0.04, f'Model Parameters \n::$\\mu={round(mean, 3)}$, \n::$\\sigma={round(std, 3)}$')
# plt.plot(x, y, c='black', linestyle='-.', linewidth=2, label=f'$\\mu={round(mean, 3)}, \\sigma={round(std, 3)}$')
plt.xlabel("Percentage of children $<$17 under the poverty line")
plt.ylabel("Frequency")
plt.legend(frameon=False)
plt.show()
