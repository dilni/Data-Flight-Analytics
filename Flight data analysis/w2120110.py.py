"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: w2120110-(UOW)  20240771-(IIT) 
 4. Date:
     Start- 5th July 2025
     End - 7th July 2025
****************************************************************************

"""
#import os
import csv
from graphics import *
from collections import defaultdict

# Get the directory of this script
#script_dir = os.path.dirname(os.path.abspath(__file__))

# Define results paths
#data_path = os.path.join(script_dir, "data") #this line is commented out so that CSV files are loaded from the same directory as the Python file.
#results_path = os.path.join(script_dir, "results")

# Ensure folders exist
#os.makedirs(data_path, exist_ok=True) #this line is commented out so that CSV files are loaded from the same directory as the Python file.
#os.makedirs(results_path, exist_ok=True)

# Airport and Airline mappings
airport_codes = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

airline_codes = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}
#------------------------------------------------------------------------------------------------------------------------------------------
#Task A - Input validations

def validate_city_code():
    while True:
        code = input("Please enter the three-letter code for the departure city required: ").strip().upper()
        if len(code) != 3:
            print("Wrong code length - please enter a three-letter city code.")
        elif code not in airport_codes:
            print("Unavailable city code - please enter a valid city code.")
        else:
            return code

def validate_year():
    while True:
        year_input = input("Please enter the year required in the format YYYY: ").strip()
        if not year_input.isdigit() or len(year_input) != 4:
            print("Wrong data type - please enter a four-digit year value.")
        elif int(year_input) < 2000 or int(year_input) > 2025:
            print("Out of range - please enter a value from 2000 to 2025.")
        else:
            return year_input

#other validation
        
def validate_airline_code(): # for task D
    while True:
        code = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
        '''if code not in airline_codes:
            print("Unavailable Airline code - please try again.")
        else:
            return code'''
        if len(code) != 2:
            print("Invalid airline code format - please enter a valid two-character code.")
        elif code not in airline_codes:
            print("Unavailable Airline code - please try again.")
        else:
            return code

def validate_continue(): # for task E
    while True:
        choice = input("Do you want to select a new data file? Y/N: ").strip().upper()
        if choice in ["Y", "N"]:
            if choice == "N":
                print("Thank you. End of run")
            return choice
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
            
#---------------------------------------------------------------------------------------------------------------------------------------------            
#Task B - Outcomes
# Load CSV data

def load_csv(filepath):
    """
    This function loads any csv file by name - set by the var 'selected_data_file' into the list "data_list"
    YOU DO NOT NEED TO CHANGE THIS BLOCK OF CODE
    """
    with open(filepath, "r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        return [row for row in reader]

# Compute outcomes

def compute_outcomes(data):
    # Count the total number of flights
    total_flights = len(data)

    # Count flights departing from Runway 1
    runway_one = sum(1 for r in data if r[8] == "1")

    # Count flights over 500 miles
    over_500 = sum(1 for r in data if int(r[5]) > 500)

    # Count British Airways flights
    british_airways = sum(1 for r in data if r[1][:2] == "BA")

    # Count flights departing in rain
    rain_flights = sum(1 for r in data if "rain" in r[9].lower())

    # Calculate average departures per hour
    departures_per_hour = round(total_flights / 12, 2)

    # Count Air France flights
    air_france = sum(1 for r in data if r[1][:2] == "AF")

    # Count delayed flights (where actual departure != planned departure)
    delayed = sum(1 for r in data if r[2] != r[3])

    # Create a set of hours in which rain fell
    rain_hours = set()
    for r in data:
        if "rain" in r[9].lower():
            rain_hours.add(int(r[2].split(":")[0]))

    # Count occurrences of each destination airport
    dest_counts = defaultdict(int)
    for r in data:
        dest_counts[r[4]] += 1

    # Determine the highest number of departures to a single destination
    max_count = max(dest_counts.values())

    # Create a sorted list of the most common destination airport names
    most_common_dest = sorted({
        airport_codes.get(code, code) for code, count in dest_counts.items() if count == max_count
    })

    return {
        "total_flights": total_flights,
        "runway_one": runway_one,
        "over_500_miles": over_500,
        "british_airways": british_airways,
        "rain_flights": rain_flights,
        "departures_per_hour": departures_per_hour,
        "air_france_percentage": round((air_france / total_flights) * 100, 2) if total_flights else 0,
        "delayed_percentage": round((delayed / total_flights) * 100, 2) if total_flights else 0,
        "rain_hours": len(rain_hours),
        "most_common_dest": most_common_dest
    }

# Display outcomes

#PRINT THE OuTPUT TO SCREEN
def display_outcomes(outcomes):
    print(f"The total number of flights from this airport was {outcomes['total_flights']}.")
    print(f"The total number of flights departing Runway one was {outcomes['runway_one']}.")
    print(f"The total number of departures of flights over 500 miles was {outcomes['over_500_miles']}.")
    print(f"There were {outcomes['british_airways']} British Airways flights from this airport.")
    print(f"There were {outcomes['rain_flights']} flights from this airport departing in rain ")
    print(f"There was an average of {outcomes['departures_per_hour']} flights per hour from this airport.")
    print(f"Air France planes made up {outcomes['air_france_percentage']}% of all departures.")
    print(f"{outcomes['delayed_percentage']}% of all departures were delayed.")
    print(f"There were {outcomes['rain_hours']} hours in which rain fell.")

    # Print the most common destination(s), handling singular and plural cases
    if len(outcomes["most_common_dest"]) == 1:
        print(f"The most common destination is ['{outcomes['most_common_dest'][0]}'].")
    else:
        dest_list = ", ".join(outcomes["most_common_dest"])
        print(f"The most common destinations are ['{dest_list}'].")

#---------------------------------------------------------------------------------------------------------------------------------------------
#Task C - Save Results as a Text File
# Save to file

def save_results(outcomes, file_name, airport_name, year):
    path = "results/" + file_name
    #os.path.join(results_path, file_name)
    with open(path, "a") as f:
        f.write("**********************************************************************\n")
        f.write(f"File {file_name} selected - Planes departing {airport_name} {year}.\n")
        f.write("**********************************************************************\n\n")
        f.write(f"The total number of flights from this airport was {outcomes['total_flights']}.\n")
        f.write(f"The total number of flights departing Runway one was {outcomes['runway_one']}.\n")
        f.write(f"The total number of departures on flights over 500 miles was {outcomes['over_500_miles']}.\n")
        f.write(f"There were {outcomes['british_airways']} British Airways flights from this airport.\n")
        f.write(f"There were {outcomes['rain_flights']} flights from this airport departing in rain.\n")
        f.write(f"There was an average of {outcomes['departures_per_hour']} flights per hour from this airport.\n")
        f.write(f"Air France planes made up {outcomes['air_france_percentage']}% of all departures.\n")
        f.write(f"{outcomes['delayed_percentage']}% of all departures were delayed.\n")
        f.write(f"There were {outcomes['rain_hours']} hours in which rain fell.\n")

        # formatting differently if there is only one or multiple destinations
        if len(outcomes["most_common_dest"]) == 1:
            f.write(f"The most common destination is ['{outcomes['most_common_dest'][0]}'].\n\n")
        else:
            dest_list = ", ".join(outcomes["most_common_dest"])
            f.write(f"The most common destinations are ['{dest_list}'].\n\n")
        f.write("\n\n")

#------------------------------------------------------------------------------------------------------------------------------------------------       
# Task D -  Histogram
# Plot histogram
# references- my previous cw

def plot_histogram(data, airline_code, airport_name, year):
    counts = [0]*12
    for r in data:
        if r[1][:2] == airline_code:
            hour = int(r[2].split(":")[0])
            counts[hour] += 1

    max_count = max(counts)if counts else 1
    if max_count == 0:
        print(f"No departures found for airline {airline_codes[airline_code]} in this file.")
        return  # This will exit the function cleanly and go back to your main loop


    win = GraphWin("Histogram", 900, 405)
    win.setBackground("white")

    # Axes
    Line(Point(60, 350), Point(850, 350)).draw(win)
    #Line(Point(50, 50), Point(50, 350)).draw(win)- to add the y axis 

    # Title
    title = f"Departures by hour for {airline_codes[airline_code]} from {airport_name} {year}"
    Text(Point(450, 25), title).draw(win)

    bar_width = 30
    spacing = 40

    for i, c in enumerate(counts):
        bar_height = (250 * c) / max_count
        x0 = 60 + i * (bar_width + spacing)
        y0 = 350 - bar_height
        x1 = x0 + bar_width
        y1 = 350

        rect = Rectangle(Point(x0, y0), Point(x1, y1))
        rect.setFill("lightgreen")
        rect.setOutline("black")
        rect.draw(win)

        Text(Point((x0 + x1)/2, 360), f"{i:02d}").draw(win)
        Text(Point((x0 + x1)/2, y0 - 10), str(c)).draw(win)

    Text(Point(450, 385), "\nHours 00:00 to 12:00\n").draw(win)


    # Try to get a click safely
    try:
        win.getMouse()
    except GraphicsError:
        pass  # user closed window

    win.close()

#------------------------------------------------------------------------------------------------------------------------------------------------------
# Task E - Program Loops on Request and Loads a New CSV file
# Main loop 

if __name__ == "__main__":
    while True:
        city = validate_city_code()
        year = validate_year()
        airport = airport_codes[city]
        csv_file = f"{city}{year}.csv"# Use data_path so CSV files are loaded from the data file directory 
        '''os.path.join (script_dir, '''
        print("**********************************************************************")
        print(f"File {city}{year}.csv selected - Planes departing {airport} {year}.")
        print("**********************************************************************")

        data = load_csv(csv_file)
        outcomes = compute_outcomes(data)
        display_outcomes(outcomes)
        save_results(outcomes, "results.txt", airport, year)

        airline = validate_airline_code()
        plot_histogram(data, airline, airport, year)

        if validate_continue() == "N":
            break

