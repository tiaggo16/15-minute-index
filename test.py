from main import handle_inputs, fmi_method

list_of_inputs = [
    # SF center with high density
    {
        "lat": "-122.427005",
        "long": "37.772705",
        "walking_time": "15",
        "amenity1": "kindergarten",
        "amenity2": "university",
        "amenity3": "supermarket",
        "avb-pref": "left",
        "avb": "2",
        "avc-pref": "left",
        "avc": "2",
        "bvc-pref": "left",
        "bvc": "2",
        "pavb-pref": "left",
        "pavb": "2",
        "pavc-pref": "left",
        "pavc": "2",
        "pbvc-pref": "left",
        "pbvc": "2",
    },
    # SF suburb in a shitty cornered location
    {
        "lat": "-122.455072",
        "long": "37.6900013",
        "walking_time": "15",
        "amenity1": "kindergarten",
        "amenity2": "university",
        "amenity3": "supermarket",
        "avb-pref": "left",
        "avb": "2",
        "avc-pref": "left",
        "avc": "2",
        "bvc-pref": "left",
        "bvc": "2",
        "pavb-pref": "left",
        "pavb": "2",
        "pavc-pref": "left",
        "pavc": "2",
        "pbvc-pref": "left",
        "pbvc": "2",
    }
]
for inputs in list_of_inputs:
    handled_inputs = handle_inputs(inputs)
    result = fmi_method(handled_inputs)
    print(result)
