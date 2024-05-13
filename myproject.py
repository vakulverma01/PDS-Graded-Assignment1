# Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read the dataset
fifa_data = pd.read_csv("fifa.csv")

# Check the first few samples
print(fifa_data.head())
# Check the shape of the data
print("Shape of the data:", fifa_data.shape)
# Get information about the data
print(fifa_data.info())
# Drop redundant columns
redundant_columns = ['Photo', 'Flag', 'Club Logo']
fifa_data.drop(columns=redundant_columns, inplace=True)
# Convert "Value", "Wage", "Release Clause" columns to float datatype
def convert_currency(value):
    if 'M' in value:
        return float(value.replace('M', '').replace('€', '')) * 1000000
    elif 'K' in value:
        return float(value.replace('K', '').replace('€', '')) * 1000
    else:
        return float(value.replace('€', ''))

fifa_data['Value'] = fifa_data['Value'].apply(convert_currency)
fifa_data['Wage'] = fifa_data['Wage'].apply(convert_currency)
fifa_data['Release Clause'] = fifa_data['Release Clause'].apply(convert_currency)
# Convert "Joined" column to integer data type with keeping only the year
fifa_data['Joined'] = pd.to_datetime(fifa_data['Joined']).dt.year

# Convert "Contract Valid Until" column to pandas datetime type
fifa_data['Contract Valid Until'] = pd.to_datetime(fifa_data['Contract Valid Until'])

# Convert "Height" column to float with decimal points
fifa_data['Height'] = fifa_data['Height'].apply(lambda x: float(x.replace("'", ".")))

# Convert "Weight" column to float after removing the "lbs" suffix
fifa_data['Weight'] = fifa_data['Weight'].apply(lambda x: float(x.replace("lbs", "")))

# Check for missing values and impute them
missing_percentage = (fifa_data.isnull().sum() / len(fifa_data)) * 100
print("Percentage of missing values:\n", missing_percentage)

# Plot the distribution of Overall rating
plt.hist(fifa_data['Overall'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Overall Rating')
plt.xlabel('Overall Rating')
plt.ylabel('Frequency')
plt.show()

# Retrieve the names of top 20 players based on the Overall rating
top_20_players = fifa_data.nlargest(20, 'Overall')['Name']
print("Top 20 players based on Overall rating:\n", top_20_players)

# Generate a dataframe of top 20 players based on Overall rating
top_20_players_info = fifa_data.nlargest(20, 'Overall')
print("Dataframe of top 20 players based on Overall rating:\n", top_20_players_info)

# Calculate average Age and Wage of top 20 players
average_age = top_20_players_info['Age'].mean()
average_wage = top_20_players_info['Wage'].mean()
print("Average Age of top 20 players:", average_age)
print("Average Wage of top 20 players:", average_wage)

# Player with the highest wage among top 20 players
highest_wage_player = top_20_players_info[top_20_players_info['Wage'] == top_20_players_info['Wage'].max()]
print("Player with the highest wage among top 20 players:\n", highest_wage_player[['Name', 'Wage']])

# Generate a dataframe with Player name, Club Name, Wage, and Overall rating
player_info_df = fifa_data[['Name', 'Club', 'Wage', 'Overall']]
print("Dataframe with Player name, Club Name, Wage, and Overall rating:\n", player_info_df)

# Calculate average Overall rating for each club
average_overall_rating = fifa_data.groupby('Club')['Overall'].mean()

# Display average overall rating of Top 10 Clubs using a plot
top_10_clubs = average_overall_rating.nlargest(10)
plt.bar(top_10_clubs.index, top_10_clubs.values, color='green')
plt.title('Average Overall Rating of Top 10 Clubs')
plt.xlabel('Club')
plt.ylabel('Average Overall Rating')
plt.xticks(rotation=90)
plt.show()

# Visualize the relationship between age and individual potential of the player
plt.scatter(fifa_data['Age'], fifa_data['Potential'], color='orange', alpha=0.5)
plt.title('Age vs Potential')
plt.xlabel('Age')
plt.ylabel('Potential')
plt.show()

# Calculate correlation between features and wages
correlation_matrix = fifa_data[['Wage', 'Potential', 'Overall', 'Value', 'International Reputation', 'Release Clause']].corr()
print("Correlation matrix:\n", correlation_matrix)

# Find position with maximum and minimum number of players
position_counts = fifa_data['Position'].value_counts()
max_position = position_counts.idxmax()
min_position = position_counts.idxmin()
print("Position with maximum number of players:", max_position)
print("Position with minimum number of players:", min_position)

# Players from club 'Juventus' with wage greater than 200K
juventus_players = fifa_data[(fifa_data['Club'] == 'Juventus') & (fifa_data['Wage'] > 200000)]
print("Players from Juventus with wage greater than 200K:\n", juventus_players)

# Generate a dataframe containing top 5