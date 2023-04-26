from ors import get_auth_client, get_isochrone_data, get_pois_inside_isochrone

location = {
    "lat": 19.071304,
    "long": 47.489314,
    "walking_time": 15,
}

client = get_auth_client()

isochrone = get_isochrone_data(client, location)

pois = get_pois_inside_isochrone(client, isochrone)
