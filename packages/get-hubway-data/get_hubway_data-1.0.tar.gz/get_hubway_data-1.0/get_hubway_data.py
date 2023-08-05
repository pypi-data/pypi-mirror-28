import pandas as pd
import os
import matplotlib.pyplot as plt
import json
import sys

# Gets data passed in command line
local_path, output_dir = None, None
for index, word in enumerate(sys.argv):
    if word == "--input":
        local_path = sys.argv[index + 1]
    if word == "--output":
        output_dir = sys.argv[index + 1]

# These have been constant through all of Hubway"s CSVs (their column headers are not)
DURATION_COLUMN = 0
START_DATE_COLUMN = 1
END_DATE_COLUMN = 2


# Some of Hubway"s CSVs durations are in ms
def is_ms(start_date, end_date, duration):
    """
    Checks if the duration given between the two dates corresponds more closely to milliseconds than seconds
    :param start_date: datetime object corresponding to the start date
    :param end_date: datetime object corresponding to the end date
    :param duration: Duration given in the data set between start_date and end_date
    :return: True if time is in milliseconds, False otherwise
    """
    percent_error_for_conversion = .8
    return duration - duration * percent_error_for_conversion < (
        (end_date - start_date).total_seconds()) * 1000 < duration + duration * percent_error_for_conversion


# Get the input file
while True:
    if local_path is None:
        local_path = input("Path of the csv (-1 to exit): ")
        if local_path == "-1": sys.exit()
    if not local_path.endswith(".csv"):
        local_path += ".csv"
    try:
        df = pd.read_csv(local_path, parse_dates=[START_DATE_COLUMN, END_DATE_COLUMN], infer_datetime_format=True)
    except FileNotFoundError:
        print("Couldn't find file : {}".format(local_path))
        local_path = None
        continue
    else:
        break

# Get the output directory
while True:
    if output_dir is None:
        output_dir = input("Output directory (-1 to exit): ")
        if output_dir == "-1": sys.exit()
    if not os.path.isdir(output_dir):
        print("This is not a valid output directory")
        output_dir = None
        continue
    break

# Cleans the data set
df.columns = [x.lower() for x in df.columns]
df = df.dropna(axis=1)

# Finds the columns for relevant data
bike_ID_column, start_station_column, end_station_column = None, None, None
for index, header in enumerate(list(df.columns.values)):
    if "bike" in header:
        bike_ID_column = index
    if "start station name" in header:
        start_station_column = index
    if "end station name" in header:
        end_station_column = index
if (bike_ID_column is None) or (start_station_column is None) or (end_station_column is None):
    print("Could not find relevant columns")
    sys.exit(1)

# Some data sets have duration in milliseconds, it is converted to seconds
if is_ms(df.iloc[0, START_DATE_COLUMN], df.iloc[0, END_DATE_COLUMN], df.iloc[0, DURATION_COLUMN]):
    df.iloc[:, DURATION_COLUMN] = df.iloc[:, DURATION_COLUMN].apply(lambda x: float(x)/1000)
# Some data sets have a letter at the start of the the bike ID, it is deleted
if str(df.iloc[0, bike_ID_column])[0].isalpha():
    df.iloc[:, bike_ID_column] = df.iloc[:, bike_ID_column].apply(lambda x: int(x[1:]) if str(x[1:]).isdigit() else None)
df = df.dropna()

# Extract the relevant data (Note: Duration data heavily right-skewed, might be better to use the median)
data = {"Earliest date": str(df.iloc[:, START_DATE_COLUMN].min()),
        "Latest date": str(df.iloc[:, END_DATE_COLUMN].max()),
        "Station most traveled from": df.iloc[:, start_station_column].value_counts().index[0],
        "Station most traveled to": df.iloc[:, end_station_column].value_counts().index[0],
        "Average duration (sec)": (df.iloc[:, DURATION_COLUMN].mean())}
data["Average duration for the most common trip (sec)"] = \
    (df.where((df.iloc[:, start_station_column] == data["Station most traveled from"]) &
              (df.iloc[:, end_station_column] == data["Station most traveled to"]))).iloc[:, DURATION_COLUMN].mean()

# Creates the histogram for the bike IDs
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.grid(color="gray",
         alpha=.2)
plt.hist(df.iloc[:, bike_ID_column],
         alpha=1,
         color="royalblue",
         bins='auto')
plt.rc('axes', axisbelow=True)
plt.ylabel("Frequency")
plt.xlabel("Bike ID")

# Exports everything to output directory
file_name = local_path.replace(".csv", "") + "_extracted_data.json"  # Creates custom file name based on the CSV
with open(output_dir + "/" + file_name, 'w') as outfile:
    json.dump(data, outfile)
plt.savefig(output_dir + "/" + file_name.replace("extracted_data.json", "bike_ID_histogram.png"), bbox_inches="tight")
