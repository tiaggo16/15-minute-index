from calculations import calculate_di, calculate_divi, calculate_pi, calculate_fmi
from inputs import at1, at2, at3, land_use_ratios
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
    "hairdresser": {
        "osm_code": [395],
        "qmax": 20,
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
    ors_client = get_auth_client()

    # set initial location data
    location = dict()
    location["walking_time"] = inputs["walking_time"]
    location["lat"] = inputs["lat"]
    location["long"] = inputs["long"]
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

    iso_area = location["iso"]["features"][0]["properties"]["area"]
    iso_pop = location["iso"]["features"][0]["properties"]["total_pop"]

    # calculate the Density Index (DI)
    di = calculate_di(iso_pop, iso_area)

    # calculate the Density Index (DI)
    divi = calculate_divi(land_use_ratios)

    # get amenity POIs
    location["amenity_pois"] = get_amenity_pois(
        ors_client, location, amenity_mapping)

    # calculate the weighted proximity index (PI)
    pi = calculate_pi(location, weights, amenity_mapping)

    # calculate the 15 Minute City Index (FCI)
    fmi = calculate_fmi(di, divi, pi, dw, divw, pw)

    # return indexes
    return {"indexes": {"fmi": fmi, "di": di, "divi": divi, "pi": pi}, "weights": weights}
