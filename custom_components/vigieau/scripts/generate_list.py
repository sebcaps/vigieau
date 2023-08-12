import aiohttp
import asyncio
import json
import sys
from pathlib import Path
from os import path


current_dir = path.dirname(__file__)
parent_dir = path.dirname(current_dir)
sys.path.append(".")
sys.path.append(parent_dir)
from custom_components.vigieau.const import GEOAPI_GOUV_URL, BASE_URL


async def get_insee_list():
    session = aiohttp.ClientSession()
    resp = await session.get(GEOAPI_GOUV_URL)

    if resp.status != 200:
        print(f"Error Calling GEOAPI with code {resp.status}")
        return {}

    return await resp.json()


async def get_restriction(city_code: str):
    url = f"{BASE_URL}/reglementation?&commune={city_code}&profil=particulier"
    session = aiohttp.ClientSession()
    resp = await session.get(url)

    if resp.status != 200:
        return {}

    return await resp.json()


async def main():
    restriction_list = {"restrictions": []}
    usage_added = []
    commune_list = await get_insee_list()
    for commune in commune_list:
        # if len(restriction_list["restrictions"]) >= 10:
        #     break
        restriction = await get_restriction(commune["code"])
        if (
            restriction
        ):  # Sometimes insee is enouhg to call vigieau Api, sometimes not exclude the one where it's not enough , for the moment
            for usage in restriction.get("usages"):
                if usage["usage"] not in usage_added:
                    restriction_list["restrictions"].append(
                        {"thematique": usage["thematique"], "usage": usage["usage"]}
                    )
                    usage_added.append(usage["usage"])

    finaldata = json.dumps(
        restriction_list, ensure_ascii=False
    )  # https://stackoverflow.com/questions/35582528/python-encoding-and-json-dumps
    file = Path(f"{current_dir}/full_usage_list.json")

    with open(file, "w", encoding="utf-8") as outfile:
        outfile.write(finaldata)


if __name__ == "__main__":
    asyncio.run(main())
