from homeassistant.components.sensor import (
    SensorEntityDescription,
)
from dataclasses import dataclass

DOMAIN = "vigieau"

BASE_URL = "https://api.vigieau.beta.gouv.fr"
GEOAPI_GOUV_URL = "https://geo.api.gouv.fr/communes?"
ADDRESS_API_URL = "https://api-adresse.data.gouv.fr"
CONF_LOCATION_MODE = "location_mode"
HA_COORD = 0
ZIP_CODE = 1
SELECT_COORD = 2
LOCATION_MODES = {
    HA_COORD: "Coordonnées Home Assistant",
    ZIP_CODE: "Code Postal",
    SELECT_COORD: "Sélection sur carte",
}
CONF_INSEE_CODE = "INSEE"
CONF_CITY = "city"
CONF_CODE_POSTAL = "Code postal"
CONF_LOCATION_MAP = "location_map"
NAME = "Vigieau"
DEVICE_ID_KEY = "device_id"


@dataclass
class VigieEauRequiredKeysMixin:
    """Mixin for required keys."""

    category: str
    matchers: list[str]


@dataclass
class VigieEauSensorEntityDescription(
    SensorEntityDescription, VigieEauRequiredKeysMixin
):
    """Describes VigieEau sensor entity."""


SENSOR_DEFINITIONS: tuple[VigieEauSensorEntityDescription, ...] = (
    VigieEauSensorEntityDescription(
        name="Alimentation des fontaines",
        icon="mdi:fountain",
        category="fountains",
        key="fountains",
        matchers=[
            "alimentation.+fontaines.+",
            "douches (des|de) plages.+",
            "fontaines.+potable.+",
            "fonctionnement.+fontaines.+",
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Arrosage des jardins potagers",
        icon="mdi:watering-can",
        category="potagers",
        key="potagers",
        matchers=[
            "Arrosage des (jardins)+.+(potager(s)*)",
            "Arrosage des potagers",
            "arrosage.+(^plant(s)*$|arbres|suspension|jeunes plants|^jardin(s)*$|espaces arborés)",
            "Dispositifs de récupération des eaux de pluie",
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Arrosage voirie et trottoirs",
        icon="mdi:road",
        category="roads",
        key="roads",
        matchers=[
            "voiries|voieries|voies publique|voirie",
            "arrosage.+poussière.+",
            "arrosage.+manifestation.+",
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Arrosage des pelouses",
        icon="mdi:sprinkler-variant",
        category="lawn",
        key="lawn",
        matchers=[
            "surface.+sportives.+",
            "arrosage.+(massif|haies|espaces verts|pelouse|jardins d'agrément|plantation).*",
            #"arrosage.+(massif|jardin|haies|espaces verts|pelouse|jardins d'agrément).*",
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Lavage des véhicules",
        icon="mdi:car-wash",
        category="car_wash",
        key="car_wash",
        matchers=[
            "lavage.+(véhicule|véhicules)*.+(particuliers|professionnel)*.+"
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Lavage des engins nautiques",
        icon="mdi:sail-boat",
        category="nautical_vehicules",
        key="nautical_vehicules",
        matchers=[
            "lavage.+engins nautiques.+professionnels",
            "Nettoyage.+(embarcation|bateaux)",
            "lavage.+bateau.+",
            "véhicules, engins nautiques",
            "Lavage d’engins nautiques",
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Lavage des toitures façades",
        icon="mdi:home-roof",
        category="roof_clean",
        key="roof_clean",
        matchers=[
            "(nettoyage|lavage).+(toitures|façade|terrasse)",
            # "façades",
            "nettoyage.+bâtiments.+",
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Vidange et remplissage des piscines",
        icon="mdi:pool",
        category="pool",
        key="pool",
        matchers=[
            "(remplissage|vidange)*(piscines|piscine).+(familial|privé|privées|collective)*",
            # "piscines non collectives",  # Remplissage et vidange de piscines non collectives (de plus de 1 m3)
            "baignades.+",
            "(structure|structures) gonflables",
            "^(fontaine).+jeux d'eau", #to avoid duplicate with fontaine, however this is a hack, should use (?!fontaine)
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Remplissage/Vidange des plans d'eau",
        icon="mdi:waves",
        category="ponds",
        key="ponds",
        matchers=[
            "^(remplissage|vidange|alimentation)((?!fontaine).)*(plan.*d.eau|bassin)*$",
            "lestage",
            # "Remplissage tonne de chasse",
            "(manoeuvre|manœuvre).+vannes.+barrages",  # Manoeuvre de vannes des seuils et barrages
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Travaux sur cours d'eau",
        icon="mdi:hydro-power",
        category="river_rate",
        key="river_rate",
        matchers=[
            # "ouvrage.+cours d.eau",
            "(manoeuvre|manœuvre).+vannes.+(moulin|réseau)*",  # Manoeuvre de vannes des seuils et barrages
            "Gestion des ouvrages",  # FIXME: we should probably match with the category as well
            "travaux.+(rivière|cours d.eau)",
            "rabattement.+nappe.+",
            "faucardage.+",
            "faucardement",
            "manoeuvre.+d.ouvrage.+",
            "orpaillage",
            "seuil.+provisoire",
            "perturbations physique.+cours d.eau",
            "pratiques.+lit.+impact.+",
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Navigation fluviale",
        icon="mdi:ferry",
        category="river_movement",
        key="river_movement",
        matchers=["Navigation fluviale", "canyoning"],
    ),
    VigieEauSensorEntityDescription(
        name="Arrosage des golfs",
        icon="mdi:golf",
        category="golfs",
        key="golfs",
        matchers=["arrosage des golfs"],
    ),
    VigieEauSensorEntityDescription(
        name="Prélèvement en canaux",
        icon="mdi:water-pump",
        category="canals",
        key="canals",
        matchers=[
            "Prélèvement en canaux",
            "Prélèvements dans le milieu naturel.+",
            "(prélèvements|prélèvement).+cours d.eau.+",
            "prélèvements.+fonctionnement.+",
            "prélèvement.+hydraulique.+",
            "alimentation.+canaux.+",
            "Activités cynégétiques",
            # "Prélèvement d’eau superficielle",
            "Prélèvements énergétiques",
            "Création de prélèvements",
            "mares de gabion" #Prélèvements pour l’alimentation de plans d’eau dont les mares de gabion
        ],
    ),
    VigieEauSensorEntityDescription(
        name="Abreuvement des animaux",
        icon="mdi:cow",
        category="animaux",
        key="animaux",
        matchers=["abreuvement"],
    ),
)
