def calculate_di(pop, a, dmin, dmax):
    """
    Calculate the Density Index (DI) given the location's population (pop),
    , minimum density (Dmin), and maximum density (Dmax).
    """
    ld = pop / a
    di = (ld - dmin) / (dmax - dmin)
    return di


def calculate_ai(at, tmax=30, tmin=5):
    """
    Calculate an Amenity Index (AI) given the time to the amenity (At),
    the maximum time to the amenity (Tmax), and the minimum time to the amenity (Tmin).
    """
    ai = (tmax - at) / (tmax - tmin)
    return ai


def calculate_fmi(di, divi, pi, dw, divw, pw):
    """
    Calculate the 15 Minute City Index (FMI) given the Density Index (DI),
    Diversity Index (DivI), and weighted Proximity Index (PI_weighted).
    """
    fmi = di * dw + divi * divw + pi * pw
    return fmi
