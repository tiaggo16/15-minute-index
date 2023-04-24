from calculations import calculate_di, calculate_ai, calculate_fmi
from inputs import dmin, dmax, at1, at2, at3, divi
from ahp import get_weights
from ors import get_auth_client, get_isochrone_data


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
    # set base params
    walking_time = inputs["walking_time"]

    # calculate weights according to user input
    w = get_weights(
        inputs["avb"],
        inputs["avc"],
        inputs["bvc"],
        inputs["pavb"],
        inputs["pavc"],
        inputs["pbvc"],
    )
    dw = w["dw"]
    divw = w["divw"]
    pw = w["pw"]
    aw1 = w["aw1"]
    aw2 = w["aw2"]
    aw3 = w["aw3"]

    # get isochrone, area and population
    isochrone_data = get_isochrone_data(ors_client, 19.071304, 47.489314, walking_time)

    isochrone = isochrone_data["features"][0]["geometry"]["coordinates"][0]
    area = isochrone_data["features"][0]["properties"]["area"]
    population = isochrone_data["features"][0]["properties"]["total_pop"]

    # calculate the Density Index (DI)
    di = calculate_di(population, area, dmin, dmax)

    # calculate the Amenity Index 1 (AI1)
    ai1 = calculate_ai(at1)

    # calculate the Amenity Index 2 (AI2)
    ai2 = calculate_ai(at2)

    # calculate the Amenity Index 3 (AI3)
    ai3 = calculate_ai(at3)

    # calculate the weighted proximity index (PI)
    pi = ai1 * aw1 + ai2 * aw2 + ai3 * aw3

    # calculate the 15 Minute City Index (FCI)
    fmi = calculate_fmi(di, divi, pi, dw, divw, pw)

    # return indexes
    return {"indexes": {"fmi": fmi, "di": di, "divi": divi, "pi": pi}, "weights": w}
