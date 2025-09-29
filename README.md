# AIQ Assessment

## Challenges

### Challenge 1: Power Plants API
A REST API service for managing and analyzing power plant data from the EPA's eGRID database.

**Location:** `./challenge1`

**Features:**
- Excel data import from eGRID2021 dataset
- MongoDB data persistence with upsert operations
- RESTful API endpoints for querying power plants
- Percentage calculation of plant generation contribution
- State-based filtering
- Winston logger integration for centralized logging

**Tech Stack:**
- Node.js with TypeScript
- Express.js
- MongoDB with Mongoose ODM
- Docker Compose for containerization
- Winston for logging

For detailed setup and usage instructions, see [challenge1/README.md](./challenge1/README.md)

### Challenge 2: Image Processing API
A REST API service for processing and serving image data with depth-based queries and colormap visualization.

**Location:** `./challenge2`

**Features:**
- CSV data import with image resizing capabilities
- PostgreSQL data persistence with Alembic migrations
- RESTful API endpoints for querying image frames
- Depth-based filtering with pagination
- Batch colormap processing with status tracking
- Multiple colormap support (viridis, plasma, jet, etc.)

**Tech Stack:**
- Python with FastAPI
- PostgreSQL with SQLAlchemy ORM
- Alembic for database migrations
- OpenCV for image processing
- Matplotlib for colormap application
- Docker Compose for containerization

For detailed setup and usage instructions, see [challenge2/README.md](./challenge2/README.md)