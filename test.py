from main import handle_inputs, fmi_method

inputs = {
        "user": "adult",
        "place": "suburb",
        "long": "19.070103",
        "lat": "47.479758",
        "walking_time": "15",
        "amenity1": "kindergarten",
        "amenity2": "restaurant",
        "amenity3": "bank",
        "avb-pref": "right",
        "avb": "3",
        "avc-pref": "right",
        "avc": "3",
        "bvc-pref": "left",
        "bvc": "1",
        "pavb-pref": "left",
        "pavb": "7",
        "pavc-pref": "left",
        "pavc": "5",
        "pbvc-pref": "right",
        "pbvc": "3",
}



handled_inputs = handle_inputs(inputs)
result = fmi_method(handled_inputs)
print(result)
