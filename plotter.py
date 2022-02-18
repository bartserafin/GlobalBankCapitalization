import matplotlib.pyplot as plt
import pandas as pd


def format_data(file):
    df = pd.read_csv(file)
    sorted_df = df.sort_values(by=['Market Cap (EUR€ Billion)'], ascending=True)
    sorted_df = sorted_df.drop('Unnamed: 0', axis=1)
    # print(sorted_df)
    plot_banks_capitalization(sorted_df)
    plot_pie_chart(sorted_df)


# plot all banks capitalization in EUR
def plot_banks_capitalization(sorted_data):
    fig1, ax1 = plt.subplots()
    y_axis = sorted_data['Market Cap (EUR€ Billion)']
    plt.ylabel('Bank Name')

    x_axis = sorted_data['Name']
    plt.xlabel('Capitalization in EUR€ Billion')
    plt.title('Top 15 World Banks Capitalization')
    plt.barh(x_axis, y_axis)
    plt.subplots_adjust(left=0.208)
    plt.show()


# plot global capitalization per country in %
def plot_pie_chart(data):
    country_capitalization = {}
    # Create a dict Country: Market Cap
    for index, row in data.iterrows():
        if row['Country'] not in country_capitalization:
            country_capitalization[row['Country']] = row['Market Cap (EUR€ Billion)']
        else:
            country_capitalization[row['Country']] += row['Market Cap (EUR€ Billion)']

    # Sum all capitals = 100%
    sum_capitals = 0
    for key in country_capitalization.keys():
        sum_capitals += country_capitalization[key]

    sum_capitals = round(sum_capitals, 2)

    # Find % for each country
    for key in country_capitalization.keys():
        country_capitalization[key] = round((country_capitalization[key] / sum_capitals) * 100, 2)

    # Prepare data for pie chart
    labels = [key for key in country_capitalization.keys()]
    sizes = [value for value in country_capitalization.values()]
    explode = tuple([0.05 for _ in range(len(sizes))])

    # plot pie chart
    fig1, ax1 = plt.subplots()
    ax1.set_title('Country % Global Market Capitalization')
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=30)
    ax1.axis('equal')
    plt.show()


def plot_graphs(file):
    format_data(file)




