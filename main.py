from calculations import calculate_di, calculate_ai, calculate_pi, calculate_fmi
from inputs import dmin, dmax, at1, at2, at3, divi
from ahp import get_weights
from ors import get_auth_client, get_isochrone_data, get_amenity_pois


def handle_inputs(inputs):
    # inverts value if right option is prefered
    for key in inputs:
        if "-pref" not in key:
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
    aw1 = weights["aw1"]
    aw2 = weights["aw2"]
    aw3 = weights["aw3"]

    # get isochrone, its area and population
    location["iso"] = get_isochrone_data(
        ors_client, location)

    isochrone = location["iso"]["features"][0]["geometry"]["coordinates"][0]
    iso_area = location["iso"]["features"][0]["properties"]["area"]
    iso_pop = location["iso"]["features"][0]["properties"]["total_pop"]

    # calculate the Density Index (DI)
    di = calculate_di(iso_pop, iso_area, dmin, dmax)

    # get amenity POIs
    location["amenity_pois"] = get_amenity_pois(ors_client, location)

    # calculate the weighted proximity index (PI)
    pi = calculate_pi(location, weights)

    # calculate the 15 Minute City Index (FCI)
    fmi = calculate_fmi(di, divi, pi, dw, divw, pw)

    # return indexes
    return {"indexes": {"fmi": fmi, "di": di, "divi": divi, "pi": pi}, "weights": weights}
