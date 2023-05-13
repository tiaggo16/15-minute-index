from numpy import clip, log


def calculate_di(iso_pop, iso_area):
    dmin = 300
    dmax = 9200
    iso_density = iso_pop / iso_area
    di = (iso_density - dmin) / (dmax - dmin)
    return clip(round(di, 4), 0, 1)


def calculate_hhi(ratios):
    if round(sum(ratios), 2) != 1:
        print("Wrong land use ratios - sum not equal to 1")
        return
    hhi = 1 - sum(r*r for r in ratios)
    return hhi


def calculate_entropy(ratios):
    if round(sum(ratios), 2) != 1:
        print("Wrong land use ratios - sum not equal to 1")
        return
    log_ratios = map(log, ratios)
    num_lu_types = len(ratios)
    sum_types = 0

    for r, log_r in zip(ratios, log_ratios):
        sum_types = sum_types + (r*log_r)

    entropy = -1 * (sum_types/log(num_lu_types))

    return entropy


def calculate_divi(land_use_ratios):
    # takes tuple with ratios of land uses, must add up to 1
    ent = calculate_entropy(land_use_ratios)
    hhi = calculate_hhi(land_use_ratios)
    divi = (ent + hhi)/2
    return clip(round(divi, 4), 0, 1)


def calculate_ai(location, i, amenity_mapping):
    # Calculate proximity component
    tmax = 30
    tmin = 0
    tt_amenity = location["amenity_data"][location["amenities"][i]]["min_tt_to_amenity"]
    ai_prox = clip((tmax - tt_amenity) / (tmax - tmin), 0, 1)

    # Calculate quantity component
    qmax = amenity_mapping[location["amenities"][i]]["qmax"]
    qmin = amenity_mapping[location["amenities"][i]]["qmin"]
    quant = location["amenity_data"][location["amenities"][i]]["number"]

    ai_quant = clip((quant - qmin) / (qmax - qmin), 0, 1)

    ai = (ai_quant + ai_prox) / 2
    return clip(round(ai, 4), 0, 1)


def calculate_pi(location, weights, amenity_mapping):
    ai1 = calculate_ai(location, 0, amenity_mapping)
    ai2 = calculate_ai(location, 1, amenity_mapping)
    ai3 = calculate_ai(location, 2, amenity_mapping)
    pi = ai1 * weights["aw1"] + ai2 * weights["aw2"] + ai3 * weights["aw3"]

    return clip(round(pi, 4), 0, 1)


def calculate_fmi(di, divi, pi, dw, divw, pw):
    fmi = di * dw + divi * divw + pi * pw
    return clip(round(fmi, 4), 0, 1)
