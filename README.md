# sqlalchemy challenge #

## instructions ##
* Part 1: Analyze and Explore the Climate Data
    * In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib.
        * Precipitation Analysis
        * Station Analysis
* Part 2: Design Your Climate App
    * Now that you’ve completed your initial analysis, you’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes


## sources ##
* 01: dow_dates.ipynb
    * __use dt to find certain dates__
        * last_year = dt.date(2017, 8, 23) + dt.timedelta(days=365)

* 02: https://stackoverflow.com/questions/38376938/sort-a-pandas-dataframe-based-on-datetime-field
    * __sort dataframe using datetime__
        * data_df.set_index(data_df['date'], inplace=True)

* 03: https://pandas.pydata.org/docs/getting_started/intro_tutorials/06_calculate_statistics.html
    * __to calculate summary statistics__
        * clean_df.describe()
    
* 04: https://stackoverflow.com/questions/18648626/for-loop-with-two-variables
    * __use for loop with two variables__
        * for d,t in result_temp:
