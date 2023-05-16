from calculations import calculate_di, calculate_divi, calculate_pi, calculate_fmi
from ahp import get_weights
from ors import get_auth_client, get_isochrone_data, get_amenities_number_and_travel_time

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
    "euclidean_suburb": (0.2172, 0.5655, 0.0917, 0.0232, 0.0003, 0.1021),
    "buda": (0.0610, 0.0001, 0.2897, 0.6490, 0.0001, 0.0001),
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

    """location["iso"] = {'type': 'FeatureCollection',
    'bbox': [-122.473082, 37.737852, -122.450759, 37.758216],
    'features': [{
        'type': 'Feature',
        'properties': {
            'group_index': 0,
            'value': 900.0,
            'center': [-122.46272434240032, 37.74736788820083],
            'area': 4.908739,
            'total_pop': 21756.0},
        'geometry': {'coordinates': [[[-122.462732, 37.75859994105149], [-122.46550288005423, 37.758384147667186], [-122.46816722979307, 37.75774506402567], [-122.47062261995363, 37.7567072602682], [-122.47277466468661, 37.75531063434707], [-122.47454065279877, 37.753608876372375], [-122.47585272771465, 37.751667402504346], [-122.4766604937375, 37.7495608382213], [-122.47693294867231, 37.747370148110285], [-122.47665966915979, 37.74517952284551], [-122.47585120409373, 37.74307314322893], [-122.4745386620921, 37.741131945733805], [-122.47277250996116, 37.73943051376319], [-122.47062062924687, 37.73803421384614], [-122.46816570617203, 37.7369966864616], [-122.46550205547646, 37.73635778748656], [-122.462732, 37.73614205894851], [-122.45996194452354, 37.73635778748656], [-122.45729829382798, 37.7369966864616], [-122.45484337075315, 37.73803421384614], [-122.45269149003884, 37.73943051376319], [-122.45092533790792, 37.741131945733805], [-122.44961279590629, 37.74307314322893], [-122.44880433084023, 37.74517952284551], [-122.4485310513277, 37.747370148110285], [-122.44880350626252, 37.7495608382213], [-122.44961127228537, 37.751667402504346], [-122.45092334720124, 37.753608876372375], [-122.4526893353134, 37.75531063434707], [-122.45484138004639, 37.7567072602682], [-122.45729677020695, 37.75774506402567], [-122.45996111994577, 37.758384147667186], [-122.462732, 37.75859994105149]]], 'type': 'Polygon'}}],
    'metadata': {'attribution': 'openrouteservice.org | OpenStreetMap contributors', 'service': 'isochrones', 'timestamp': 1684054295315, 'query': {'profile': 'foot-walking', 'locations': [[-122.462732, 37.747371]], 'range': [900.0], 'range_type': 'time', 'units': 'km', 'attributes': ['area', 'total_pop']}, 'engine': {'version': '6.8.1', 'build_date': '2023-02-27T01:00:29Z', 'graph_date': '2023-04-29T05:28:04Z'}
    }
    } """

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

    # get amenity data
    location["amenity_data"] = get_amenities_number_and_travel_time(
        ors_client, location, amenity_mapping)

    # calculate the Proximity index (PI)
    pi = calculate_pi(location, weights, amenity_mapping)

    # calculate the 15 Minute City Index (FCI)
    fmi = calculate_fmi(di, divi, pi, dw, divw, pw)

    # return indexes
    # return {"indexes": {"fmi": fmi, "di": di, "divi": divi, "pi": pi}, "weights": weights}
    return {f"{inputs['user']}_{inputs['place']}": {"fmi": fmi, "di": di, "divi": divi, "pi": pi, "pop": iso_pop, "area": iso_area, "amenity_data": location["amenity_data"], "weights": weights}}
