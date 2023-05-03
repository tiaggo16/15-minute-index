from calculations import calculate_di, calculate_divi, calculate_pi, calculate_fmi
from ahp import get_weights
from ors import get_auth_client, get_isochrone_data, get_amenity_pois

import re


amenity_mapping = {
    "kindergarten": {
        "osm_code": [153],
        "qmax": 10,
        "qmin": 0,
    },
    "supermarket": {
        "osm_code": [518],
        "qmax": 25,
        "qmin": 0,
    },
    "church": {
        "osm_code": [135],
        "qmax": 5,
        "qmin": 0,
    },
    "bank": {
        "osm_code": [192],
        "qmax": 10,
        "qmin": 0,
    },
    "school": {
        "osm_code": [156],
        "qmax": 15,
        "qmin": 0,
    },
    "university": {
        "osm_code": [157],
        "qmax": 5,
        "qmin": 0,
    },
    "hospital": {
        "osm_code": [206],
        "qmax": 10,
        "qmin": 0,
    },
    "park": {
        "osm_code": [280],
        "qmax": 20,
        "qmin": 0,
    },
    "restaurant": {
        "osm_code": [570],
        "qmax": 25,
        "qmin": 0,
    },
    "bar": {
        "osm_code": [561],
        "qmax": 40,
        "qmin": 0,
    },
    "cafe": {
        "osm_code": [564],
        "qmax": 40,
        "qmin": 0,
    },
}

ratios_mapping = {
    "center": (0.0858, 0.3273, 0.1984, 0.2572, 0.0927, 0.0386),
    "suburb": (0.1285, 0.1074, 0.1506, 0.5786, 0.0344, 0.004),
    "uni": (0.6960, 0.0643, 0.0124, 0.1927, 0.0332, 0.0013),
}


def handle_inputs(inputs):
    # inverts value if right option is prefered
    for key in inputs:
        if not re.search('[a-zA-Z]', inputs[key]):
            inputs[key] = float(inputs[key])
    for key in inputs:
        preference_key = key + "-pref"
        if preference_key in inputs and inputs[preference_key] == "right":
            inputs[key] = inputs[key] ** (-1)

    return inputs


def fmi_method(inputs):
    # if "user" not in inputs:
    #    inputs["user"] = "not_set"
    # if "place" not in inputs:
    #    inputs["place"] = "center"

    ors_client = get_auth_client()
    # set initial location data
    location = dict()
    location["walking_time"] = inputs["walking_time"]
    location["long"] = inputs["long"]
    location["lat"] = inputs["lat"]
    location["amenities"] = (
        inputs["amenity1"], inputs["amenity2"], inputs["amenity3"])
    # calculate weights according to user input
    weights = get_weights(
        inputs["avb"],
        inputs["avc"],
        inputs["bvc"],
        inputs["pavb"],
        inputs["pavc"],
        inputs["pbvc"],
    )
    dw = weights["dw"]
    divw = weights["divw"]
    pw = weights["pw"]

    # get isochrone, its area and population
    location["iso"] = get_isochrone_data(
        ors_client, location)
    # return location["iso"]["features"][0]
    iso_area = location["iso"]["features"][0]["properties"]["area"]
    iso_pop = location["iso"]["features"][0]["properties"]["total_pop"]

    # calculate the Density Index (DI)
    di = calculate_di(iso_pop, iso_area)

    # calculate the Density Index (DI)
    place = inputs["place"]
    land_use_ratios = ratios_mapping[place]
    divi = calculate_divi(land_use_ratios)

    # get amenity POIs
    location["amenity_pois"] = get_amenity_pois(
        ors_client, location, amenity_mapping)

    # calculate the weighted proximity index (PI)
    pi = calculate_pi(location, weights, amenity_mapping)

    # calculate the 15 Minute City Index (FCI)
    fmi = calculate_fmi(di, divi, pi, dw, divw, pw)

    # return indexes
    # return {"indexes": {"fmi": fmi, "di": di, "divi": divi, "pi": pi}, "weights": weights}
    return {f"{inputs['user']}_{inputs['place']}": {"fmi": fmi, "di": di, "divi": divi, "pi": pi, "pop": iso_pop, "area": iso_area, "weights": weights}}
