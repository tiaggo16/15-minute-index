from main import handle_inputs, fmi_method

inputs = {
    "user": "grandma",
    "place": "suburb",
    "long": "-122.471036",
    "lat": "37.769459",
    "walking_time": "20",
    "amenity1": "hospital",
    "amenity2": "church",
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


handled_inputs = handle_inputs(inputs)
result = fmi_method(handled_inputs)
print(result)
