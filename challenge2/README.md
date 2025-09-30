# Image Processing API

## Quick Start

## Environment Configuration

Create a `.env` file in the project root:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=image_processing
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/image_processing

# API
API_PORT=8000
DEBUG=true
```

### 1. Start with Docker

```bash
docker-compose up -d
```

Wait 10-15 seconds for PostgreSQL to initialize and migrations to run automatically.

### 2. Load and Process Data

```bash
curl -X POST http://localhost:8000/api/v1/resize \
  -H "Content-Type: application/json" \
  -d '{"target_width": 150}'
```

This returns an `image_id` that you'll use in subsequent requests:

```json
{
  "message": "Successfully processed and resized 500 frames",
  "image_id": 1,
  "frames_processed": 500,
  "target_width": 150
}
```

### 3. Query Image Frames

#### Interactive API Documentation

Visit http://localhost:8000/docs for Swagger UI with interactive API documentation.

#### Get Image Frames (Required: image_id)

```bash
curl "http://localhost:8000/api/v1/frames?image_id=1&page=1&per_page=10"
```

#### Get Frames by Depth Range

```bash
curl "http://localhost:8000/api/v1/frames?image_id=1&depth_min=1.0&depth_max=5.0&per_page=5"
```

#### Get Colormap Data Only

```bash
curl "http://localhost:8000/api/v1/frames?image_id=1&coloredmap=true&per_page=5"
```

#### Get Grayscale Data Only

```bash
curl "http://localhost:8000/api/v1/frames?image_id=1&coloredmap=false&per_page=5"
```

### 4. Apply Colormap

```bash
curl -X POST http://localhost:8000/api/v1/colormap/apply \
  -H "Content-Type: application/json" \
  -d '{"image_id": 1, "colormap": "viridis", "batch_size": 100}'
```

## API Endpoints

| Method | Endpoint                 | Description                          | Required Parameters | Optional Parameters                                        |
| ------ | ------------------------ | ------------------------------------ | ------------------- | ---------------------------------------------------------- |
| POST   | `/api/v1/resize`         | Load CSV data, resize and save to DB | -                   | `target_width` (default: 150)                              |
| GET    | `/api/v1/frames`         | Get image frames with pagination     | `image_id`          | `depth_min`, `depth_max`, `page`, `per_page`, `coloredmap` |
| POST   | `/api/v1/colormap/apply` | Apply colormap to frames in batch    | `image_id`          | `colormap` (default: viridis), `batch_size` (default: 100) |

## Example Responses

### Load Data Response

```json
{
  "message": "Successfully processed and resized 500 frames",
  "image_id": 1,
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
      "image_id": 1,
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
      "image_id": 1,
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

### Apply Colormap Response

```json
{
  "message": "Successfully applied 'viridis' colormap",
  "image_id": 1,
  "processed": 500,
  "total": 500,
  "colormap_applied": "viridis"
}
```

### Available Colormaps

The API supports 19 matplotlib colormaps:

- **Perceptually Uniform**: `viridis`, `plasma`, `inferno`, `magma`, `cividis`
- **Sequential**: `hot`, `cool`, `bone`, `copper`, `gray`
- **Diverging**: `turbo`, `jet`, `rainbow`
- **Cyclic**: `spring`, `summer`, `autumn`, `winter`
- **Specialized**: `ocean`, `terrain`

## Architecture

### Technology Stack

- **Framework**: FastAPI 0.104.1 with Uvicorn ASGI server
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0.23 ORM
- **Image Processing**: OpenCV 4.8.1 for resizing, Matplotlib 3.8.2 for colormaps
- **Data Processing**: Pandas 2.1.3 for CSV parsing, NumPy 1.26.2 for numerical operations
- **Migrations**: Alembic 1.12.1 for database version control
- **Containerization**: Docker & Docker Compose

### Database Schema

#### `images` Table

- `id`: Primary key (auto-increment)
- `target_width`: Width of resized pixel arrays
- `total_frames`: Count of frames in this image
- `csv_source`: Source CSV file path
- `created_at`: Timestamp of image creation

#### `image_frames` Table

- `id`: Primary key (auto-increment)
- `image_id`: Foreign key to images table (CASCADE delete)
- `depth`: Depth value for this frame
- `pixels`: JSON array of resized grayscale pixel values (target_width length)
- `color_map_pixels`: JSON array of RGB triplets after colormap application
- `colormap_name`: Name of applied colormap (e.g., "viridis")
- `created_at`: Timestamp of frame creation
- `colormap_applied_at`: Timestamp of colormap application

**Indexes**:

- `idx_image_depth`: Composite index on (image_id, depth) for depth-range queries
- `idx_colormap_status`: Composite index on (image_id, colormap_name) for colormap filtering

## Stop Services

```bash
docker-compose down
```

To remove volumes and reset database:

```bash
docker-compose down -v
```
