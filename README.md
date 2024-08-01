# Olympics 2024 Medals API

# Overview

This API provides data on Olympic medals for the 2024 Paris Olympics. It allows you to retrieve medal summaries for specific countries. Please note that this API is not official and uses data from publicly available sources.

# Endpoints

# Medals Endpoint

- **URL:** `/medals`
- **Method:** `GET`
- **Query Parameters:**
  - `country` (Optional): A comma-separated list of country codes (e.g., `USA,GBR`).
- **Response:** JSON

**Description:** 
Retrieves a summary of Olympic medals for the specified countries.

**Example Request:**

```
GET /medals?country=fra,usa
```

**Example Response:**

```
{
  "last_updated": "2024-08-01T11:34:23.122426",
  "source": "https://olympics.com/OG2024/data/CIS_MedalNOCs~lang=ENG~comp=OG2024.json",
  "total_results": 2,
  "results": [
    {
      "country": {
        "code": "FRA",
        "name": "France",
        "iso_alpha_3": "FRA",
        "iso_alpha_2": "FR"
      },
      "medals": {
        "bronze": 8,
        "gold": 8,
        "silver": 10,
        "total": 26
      },
      "rank": 2
    },
    {
      "country": {
        "code": "USA",
        "name": "United States",
        "iso_alpha_3": "USA",
        "iso_alpha_2": "US"
      },
      "medals": {
        "bronze": 12,
        "gold": 6,
        "silver": 13,
        "total": 31
      },
      "rank": 5
    }
  ]
}
```

# Data Sources

- **Medal Data:** [Olympics Medal Data](https://olympics.com/OG2024/data/CIS_MedalNOCs~lang=ENG~comp=OG2024.json)
- **NOC Codes:** [NOC Codes](https://olympics.com/OG2024/data/MIS_NOCS~lang=ENG~comp=OG2024.json)

# Running the API

To run this API locally:

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Run the FastAPI application:
   ```
   uvicorn main:app --reload
   ```

   Replace `main` with the name of your Python file if it's different.

# Live API

The API is live and available at: [2024-olympics-api-vercel.vercel.app](https://2024-olympics-api-vercel.vercel.app)

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
