# Image Processing API

## Quick Start

### 1. Start with Docker

```bash
docker-compose up -d
```

Wait 10-15 seconds for PostgreSQL to initialize and migrations to run automatically.

### 2. Load and Process Data

```bash
curl -X POST http://localhost:8000/api/v1/resize \
  -H "Content-Type: application/json" \
  -d '{"csv_path": "/app/data.csv", "target_width": 150}'
```

### 3. Test API

#### Interactive API Documentation

Visit http://localhost:8000/docs for Swagger UI with interactive API documentation.

#### Get Image Frames

```bash
curl "http://localhost:8000/api/v1/frames?page=1&per_page=10"
```

#### Get Frames by Depth Range

```bash
curl "http://localhost:8000/api/v1/frames?depth_min=1.0&depth_max=5.0&per_page=5"
```

#### Get Colormap Data Only

```bash
curl "http://localhost:8000/api/v1/frames?coloredmap=true&per_page=5"
```

#### Get Grayscale Data Only

```bash
curl "http://localhost:8000/api/v1/frames?coloredmap=false&per_page=5"
```

#### Apply Colormap

```bash
curl -X POST http://localhost:8000/api/v1/colormap/apply \
  -H "Content-Type: application/json" \
  -d '{"colormap": "viridis", "batch_size": 100}'
```

#### Check Colormap Status

```bash
curl http://localhost:8000/api/v1/colormap/status
```

#### Get Available Colormaps

```bash
curl http://localhost:8000/api/v1/colormaps
```

## API Endpoints

| Method | Endpoint                    | Description                              | Parameters                                    |
| ------ | --------------------------- | ---------------------------------------- | --------------------------------------------- |
| POST   | `/api/v1/resize`            | Load CSV data, resize and save to DB    | `csv_path`, `target_width`                    |
| GET    | `/api/v1/frames`            | Get image frames with pagination         | `depth_min`, `depth_max`, `page`, `per_page`, `coloredmap` |
| POST   | `/api/v1/colormap/apply`    | Apply colormap to all frames (batch)    | `colormap`, `batch_size`                      |
| GET    | `/api/v1/colormap/status`   | Get colormap processing status           | -                                             |
| GET    | `/api/v1/colormaps`         | Get list of available colormaps          | -                                             |

## Example Responses

### Load Data Response

```json
{
  "message": "Successfully processed and resized 500 frames",
  "frames_processed": 500,
  "target_width": 150
}
```

### Get Frames Response

#### With coloredmap=true (returns colormap data, pixels array is empty)

```json
{
  "frames": [
    {
      "id": 1,
      "depth": 1.5,
      "pixels": [],
      "color_map_pixels": [[255, 0, 0], [0, 255, 0], ...],
      "colormap_name": "viridis",
      "created_at": "2025-09-29T20:00:00Z",
      "colormap_applied_at": "2025-09-29T20:30:00Z"
    }
  ],
  "count": 10,
  "total": 500,
  "page": 1,
  "per_page": 10,
  "total_pages": 50
}
```

#### With coloredmap=false (returns grayscale data, color_map_pixels array is empty)

```json
{
  "frames": [
    {
      "id": 1,
      "depth": 1.5,
      "pixels": [120, 135, 142, ...],
      "color_map_pixels": [],
      "colormap_name": "viridis",
      "created_at": "2025-09-29T20:00:00Z",
      "colormap_applied_at": "2025-09-29T20:30:00Z"
    }
  ],
  "count": 10,
  "total": 500,
  "page": 1,
  "per_page": 10,
  "total_pages": 50
}
```

### Colormap Status Response

```json
{
  "processed": 250,
  "total": 500,
  "status": "processing",
  "current_batch": 3,
  "total_batches": 5
}
```

### Available Colormaps Response

```json
{
  "colormaps": [
    "viridis", "plasma", "inferno", "magma",
    "jet", "hot", "cool", "spring", "summer",
    "autumn", "winter", "gray", "bone"
  ]
}
```

## Architecture

### Database Schema

- **image_frames**: Stores processed image data
  - `id`: Primary key
  - `depth`: Unique depth value with index
  - `pixels`: JSON array of resized pixel values (150 values)
  - `color_map_pixels`: JSON array of RGB values after colormap application
  - `colormap_name`: Name of applied colormap
  - `created_at`: Timestamp of frame creation
  - `colormap_applied_at`: Timestamp of colormap application

### Services

- **DataLoader**: Handles CSV import and pixel resizing
- **ImageProcessor**: Resizes pixel arrays using OpenCV
- **ColorMapProcessor**: Batch processes colormap application
- **ColormapHandler**: Applies matplotlib colormaps to grayscale data

## Stop Services

```bash
docker-compose down
```