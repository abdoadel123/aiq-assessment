# Power Plants API

## Quick Start

### 1. Install Dependencies
```bash
npm install
```

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

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| POST | `/api/v1/plants/update` | Import Excel data to MongoDB | `excelPath`, `sheetName` |
| GET | `/api/v1/plants` | Get top N plants with percentage | `limit` (1-100), `state` (optional) |

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