from datetime import datetime

def calc_fuel_litres(fuel_added: float, fuel_rate: float) -> float:
    """
    Calculate the amount of fuel in litres based on fuel added and fuel consumption rate.

    Parameters:
    fuel_added (float): The amount of fuel added in liters.
    fuel_rate (float): The rate at which fuel is consumed (liters per unit distance).

    Returns:
    float: Calculated fuel in litres.
    """
    try:
        return fuel_added / fuel_rate
    except ZeroDivisionError:
        return 0


def calc_fuel_litres_adjusted(fuel_litres: float, distance_reserve: float = 0, mean_average: float = 45) -> float:
    """
    Adjust fuel litres by accounting for a reserve distance.

    Parameters:
    fuel_litres (float): The initial amount of fuel in litres.
    distance_reserve (float): from the row above calculated using calc_distance_reserve().
    mean_average (float): The average distance covered per litre of fuel (default is 45).

    Returns:
    float: Adjusted fuel litres.
    """
    return fuel_litres - (distance_reserve / mean_average)


def calc_upcoming_fueling(fuel_addition_mileage: float, fuel_litres_adjusted: float, fuel_avg: float) -> float:
    """
    Calculate the upcoming mileage where refueling will be required.

    Parameters:
    fuel_addition_mileage (float): The mileage when fuel was added.
    fuel_litres_adjusted (float): Adjusted fuel litres available after reserve adjustment. From calc_fuel_litres_adjusted()
    fuel_avg (float): The average mileage per litre. From calc_fuel_avg()

    Returns:
    float: The estimated mileage for the next fueling.
    """
    return fuel_addition_mileage + (fuel_litres_adjusted * fuel_avg)


def calc_distance_reserve(fuel_addition_mileage: float, reserve_switch_mileage: float) -> float:
    """
    Calculate the reserve distance based on fueling and reserve switch mileage.

    Parameters:
    fuel_addition_mileage (float): The mileage when fuel was added.
    reserve_switch_mileage (float): The mileage at which the reserve fuel indicator switched.

    Returns:
    float: The calculated reserve distance.
    """
    return fuel_addition_mileage - reserve_switch_mileage


def calc_distance_fuel_adjusted(reserve_switch_mileage: float, fuel_addition_mileage: float) -> float:
    """
    Calculate the adjusted distance that can be traveled on the remaining fuel.

    Parameters:
    reserve_switch_mileage (float): The mileage at which reserve fuel is indicated.
    fuel_addition_mileage (float): The mileage when fuel was added. From row above

    Returns:
    float: The distance that can be traveled based on fuel adjustments.
    """
    return reserve_switch_mileage - fuel_addition_mileage


def calc_fuel_avg(distance_fuel_adjusted: float, fuel_litres_adjusted: float) -> float:
    """
    Calculate the average fuel consumption rate.

    Parameters:
    distance_fuel_adjusted (float): The adjusted distance covered on fuel.
    fuel_litres_adjusted (float): Adjusted fuel in litres.

    Returns:
    float: The calculated average fuel consumption (km per litre).
    """
    try:
        return distance_fuel_adjusted / fuel_litres_adjusted
    except ZeroDivisionError:
        return 0


def calc_travel_avg(distance_fuel_adjusted: float, fuel_days_lasted: int) -> float:
    """
    Calculate the average distance traveled per day based on the adjusted fuel.

    Parameters:
    distance_fuel_adjusted (float): The adjusted distance that can be covered on fuel.
    fuel_days_lasted (int): The number of days the fuel lasted.

    Returns:
    float: Average distance traveled per day.
    """
    try:
        return distance_fuel_adjusted / fuel_days_lasted
    except ZeroDivisionError:
        return 0


def calc_fuel_days_lasted(date_current_row: str, date_previous_row: str) -> int:
    """
    Calculate the number of days that fuel has lasted based on two dates in string format.

    Parameters:
    date_current_row (str): The current date of the record, in "YYYY-MM-DD" format.
    date_previous_row (str): The previous date of the record, in "YYYY-MM-DD" format.

    Returns:
    int: The number of days between the two dates.
    """
    date_current = datetime.strptime(date_current_row, "%Y-%m-%d")
    date_previous = datetime.strptime(date_previous_row, "%Y-%m-%d")

    difference = date_current - date_previous
    return difference.days


def process_fuel_data(fuel_record_list):
    index = len(fuel_record_list) - 1
    calculated_record = {}
    calculated_record["fuel_litres"] = calc_fuel_litres(fuel_added=0 if index == 0 else fuel_record_list[index - 1]["fuel_added"],fuel_rate=0 if index == 0 else fuel_record_list[index - 1]["fuel_rate"],)
    calculated_record["distance_on_reserve"] = calc_distance_reserve(
        fuel_addition_mileage=(
            0 if index == 0 else fuel_record_list[index - 1]["fuel_addition_mileage"]
        ),
        reserve_switch_mileage=(
            0 if index == 0 else fuel_record_list[index - 1]["reserve_switch_mileage"]
        ),
    )
    calculated_record["fuel_litres_adjusted"] = calc_fuel_litres_adjusted(
        fuel_litres=calculated_record["fuel_litres"],
        distance_reserve=calculated_record["distance_on_reserve"],
    )
    calculated_record["distance_fuel_adjusted"] = calc_distance_fuel_adjusted(
        reserve_switch_mileage=fuel_record_list[index]['reserve_switch_mileage'],
        fuel_addition_mileage=(
            0 if index == 0 else fuel_record_list[index - 1]["fuel_addition_mileage"]
        ),
    )
    calculated_record["fuel_average"] = calc_fuel_avg(
        distance_fuel_adjusted=calculated_record["distance_fuel_adjusted"],
        fuel_litres_adjusted=calculated_record["fuel_litres_adjusted"],
    )
    calculated_record["upcoming_fueling"] = calc_upcoming_fueling(
        fuel_addition_mileage=fuel_record_list[index]["fuel_addition_mileage"],
        fuel_litres_adjusted=calculated_record["fuel_litres_adjusted"],
        fuel_avg=calculated_record["fuel_average"],
    )
    calculated_record["fuel_days"] = calc_fuel_days_lasted(
        date_current_row=fuel_record_list[index]["fueling_date"],
        date_previous_row=(
            fuel_record_list[index]["fueling_date"] if index == 0 else fuel_record_list[index - 1]["fueling_date"]
        ),
    )
    calculated_record["travel_avg"] = calc_travel_avg(
        distance_fuel_adjusted=calculated_record["distance_fuel_adjusted"],
        fuel_days_lasted=calculated_record["fuel_days"],
    )

    return calculated_record