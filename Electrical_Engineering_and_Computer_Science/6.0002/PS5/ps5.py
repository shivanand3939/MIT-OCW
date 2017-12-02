# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy as np
# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    # TODO
    res = []
    for deg in degs:
        p = pylab.polyfit(x, y, deg)
        res.append(p)
    return res


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    # TODO
    mean_y_actual = sum(y)/float(len(y))
    import numpy as np 
    y_yest = np.array(y) - np.array(estimated)
    y_y_mean = np.array(y)-mean_y_actual
    sum_square_error = sum(y_yest*y_yest)
    sum_square_y_minus_mean = sum(y_y_mean*y_y_mean)
    return 1 - float(sum_square_error)/sum_square_y_minus_mean


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """ 
    for model in models:
        pylab.figure()
        pylab.scatter(x,y,color='blue')
        i = len(model.tolist())
        import numpy as np
        y_est = np.array([0.]*len(x))
        for c in model:
            y_est += np.array([ c*each**(i-1) for each in x])
            i-=1
        r_2 = r_squared(y, y_est)
        pylab.plot(x,y_est,color='red',)
        pylab.legend()
        pylab.xlabel('years')
        pylab.ylabel('temperature')
        deg = len(model.tolist())-1
        if deg == 1:
            se_over_sl = se_over_slope(np.array(x), np.array(y), y_est, model)
            title = 'degree: {} \n R-square: {} \n se_over_slope: {}'.format(deg,  r_2, se_over_sl)
        else:
            title = 'degree: {} \n R-square: {}'.format(deg,  r_2)
        pylab.title(title)
        pylab.show()
        

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """  
    y_avg_yr=[] 
    for each in years: 
        avg_temp = 0
        for city in multi_cities:
            yr_temp = climate.get_yearly_temp(city, each)
            avg_temp += sum(yr_temp)/float(len(yr_temp)) 
        y_avg_temp = float(avg_temp)/len(multi_cities)
        y_avg_yr.append(y_avg_temp)
    return y_avg_yr

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    # TODO
    y_res = []
    for k in range(len(y)):
        valid_elements = 0
        sum_window_elements = 0
        for i in range(window_length):
            if k-i >= 0:
                valid_elements += 1
                sum_window_elements += y[k-i]
        y_res.append(float(sum_window_elements)/valid_elements)
    return y_res


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """ 
    return np.sqrt(sum((y - estimated)**2)/float(len(y)))


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    # TODO
    y_avg_yr=[] 
    for each in years: 
        yr_temp = 0
        for city in multi_cities:
            yr_temp += climate.get_yearly_temp(city, each) 
        y_avg_temp = yr_temp/float(len(multi_cities))
        mean = sum(y_avg_temp)/float(len(y_avg_temp))
        sum_squares = 0
        for sample in y_avg_temp:
            sum_squares += (sample - mean)**2 
        y_avg_yr.append(np.sqrt(float(sum_squares)/len(y_avg_temp)))
    return y_avg_yr

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates ofd
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        pylab.figure()
        pylab.scatter(x,y,color='blue')
        i = len(model.tolist())
        import numpy as np
        y_est = np.array([0.]*len(x))
        for c in model:
            y_est += np.array([ c*each**(i-1) for each in x])
            i-=1
        rmse_ = rmse(y, y_est)
        pylab.plot(x,y_est,color='red',)
        pylab.legend()
        pylab.xlabel('years')
        pylab.ylabel('temperature')
        deg = len(model.tolist())-1
        title = 'degree: {} \n RMSE: {}'.format(deg,  rmse_)
        pylab.title(title)
    pylab.show()

if __name__ == '__main__':
    pass
    #print generate_models(pylab.array([1961, 1962, 1963]), pylab.array([-4.4, -5.5, -6.6]), [1, 2])  

    # Part A.4
    # TODO: replace this line with your code
    cli = Climate('data.csv')
    x=TRAINING_INTERVAL
    # y_jan_10=[] 
    # for each in x: 
    #     y_jan_10.append(cli.get_daily_temp('NEW YORK', 1, 10, each))
    # model = generate_models(x, y_jan_10, [1]) 
    # evaluate_models_on_training(x, y_jan_10, model)
    
    # #A.4.II
    # y_avg_yr=[] 
    # for each in x: 
    #     yr_temp = cli.get_yearly_temp('NEW YORK', each)
    #     avg_temp = sum(yr_temp)/float(len(yr_temp)) 
    #     y_avg_yr.append(round(avg_temp,2))
    # model = generate_models(x, y_avg_yr, [1]) 
    # evaluate_models_on_training(x, y_avg_yr, model)


    # Part B
    # TODO: replace this line with your code
    #y_avg_yr_all_cities = gen_cities_avg(cli, CITIES, x)
    #model = generate_models(x, y_avg_yr_all_cities, [1]) 
    #evaluate_models_on_training(x, y_avg_yr_all_cities, model)

    # Part C
    # TODO: replace this line with your code
    # window_length = 5
    # y_avg_yr_all_cities = gen_cities_avg(cli, CITIES, x)
    # y_moving_avg_yr_all_cities = moving_average(y_avg_yr_all_cities, window_length)
    # model = generate_models(x, y_moving_avg_yr_all_cities, [1]) 
    # evaluate_models_on_training(x, y_moving_avg_yr_all_cities, model)

    # Part D.2
    # TODO: replace this line with your code
    # window_length = 5
    # y_avg_yr_all_cities = gen_cities_avg(cli, CITIES, x)
    # y_moving_avg_yr_all_cities = moving_average(y_avg_yr_all_cities, window_length)
    # models = generate_models(x, y_moving_avg_yr_all_cities, [1, 2, 20]) 
    # #evaluate_models_on_training(x, y_moving_avg_yr_all_cities, models)
    # #Testing
    # y_avg_yr_all_cities_test_real = gen_cities_avg(cli, CITIES, TESTING_INTERVAL)
    # y_moving_avg_yr_all_cities_test_real = moving_average(y_avg_yr_all_cities_test_real, window_length)
    # evaluate_models_on_testing(TESTING_INTERVAL, y_moving_avg_yr_all_cities_test_real, models)
    
    # Part E
    # TODO: replace this line with your code
    #window_length = 5
    #y_avg_yr_all_cities = gen_std_devs(cli, CITIES, x)
    #y_moving_avg_yr_all_cities = moving_average(y_avg_yr_all_cities, window_length)
    # models = generate_models(x, y_moving_avg_yr_all_cities, [1]) 
    # evaluate_models_on_training(x, y_moving_avg_yr_all_cities, models)
    
