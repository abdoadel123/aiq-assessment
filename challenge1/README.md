# Power Plants API

## Quick Start

## Environment Configuration

Create a `.env` file in the project root:

```env
# MongoDB Configuration
MONGO_USERNAME=admin
MONGO_PASSWORD=password123
MONGO_DB_NAME=powerplants
MONGO_HOST=localhost
MONGO_PORT=27017

# Application Configuration
PORT=3000
```

### 1. Download Data

Download the Data File (Excel format) from the EPA website:

Visit https://www.epa.gov/egrid/download-data and download eGRID2021 or recent data sheet (xlsx)

Place the downloaded file in the challenge1 directory

### 2. Start with Docker

```bash
docker-compose up -d
```

Wait 5-10 seconds for MongoDB to initialize.

### 3. Import Data

```bash
curl -X POST http://localhost:3000/api/v1/plants/update \
  -H "Content-Type: application/json" \
  -d '{"excelPath": "./eGRID2021_data.xlsx", "sheetName": "PLNT21"}'
```

### 4. Test API

#### Get Top 10 Plants

```bash
curl http://localhost:3000/api/v1/plants?limit=10
```

#### Get Top 5 Plants in California

```bash
curl http://localhost:3000/api/v1/plants?limit=5&state=CA
```

## API Endpoints

| Method | Endpoint                | Description                      | Parameters                          |
| ------ | ----------------------- | -------------------------------- | ----------------------------------- |
| POST   | `/api/v1/plants/update` | Import Excel data to MongoDB     | `excelPath`, `sheetName`            |
| GET    | `/api/v1/plants`        | Get top N plants with percentage | `limit` (1-100), `state` (optional) |

## Example Responses

### Import Data Response

```json
{
  "success": true,
  "message": "Data updated successfully"
}
```

### Get Plants Response

```json
{
  "success": true,
  "data": [
    {
      "id": 55147,
      "name": "Palo Verde",
      "state": "AZ",
      "annualNetGeneration": 31920658.6,
      "percentage": 0.78
    }
  ]
}
```

## Stop Services

```bash
docker-compose down
```
