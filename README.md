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