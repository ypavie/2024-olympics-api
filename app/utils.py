from datetime import datetime
from typing import List, Dict, Optional, Tuple, Union
import requests
import json
import pycountry
from bs4 import BeautifulSoup
from pathlib import Path

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

MEDAL_DATA_URL = "https://olympics.com/OG2024/data/CIS_MedalNOCs~lang=ENG~comp=OG2024.json"
NOC_CODES_URL = "https://olympics.com/OG2024/data/MIS_NOCS~lang=ENG~comp=OG2024.json"
COUNTRY_CODE_URL = "https://en.wikipedia.org/wiki/Comparison_of_alphabetic_country_codes"
HEADERS = {'User-Agent': USER_AGENT}

def get_medal_summary(noc_codes: Optional[List[str]] = None) -> Dict[str, Union[str, int, List[Dict[str, Union[Dict[str, str], Dict[str, int]]]]]]:
    try:
        last_updated, medal_data, source_url = retrieve_medal_data()
    except Exception as e:
        return {}
    if noc_codes:
        filtered_medal_data = [filter_medals_by_noc(medal_data, noc_code) for noc_code in noc_codes]
        medal_data = [item for sublist in filtered_medal_data if sublist for item in sublist]

    medal_data = add_iso_codes(results=medal_data)

    return {
        "last_updated": last_updated,
        "source": source_url,
        "total_results": len(medal_data),
        "results": medal_data,
    }

def filter_medals_by_noc(data: List[Dict[str, any]], noc_code: str) -> List[Dict[str, any]]:
    filtered_data = [item for item in data if item["country"]["code"].lower() == noc_code.lower()]
    return filtered_data

def retrieve_medal_data() -> Tuple[str, List[Dict[str, any]], str]:
    response = requests.get(MEDAL_DATA_URL, headers=HEADERS)
    response.raise_for_status()
    medal_entries = response.json()["medalNOC"]
    noc_codes = get_noc_codes()

    aggregated_medals = aggregate_medal_counts(medal_entries)
    formatted_results = prepare_medal_results(aggregated_medals, noc_codes)
    sorted_results = sort_medal_results(formatted_results)

    return datetime.now().isoformat(), sorted_results, MEDAL_DATA_URL

def get_noc_codes() -> Dict[str, Dict[str, str]]:
    response = requests.get(NOC_CODES_URL, headers=HEADERS)
    nocs = {}
    for noc in response.json()["nocs"]:
        nocs[noc["code"]] = noc
    return nocs

def aggregate_medal_counts(entries: List[Dict[str, any]]) -> Dict[str, Dict[str, int]]:
    medal_counts = {}
    for entry in entries:
        if entry["gender"] == "TOT" and entry["sport"] == "GLO":
            noc_code = entry["org"]
            if noc_code not in medal_counts:
                medal_counts[noc_code] = {"gold": 0, "silver": 0, "bronze": 0, "rank": entry["rank"]}
            medal_counts[noc_code]["gold"] += entry["gold"]
            medal_counts[noc_code]["silver"] += entry["silver"]
            medal_counts[noc_code]["bronze"] += entry["bronze"]
    return medal_counts

def prepare_medal_results(medal_counts: Dict[str, Dict[str, int]], noc_codes: Dict[str, Dict[str, str]]) -> List[Dict[str, Union[Dict[str, str], Dict[str, int]]]]:
    return [
        {
            "country": {
                "code": noc_code,
                "name": noc_codes.get(noc_code, {}).get("name", "None"),
            },
            "medals": {
                "bronze": data["bronze"],
                "gold": data["gold"],
                "silver": data["silver"],
                "total": data["bronze"] + data["gold"] + data["silver"],
            },
            "rank": data["rank"],
        }
        for noc_code, data in medal_counts.items()
    ]

def sort_medal_results(results: List[Dict[str, Union[Dict[str, str], Dict[str, int]]]]) -> List[Dict[str, Union[Dict[str, str], Dict[str, int]]]]:
    results.sort(
        key=lambda x: (
            x["medals"]["gold"],
            x["medals"]["silver"],
            x["medals"]["bronze"],
            x["country"]["code"],
        ),
        reverse=True,
    )

    current_rank = 1
    for i, result in enumerate(results):
        if i > 0:
            previous_medals = results[i - 1]["medals"]
            current_medals = result["medals"]
            if current_medals == previous_medals:
                result["rank"] = results[i - 1]["rank"]
            else:
                result["rank"] = current_rank
        else:
            result["rank"] = current_rank
        current_rank += 1

    return sorted(results, key=lambda x: (x["rank"], x["country"]["code"]))

def get_country_codes() -> Tuple[List[Dict[str, str]], Dict[str, Dict[str, str]]]:
    response = requests.get(COUNTRY_CODE_URL, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    noc_table = soup.find("table", {"class": "wikitable"})

    def extract_code(cell: str) -> Optional[str]:
        if not cell.strip() or cell.startswith("[") or cell.startswith("]"):
            return None
        return cell.strip()

    codes = []
    for row in noc_table.find_all("tr")[1:]:
        columns = row.find_all("td")

        country_name = extract_code(columns[1].find("a").text)
        ioc_code = extract_code(columns[2].text)
        fifa_code = extract_code(columns[3].text)
        iso_alpha_3 = extract_code(columns[4].text.strip())

        iso_alpha_2 = None
        if iso_alpha_3:
            try:
                country = pycountry.countries.lookup(iso_alpha_3)
                iso_alpha_2 = country.alpha_2
            except LookupError:
                pass

        codes.append({
            "country_name": country_name,
            "ioc_noc_code": ioc_code,
            "fifa_code": fifa_code,
            "iso_alpha_3": iso_alpha_3,
            "iso_alpha_2": iso_alpha_2,
        })
    return codes

def load_country_codes() -> List[Dict[str, Optional[str]]]:
    file_path = Path(__file__).parent / 'data' / 'countries.json'
    with open(file_path) as f:
        return json.load(f)

def add_iso_codes(results: List[Dict[str, Union[Dict[str, str], Dict[str, int]]]]) -> List[Dict[str, Union[Dict[str, str], Dict[str, int]]]]:
    country_codes = load_country_codes()
    noc_to_country = {code["ioc_noc_code"]: code for code in country_codes}

    for result in results:
        country = result["country"]
        noc_code = country["code"]
        if noc_code in noc_to_country:
            country.update({
                "iso_alpha_3": noc_to_country[noc_code]["iso_alpha_3"],
                "iso_alpha_2": noc_to_country[noc_code]["iso_alpha_2"],
            })

    return results
