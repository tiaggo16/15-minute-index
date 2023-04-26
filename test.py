from main import handle_inputs, fmi_method

handled_inputs = handle_inputs(
    {
        "lat": "19.071304",
        "long": "47.489314",
        "walking_time": "15",
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
)

result = fmi_method(handled_inputs)

print(result)
