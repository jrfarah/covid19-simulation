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


###### LOAD IN AFFLUENCE DATA ######
_affluence_data_fpath = './data/PovertyEstimates.csv'
affluence_data_pd = pd.read_csv(_affluence_data_fpath)
counties = affluence_data_pd['Area_name']
pctpov = affluence_data_pd['PCTPOV017_2018']

affluence_dict = {}
for idx, county in enumerate(counties):
    affluence_dict[county.split(' ')[0].lower()] = pctpov[idx]



##### LOAD IN COVID DATA ######
## load in csv ##
with open("data/us-counties_covid_data.csv", "r") as covid:
    lines = covid.readlines()

## create dictionary ##
## key = ID, entry = {'name':, 'state': 'dates':[], 'cases':[], 'deaths':}
t0 = time.time()
covid_time_series = {}
for line in lines[1:]:
    splitline = line.split(',')
    date     = splitline[0]
    county   = splitline[1]
    state    = splitline[2]
    fips     = splitline[3]
    cases    = float(splitline[4])
    deaths   = splitline[5]
    try:
        deaths = float(deaths)
    except ValueError:
        deaths = 0


    ## check if id already exists ##
    if fips in covid_time_series:
        covid_time_series[fips]['dates'].append(date)
        covid_time_series[fips]['cases'].append(cases)
        covid_time_series[fips]['deaths'].append(deaths)
    else:
        print(f"Adding county {county} with ID {fips} in state {state}.")
        covid_time_series[fips] = {}
        covid_time_series[fips]['name'] = county
        covid_time_series[fips]['state'] = state
        covid_time_series[fips]['dates'] = []
        covid_time_series[fips]['cases'] = []
        covid_time_series[fips]['deaths'] = []

print(f"Read in data in {time.time()-t0} seconds.")
print(f"Total: {len(covid_time_series)} counties with around {len(covid_time_series['06037']['dates'])} data points.")



##### PRODUCE SCATTER DATASET #####
t0 = time.time()
points_mu = []
points_sigma = []
for fips in list(covid_time_series.keys()):

    ## grab covid info ##
    cases = covid_time_series[str(fips)]['cases']
    dates = covid_time_series[str(fips)]['dates']
    county = covid_time_series[str(fips)]['name']

    ## convert county name ##
    county = county.lower()

    ## grab county affluence ##
    try:
        affluence = affluence_dict[county]
    except KeyError:
        print ("[{0}][county: {1}]".format(datetime.datetime.utcnow().strftime("%H:%M:%S"), county))


    ## get gaussian ##
    day_of_year = [float(datetime.datetime.strptime(date.replace('-0', '-'),"%Y-%m-%d").date().strftime('%j')) for date in dates]
    fitter = modeling.fitting.LevMarLSQFitter()
    model = modeling.models.Gaussian1D(max(cases), 100, 50)   # depending on the data you need to give some initial values
    fitted_model = fitter(model, day_of_year, cases)

    mu, sigma = fitted_model.parameters[1], fitted_model.parameters[2]



    ## make points ##
    point_mu = [affluence, mu]
    point_sigma = [affluence, sigma]

    ## add points ##
    points_mu.append(point_mu)
    points_sigma.append(point_sigma)

print(f"Time to collate data: {time.time()-t0} seconds.")




## produce scatter plot ##

# fitx = np.linspace(-10, 70)
fitx = np.linspace(-10, 70)
# fity = -24.166666666666668*fitx + 1500
fity = -1.666667*fitx+250
plt.plot(fitx, fity, c='red', linestyle='--', lw=2, label='Linear regression')
plt.fill_between(fitx, fity+150, fity-150, alpha=0.1, color='red', label='90$\%$ confidence')
plt.scatter(*np.transpose(points_sigma), label='County measure')
plt.xlabel("Affluence metric")
plt.ylabel("Estimated spread $\\sigma$")
plt.xlim(0, 60)
plt.ylim(5, 750)
plt.legend(frameon=False)
plt.show()