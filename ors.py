import itertools
import openrouteservice
import folium
import time


def get_auth_client():
    client = openrouteservice.Client(
        key="5b3ce3597851110001cf6248ed7c285472d0424fa3355fcc32430803"
    )
    return client


def get_isochrone_data(client, location):
    # Set the locations coordinate for request
    long = location["long"]
    lat = location["lat"]
    locations = [[long, lat]]

    # Set the walking time in seconds
    walking_time = [location["walking_time"] * 60]
    mobility_modal = "foot-walking"

    # Make API request for isochrone data
    isochrone = openrouteservice.isochrones.isochrones(
        client,
        locations,
        profile=mobility_modal,
        range_type="time",
        range=walking_time,
        intervals=None,
        segments=None,
        interval=None,
        units="km",
        location_type=None,
        smoothing=None,
        attributes=["area", "total_pop"],
    )
    create_map_with_iso_file(isochrone, lat, long)

    return isochrone


def create_map_with_iso_file(isochrone, lat, long):
    # map
    map_isochrone = folium.Map(
        location=[lat, long], tiles="cartodbpositron", zoom_start=12
    )

    # add geojson to map with population
    population = isochrone["features"][0]["properties"]["total_pop"]
    folium.GeoJson(
        isochrone, name="isochrone", tooltip=f"population: {population:,.0f}"
    ).add_to(map_isochrone)

    # add marker to map
    minutes = isochrone["features"][0]["properties"]["value"] / 60
    popup_message = f"outline shows areas reachable within {minutes} minutes"
    folium.Marker([lat, long], popup=popup_message, tooltip="click").add_to(
        map_isochrone
    )

    # add layer control to map (allows layer to be turned on or off)
    folium.LayerControl().add_to(map_isochrone)

    # display map
    map_isochrone.save("templates/map.html")


def build_categories_poi(categories, amenity_mapping):
    # POI categories according to
    # https://giscience.github.io/openrouteservice/documentation/Places.html
    categories_poi = {}
    for cat in categories:
        categories_poi[cat] = amenity_mapping[cat]["osm_code"]
    return categories_poi


def get_amenity_pois_by_category(client, loc, amenity_mapping):
    params_poi = {"request": "pois", "sortby": "distance"}
    categories_poi = build_categories_poi(
        loc["amenities"], amenity_mapping)

    amenity_pois_by_category = dict()
    params_poi["geojson"] = loc["iso"]["features"][0]["geometry"]

    for typ, category in categories_poi.items():
        params_poi["filter_category_ids"] = category
        amenity_pois_by_category[typ] = dict()

        amenity_pois_by_category[typ]["geojson"] = client.places(**params_poi)[
            "features"
        ]  # Actual POI request

        print(f"\t{typ}: {len(amenity_pois_by_category[typ]['geojson'])}")

    return amenity_pois_by_category


def get_travel_times_to_closest_amenities(client, location, amenity_pois_by_category):
    # Set up common request parameters
    params_route = {'profile': 'foot-walking',
                    'format_out': 'geojson',
                    'geometry': 'true',
                    'format': 'geojson',
                    'instructions': 'false',
                    }
    # Store all routes to POIs
    min_travel_times = []
    for cat, pois in amenity_pois_by_category.items():
        poi_durations = []
        print("Sleeping 60s before asking ORS API for routes.")
        time.sleep(60)
        for poi in itertools.islice(pois['geojson'], 40):
            poi_coords = poi['geometry']['coordinates']

            # Perform actual request
            params_route['coordinates'] = [[location['long'], location['lat']],
                                           poi_coords
                                           ]
            json_route = client.directions(**params_route)
            poi_duration = json_route['features'][0]['properties']['summary']['duration']
            # Record durations of routes
            poi_durations.append(poi_duration)
        if poi_durations:
            min_travel_times.append(round(min(poi_durations) / 60, 1))
        else:
            # if no amenity, uses 30 min, the maximum distance. Therefore, AI = 0.
            min_travel_times.append(30.0)
    print(min_travel_times)
    return min_travel_times


def get_number_of_amenities(amenity_pois_by_category):
    amen_number_list = []
    for key, value in amenity_pois_by_category.items():
        amen_number_list.append(len(value["geojson"]))
    return amen_number_list


def get_amenities_number_and_travel_time(client, location, amenity_mapping):
    amenity_dict = {}
    amenity_keys = location["amenities"]

    amenity_pois_by_category = get_amenity_pois_by_category(
        client, location, amenity_mapping)
    number_of_amenities = get_number_of_amenities(amenity_pois_by_category)

    min_tt_to_amenity = get_travel_times_to_closest_amenities(
        client, location, amenity_pois_by_category)


    for key, number, min_tt_to_amenity in zip(amenity_keys, number_of_amenities, min_tt_to_amenity):
        amenity_dict[key] = {
            "number": number,
            "min_tt_to_amenity": min_tt_to_amenity,
        }

    return amenity_dict
