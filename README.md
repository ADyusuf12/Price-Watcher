📦 PriceWatcher
PriceWatcher is a full‑stack monorepo project that scrapes product data from Nigerian e‑commerce platforms (Jumia, Konga), stores it in PostgreSQL, exposes it via a Rails API, and provides a React + Vite frontend with a glassmorphic UI for product browsing and side‑by‑side price comparisons.

🚀 Features
Scrapers & Pipelines

Jumia and Konga scrapers with resilient pipelines.

Normalized price parsing, discount calculation, and checkpointing.

Inserts into PostgreSQL with source and image fields.

Database

PostgreSQL schema with products table.

Unique index on product URLs to prevent duplicates.

UTC timestamps with defaults.

Rails API

Versioned endpoints under /api/v1/.

ProductsController for listing and detail.

ComparisonsController for side‑by‑side price differences.

Query objects for cleaner logic.

Frontend (React + Vite)

Nigerian green‑and‑white glassmorphism theme.

ProductCard component with hover scrolling titles, source badges, and currency formatting.

ComparisonPage with search, grouped comparisons, pagination, and loading states.

TailwindCSS setup with text shadow utilities.

Docker & Infra

docker-compose.yml orchestrates API, DB, and frontend.

Rails dev Dockerfile + entrypoint script.

Scraper Dockerfile for containerized scraping.

.dockerignore and .gitignore to keep repo clean.

🗂 Monorepo Structure
Code
pricewatcher/
├── docker-compose.yml
├── frontend/              # React + Vite app
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   ├── package.json
│   └── tailwind.config.js
├── pricewatcher_api/      # Rails API
│   ├── app/
│   │   ├── controllers/api/v1/
│   │   └── queries/
│   ├── db/
│   │   ├── migrate/
│   │   └── schema.rb
│   ├── Dockerfile.dev
│   └── entrypoint.sh
├── scrapers/              # Python scrapers
│   ├── jumia_pipeline.py
│   └── konga_pipeline.py
├── Dockerfile.scraper
└── requirements.txt
⚙️ Setup Checklist
Clone the repo

bash
git clone https://github.com/yourusername/pricewatcher.git
cd pricewatcher
Backend (Rails API)

Ensure PostgreSQL is running.

Copy .env with DB credentials into pricewatcher_api/.

Run migrations:

bash
cd pricewatcher_api
bin/rails db:migrate
Frontend

bash
cd frontend
npm install
npm run dev
Scrapers

Activate Python venv.

Install requirements:

bash
pip install -r requirements.txt
Run scrapers to populate DB.

Docker (optional)

bash
docker-compose up
🧪 Verification
API: http://localhost:3000/api/v1/products

Frontend: http://localhost:5173

Comparisons: http://localhost:5173/compare

📌 Git Workflow
Default branch: main

Development branch: dev

Feature branches for scoped work:

feature/jumia-scrapers-initial-setup

feature/comparisons-endpoint

feature/tailwind-setup

feature/full-stack-enhancements

🔮 Next Steps
Improve comparison matching logic (brand, model, RAM, storage).

Expand scraping to more categories.

Enhance frontend navigation and styling.

Continuous integration with tests for scrapers and API.
