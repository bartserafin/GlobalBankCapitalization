import pandas as pd
from datetime import datetime
import glob
import csv
from scrapper import scrap_data
from plotter import plot_graphs

original_file = "original_data.csv"  # file used to store all extracted data
log_file = "logfile.txt"  # all event logs will be stored in this file
target_file = "transformed_data.csv"  # file where transformed data is stored


# ----- EXTRACT DATA ----- #
def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process, lines=False)
    return dataframe


def extract():
    extracted_data = pd.DataFrame(
        {
            'Name': [],
            'Country': [],
            "Market Cap (US$ Billion)": [],
        }
    )

    # process json file
    for jsonfile in glob.glob("*.json"):
        extracted_data = extract_from_json(jsonfile)

    extracted_data.to_csv(original_file)

    return extracted_data


# ----- TRANSFORM DATA ----- #
def transform(data):
    # Convert currency using exchange_rate.csv
    # Access USD to EUR exchange rate
    with open('GlobalBankCapitalization\exchange_rates.csv', 'r') as file:
        content = csv.reader(file)
        for row in content:
            if row[0] == 'EUR':
                exchange_rate = float(row[1])
                print(exchange_rate)
                break

        # Convert currency from USD to EUR for all banks in Data
        market_cap_euro_lst = []
        for row in data['Market Cap (US$ Billion)']:
            row = float(row.replace(',',''))
            market_cap_euro = round(row * exchange_rate, 2)
            market_cap_euro_lst.append(market_cap_euro)

    # Append Data
    data = data.rename(columns={'Market Cap (US$ Billion)': "Market Cap (EUR€ Billion)"})
    data["Market Cap (EUR€ Billion)"] = market_cap_euro_lst

    return data


# ----- LOAD DATA ----- #
def load(target_file, data_to_load):
    data_to_load.to_csv(target_file)


# ----- LOGGING DATA ----- #
def log(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'  # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now()  # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("log_file.txt", "a") as f:
        f.write(timestamp + ',' + message + '\n')


# ----- ETL PROCESS ----- #
log("ETL Job Started")

log("Extract phase Started")
data = scrap_data()
extracted_data = extract()
log("Extract phase Ended")

log("Transform phase Started")
transformed_data = transform(extracted_data)
log("Transform phase Ended")

log("Load phase Started")
load(target_file, transformed_data)
log("Load phase Ended")

log("ETL Job Ended")

# ----- PLOTTER ----- #
plot_graphs(target_file)
