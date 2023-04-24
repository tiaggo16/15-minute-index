import openrouteservice
import folium
import json


def get_auth_client():
    client = openrouteservice.Client(
        key="5b3ce3597851110001cf6248ed7c285472d0424fa3355fcc32430803"
    )
    return client


def get_isochrone_data(client, lat, long, walking_time):
    # Set the location coordinate
    locations = [[lat, long]]

    # Set the walking time in seconds
    walking_time = [walking_time * 60]
    mobility_modal = "foot-walking"

    isochrone = openrouteservice.isochrones.isochrones(
        client,
        locations,
        profile=mobility_modal,
        range_type="time",
        range=walking_time,
        intervals=None,
        segments=None,
        interval=None,
        units=None,
        location_type=None,
        smoothing=None,
        attributes=["area", "total_pop"],
    )

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

    return isochrone
