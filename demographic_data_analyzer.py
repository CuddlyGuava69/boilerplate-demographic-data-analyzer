import pandas as pd
import numpy as np

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')

    # How many of each race are represented in this dataset?
    # This should be a Pandas series with race names as the index labels.

    race_count = df.race.value_counts()

    # What is the average age of men?
    average_age_men = np.round(df.loc[df.sex == 'Male', 'age'].mean(), 1)

    # What is the percentage of people who have a Bachelor's degree?
    has_bachelor = len(df.loc[df.education == 'Bachelors'])
    total_people = len(df.education)
    percentage_bachelors = np.round((has_bachelor / total_people) * 100, 1)

    # What percentage of people with advanced education \
    # (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = len(df.loc[df.education.isin([
        'Bachelors', 'Masters', 'Doctorate'])])
    lower_education = len(df.loc[~df.education.isin([
        'Bachelors', 'Masters', 'Doctorate'])])
    lower_education_50k = len(df.loc[(~df.education.isin(['Bachelors', 'Masters', 'Doctorate'])) & \
        (df.salary == '>50K')])

    # percentage with salary >50K
    higher_education_rich = round((len(df.loc[(df.education.isin(['Bachelors', 'Masters', 'Doctorate'])) & (
        df.salary == '>50K')]) / higher_education) * 100, 1)
    lower_education_rich = round((lower_education_50k / lower_education) * 100, 1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = len(df.loc[df['hours-per-week'] == min_work_hours])
    rich_percentage = round((len(df.loc[(df['hours-per-week'] == min_work_hours) & (df.salary == '>50K')]) / num_min_workers) * 100, 1)

    # What country has the highest percentage of people that earn >50K?
    highest_earning_country = df.groupby(['native-country', 'salary'])['age'].count().reset_index()
    highest_earning_country = highest_earning_country.loc[highest_earning_country.salary == '>50K'].reset_index()
    highest_earning_country = highest_earning_country.rename(columns={'age':'num_of_peeps'})

    # The total variable measures the total amout of people surveyed in each country
    total = df.groupby('native-country')['age'].count().reset_index()
    total = total.rename(columns = {'age':'total'})

    # The two datasets are merged left towards highest_earning_country to place the total\
    # survees of each country in the correct row and create a new total column in highest_earning_county
    highest_earning_country = pd.merge(highest_earning_country, total, how='left')

    highest_earning_country['percentage'] = round(highest_earning_country.num_of_peeps / highest_earning_country.total * 100, 1)
    highest_earning_country_end = highest_earning_country.sort_values(by = 'percentage', ascending = False).reset_index()
    highest_earning_country = highest_earning_country_end['native-country'][0]
    
    highest_earning_country_percentage = highest_earning_country_end.percentage[0]

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df.loc[(df.salary == '>50K') & (df['native-country'] == 'India')]
    top_IN_occupation = top_IN_occupation.groupby('occupation')['age'].count().reset_index()
    top_IN_occupation.rename(columns = {'age': 'number_of_people'}, inplace = True)
    top_IN_occupation = top_IN_occupation.sort_values(by = 'number_of_people', ascending = False).reset_index()
    top_IN_occupation = top_IN_occupation.occupation[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count)
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(
            f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(
            f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(
            f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(
            f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
