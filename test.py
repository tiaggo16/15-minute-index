from main import handle_inputs, fmi_method

list_of_inputs = [
    {
        "lat": "-122.455072",
        "long": "37.6900013",
        "walking_time": "15",
        "amenity1": "kindergarten",
        "amenity2": "university",
        "amenity3": "supermarket",
        "avb-pref": "left",
        "avb": "2",
        "avc-pref": "right",
        "avc": "5",
        "bvc-pref": "right",
        "bvc": "3",
        "pavb-pref": "left",
        "pavb": "3",
        "pavc-pref": "left",
        "pavc": "5",
        "pbvc-pref": "left",
        "pbvc": "2",
    },
    {
        "lat": "-122.455072",
        "long": "37.6900013",
        "walking_time": "15",
        "amenity1": "kindergarten",
        "amenity2": "university",
        "amenity3": "supermarket",
        "avb-pref": "left",
        "avb": "2",
        "avc-pref": "right",
        "avc": "5",
        "bvc-pref": "right",
        "bvc": "3",
        "pavb-pref": "left",
        "pavb": "3",
        "pavc-pref": "left",
        "pavc": "5",
        "pbvc-pref": "left",
        "pbvc": "2",
    }
]
for inputs in list_of_inputs:
    handled_inputs = handle_inputs(inputs)
    result = fmi_method(handled_inputs)
    print(result)
