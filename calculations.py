def calculate_di(iso_pop, iso_area, dmin, dmax):
    """
    Calculate the Density Index (DI) given the location's population (pop),
    , minimum density (Dmin), and maximum density (Dmax).
    """
    iso_density = iso_pop / iso_area
    di = (iso_density - dmin) / (dmax - dmin)
    return round(di, 4)


def calculate_ai(location, key, qmax=100, qmin=0):
    quant = location["amenity_pois"][key]
    ai = (quant - qmin / qmax - qmin) / 100
    return round(ai, 4)

    # AMENITY INDEX FORMULA USING ROUTE TIME INSTEAD OF QUANTITY
    """
    Calculate an Amenity Index (AI) given the time to the amenity (At),
    the maximum time to the amenity (Tmax), and the minimum time to the amenity (Tmin).
    """
    # (tmax = 30, tmin = 5)
    # ai = (tmax - at) / (tmax - tmin)
    # return round(ai, 4)


def calculate_pi(location, weights, qmax=100, qmin=0):

    ai1 = calculate_ai(location, "kindergarten")
    ai2 = calculate_ai(location, "supermarket")
    ai3 = calculate_ai(location, "hairdresser")
    pi = ai1 * weights["aw1"] + ai2 * weights["aw2"] + ai3 * weights["aw3"]
    breakpoint()


def calculate_fmi(di, divi, pi, dw, divw, pw):
    """
    Calculate the 15 Minute City Index (FMI) given the Density Index (DI),
    Diversity Index (DivI), and weighted Proximity Index (PI_weighted).
    """
    fmi = di * dw + divi * divw + pi * pw
    return round(fmi, 4)
