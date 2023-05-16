from main import handle_inputs, fmi_method
# budacoords:  "long": "19.070103", "lat": "47.479758"
inputs = {
        "user": "student",
        "place": "buda",
        "long": "19.070103",
        "lat": "47.479758",
        "walking_time": "15",
        "amenity1": "university",
        "amenity2": "bar",
        "amenity3": "cafe",
        "avb-pref": "left",
        "avb": "3",
        "avc-pref": "left",
        "avc": "2",
        "bvc-pref": "right",
        "bvc": "3",
        "pavb-pref": "left",
        "pavb": "4",
        "pavc-pref": "left",
        "pavc": "6",
        "pbvc-pref": "left",
        "pbvc": "3",
}



handled_inputs = handle_inputs(inputs)
result = fmi_method(handled_inputs)
print(result)
