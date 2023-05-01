import openrouteservice
import folium


def get_auth_client():
    client = openrouteservice.Client(
        key="5b3ce3597851110001cf6248ed7c285472d0424fa3355fcc32430803"
    )
    return client


def get_isochrone_data(client, location):
    # Set the locations coordinate for request
    lat = location["lat"]
    long = location["long"]
    locations = [[lat, long]]

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
    create_map_with_iso_file(isochrone, long, lat)
    print(isochrone["features"][0])
    return isochrone


def create_map_with_iso_file(isochrone, long, lat):
    # map
    map_isochrone = folium.Map(
        location=[long, lat], tiles="cartodbpositron", zoom_start=12
    )

    # add geojson to map with population
    population = isochrone["features"][0]["properties"]["total_pop"]
    folium.GeoJson(
        isochrone, name="isochrone", tooltip=f"population: {population:,.0f}"
    ).add_to(map_isochrone)

    # add marker to map
    minutes = isochrone["features"][0]["properties"]["value"] / 60
    popup_message = f"outline shows areas reachable within {minutes} minutes"
    folium.Marker([long, lat], popup=popup_message, tooltip="click").add_to(
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


def get_amenity_pois(client, location, amenity_mapping):
    isochrone = location["iso"]
    params_poi = {"request": "pois", "sortby": "distance"}
    categories_poi = build_categories_poi(
        location["amenities"], amenity_mapping)

    amenity_pois = dict()  # Store in pois dict for easier retrieval
    amen_pois = dict()  # Store just number of pois for each category
    params_poi["geojson"] = isochrone["features"][0]["geometry"]

    for typ, category in categories_poi.items():
        params_poi["filter_category_ids"] = category
        amenity_pois[typ] = dict()
        # create key for my second amenity thing that will have less data
        amen_pois[typ] = dict()
        amenity_pois[typ]["geojson"] = client.places(**params_poi)[
            "features"
        ]  # Actual POI request
        amen_pois[typ] = len(
            amenity_pois[typ]['geojson'])
        print(f"\t{typ}: {len(amenity_pois[typ]['geojson'])}")

    # currently using amen_pois to return only the number
    # of pois, not extra data about each amenity poi
    return amen_pois
