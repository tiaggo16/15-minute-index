import ahpy


def get_weights(avb, avc, bvc, pavb, pavc, pbvc):
    criteria_comparisons = {
        ("density", "diversity"): avb,
        ("density", "proximity"): avc,
        ("diversity", "proximity"): bvc,
    }

    proximity_comparisons = {
        ("amenity_1", "amenity_2"): pavb,
        ("amenity_1", "amenity_3"): pavc,
        ("amenity_2", "amenity_3"): pbvc,
    }

    criteria = ahpy.Compare(
        "Criteria", criteria_comparisons, precision=3, random_index="saaty"
    )

    proximity = ahpy.Compare(
        "Proximity", proximity_comparisons, precision=3, random_index="saaty"
    )
    if criteria.consistency_ratio > 0.1 or proximity.consistency_ratio > 0.1:
        print(
            "The priorities given for the criteria are too inconsistent. Please verify values.")
        return

    weights = {
        "dw": criteria.target_weights["density"],
        "divw": criteria.target_weights["diversity"],
        "pw": criteria.target_weights["proximity"],
        "aw1": proximity.target_weights["amenity_1"],
        "aw2": proximity.target_weights["amenity_2"],
        "aw3": proximity.target_weights["amenity_3"],
        "g_cr": criteria.consistency_ratio,
        "p_cr": proximity.consistency_ratio,
    }

    return weights
