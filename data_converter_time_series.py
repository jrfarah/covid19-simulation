import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from astropy import modeling


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


def plots(fips, fips2=None, fit_fips=False, plot_deaths=True):
    ## plot first data ##
    colors = ['blue', 'green', 'red', 'orange']
    cases = covid_time_series[str(fips)]['cases']
    deaths = covid_time_series[str(fips)]['deaths']
    dates = covid_time_series[str(fips)]['dates']
    county = covid_time_series[str(fips)]['name']

    plt.plot(dates, cases, label=f'cases, {county}', c=colors[0])
    if plot_deaths: plt.plot(dates, deaths, label=f'deaths, {county}', c=colors[0], linestyle='--', alpha=0.5)


    if fit_fips is True:
        fips2 = None
        day_of_year = [float(datetime.datetime.strptime(date.replace('-0', '-'),"%Y-%m-%d").date().strftime('%j')) for date in dates]
        fitter = modeling.fitting.LevMarLSQFitter()
        model = modeling.models.Gaussian1D(max(cases), 160, 50)   # depending on the data you need to give some initial values
        fitted_model = fitter(model, day_of_year, cases)

        plt.plot(day_of_year, fitted_model(day_of_year), c='black', linestyle='-.', label=f'Gaussian fit, {county}')

        plt.text(185, 0.65*10**2, 'Model parameters', fontweight='heavy', size=16)
        plt.text(185, 0.35*10**2, f':::A$\\to$ {round(fitted_model.parameters[0], 3)}')
        plt.text(185, 0.2*10**2, f':::$\\mu\\to$ {round(fitted_model.parameters[1], 3)}')
        plt.text(185, 0.1*10**2, f':::$\\sigma\\to$ {round(fitted_model.parameters[2], 3)}')


    ## plot second data ##
    if fips2 is not None:
        colors = ['blue', 'green', 'red', 'orange']
        cases = covid_time_series[str(fips2)]['cases']
        deaths = covid_time_series[str(fips2)]['deaths']
        dates = covid_time_series[str(fips2)]['dates']
        county = covid_time_series[str(fips2)]['name']

        plt.plot(dates, cases, label=f'cases, {county}', c=colors[2])
        if plot_deaths: plt.plot(dates, deaths, label=f'deaths, {county}', c=colors[2], linestyle='--', alpha=0.5)



    ## plot dates properly ##
    dates = [datetime.datetime.strptime(d.replace('-0', '-'),"%Y-%m-%d").date() for d in dates]
    ax = plt.gca()
    formatter = mdates.DateFormatter("%b")
    ax.xaxis.set_major_formatter(formatter)
    locator = mdates.MonthLocator()
    ax.xaxis.set_major_locator(locator)

    plt.yscale('log')
    plt.xlabel("Date")
    plt.ylabel("Impact")
    plt.legend(loc='lower right', frameon=False)

    plt.show()

plots(fips = '06037', fit_fips=False, plot_deaths=False)
plots(fips = '06037', fit_fips=False, plot_deaths=True)
plots(fips = '06037', fit_fips=True, plot_deaths=False)
plots(fips = '06037', fips2='25017', fit_fips=False, plot_deaths=False)