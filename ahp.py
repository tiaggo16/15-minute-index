import ahpy


def get_weights(avb, avc, bvc, pavb, pavc, pbvc):
    criteria_comparisons = {
        ("Density", "Diversity"): avb,
        ("Density", "Proximity"): avc,
        ("Diversity", "Proximity"): bvc,
    }

    proximity_comparisons = {
        ("Grocery Shop", "School"): pavb,
        ("Grocery Shop", "Mall"): pavc,
        ("School", "Mall"): pbvc,
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
        "dw": criteria.target_weights["Density"],
        "divw": criteria.target_weights["Diversity"],
        "pw": criteria.target_weights["Proximity"],
        "aw1": proximity.target_weights["Grocery Shop"],
        "aw2": proximity.target_weights["School"],
        "aw3": proximity.target_weights["Mall"],
        "g_cr": criteria.consistency_ratio,
        "p_cr": proximity.consistency_ratio,
    }

    return weights
