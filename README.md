# HRMS Lite

HRMS Lite is a full-stack Human Resource Management System for managing employees and attendance with a clean API contract, validation-first backend, and production-ready frontend UX.

## Features

- Employee management
  - Create employee with strict validation
  - Unique constraints on `employeeId` and `email`
  - List employees with pagination metadata
  - Delete employee (with cascading attendance cleanup)
- Attendance management
  - Mark attendance by `date` and `status` (`Present`/`Absent`)
  - Optional `punchInTime` and `punchOutTime`
  - Duplicate prevention: one attendance record per employee per day
  - View full attendance history by employee
  - Monthly attendance view with auto-filled absent days
- Monthly reporting
  - Separate monthly attendance page in frontend
  - CSV export for monthly data (Excel-compatible)
- Reliability
  - Standardized success/error response schema
  - Global exception handling with machine-readable error codes
  - Request ID metadata for traceability
  - Automated API tests with `pytest` + `mongomock`

## Tech Stack

- Frontend: React 19, Vite, React Router, Axios
- Backend: FastAPI, Pydantic v2, PyMongo
- Database: MongoDB (local or Atlas)
- Testing: Pytest, FastAPI TestClient, Mongomock

## Architecture

Backend uses layered design:

`api -> services -> repositories -> database`

Important backend modules:

- `backend/app/api/` - HTTP routes
- `backend/app/services/` - business logic and validations
- `backend/app/repositories/` - Mongo data access
- `backend/app/database/connection.py` - connection and indexes
- `backend/app/middleware/` - request ID and error handling

## API Endpoints

Health:

- `GET /health`

Employees:

- `POST /employees`
- `GET /employees?page=1&limit=20`
- `DELETE /employees/{employee_id}`

Attendance:

- `POST /attendance`
- `GET /attendance/{employee_id}`
- `GET /attendance/monthly/{employee_id}?year=2026&month=2`

## Response Contract

Success:

```json
{
  "success": true,
  "message": "Employee created successfully",
  "data": {},
  "meta": {
    "requestId": "..."
  }
}
```

Error:

```json
{
  "success": false,
  "message": "Validation failed",
  "error": {
    "code": "VALIDATION_ERROR",
    "details": {
      "errors": []
    }
  },
  "meta": {
    "requestId": "..."
  }
}
```

Common error codes:

- `VALIDATION_ERROR`
- `NOT_FOUND`
- `DUPLICATE_EMPLOYEE`
- `DUPLICATE_ATTENDANCE`
- `DATABASE_ERROR`
- `SERVER_ERROR`

## Project Structure

```text
backend/
  app/
  tests/
  requirements.txt
frontend/
  src/
  package.json
README.md
```

## Local Development Setup

### 1. Backend Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Backend default URL: `http://127.0.0.1:8000`

Required backend `.env` values:

- `DATABASE_URL` (example: `mongodb://localhost:27017` or Atlas URI)
- `DATABASE_NAME` (example: `hrms_lite`)
- `CORS_ORIGINS` (comma-separated frontend origins)

### 2. Frontend Setup

```bash
cd frontend
npm install
copy .env.example .env
npm run dev
```

Frontend default URL: `http://127.0.0.1:5173`

Required frontend `.env` value:

- `VITE_API_BASE_URL=http://127.0.0.1:8000`

## Testing

Run backend tests:

```bash
cd backend
pytest -q
```

Current tests cover:

- Employee CRUD and duplicate checks
- Attendance mark/read/monthly behavior
- Punch time validation rules
- Validation and error contract
- Health endpoint contract

## Deployment Guide

Recommended production split:

- Frontend: Netlify or Vercel
- Backend API: Vercel (Python Serverless)
- Database: MongoDB Atlas

### Backend deployment (Vercel)

1. Import GitHub repo into Vercel.
2. Set Root Directory to `backend`.
3. Set Build Command: `pip install -r requirements.txt`
4. Set Output Directory: leave default for Python runtime.
5. Add environment variables:
   - `DATABASE_URL`
   - `DATABASE_NAME`
   - `CORS_ORIGINS` (include deployed frontend URL)
   - `APP_NAME`
   - `APP_VERSION`
   - `DEBUG=false`
6. Deploy and verify:
   - `https://<backend-domain>/health`

### Frontend deployment (Netlify)

1. Import GitHub repo into Netlify.
2. Set Base directory: `frontend`
3. Build command: `npm run build`
4. Publish directory: `dist`
5. Add environment variable:
   - `VITE_API_BASE_URL=https://<your-backend-domain>`
6. Deploy.
7. For SPA routing, add `frontend/public/_redirects` with:

```text
/* /index.html 200
```

### Frontend deployment (Vercel alternative)

1. Import GitHub repo into Vercel.
2. Set Root Directory to `frontend`.
3. Build Command: `npm run build`
4. Output Directory: `dist`
5. Add `VITE_API_BASE_URL=https://<your-backend-domain>`
6. Deploy.

## GitHub Actions CI/CD (Auto Vercel Deploy)

This repo now includes `.github/workflows/vercel-cicd.yml`.

Behavior:

- On every push to `main`, it runs backend tests and frontend build checks.
- If checks pass, it deploys backend and frontend to Vercel production.
- You can also run it manually from GitHub Actions (`workflow_dispatch`).

Required GitHub repository secrets:

- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_BACKEND_PROJECT_ID`
- `VERCEL_FRONTEND_PROJECT_ID`

How to get IDs:

1. Run `vercel login`.
2. Run `vercel link` inside `backend`.
3. Run `vercel link` inside `frontend`.
4. Open generated `.vercel/project.json` in each folder and copy:
   - `orgId` -> `VERCEL_ORG_ID` (same org for both)
   - `projectId` -> backend/frontend project secrets

Also make sure Vercel project env vars are set in Vercel dashboard:

- Backend: `DATABASE_URL`, `DATABASE_NAME`, `CORS_ORIGINS`, `APP_NAME`, `APP_VERSION`, `DEBUG`
- Frontend: `VITE_API_BASE_URL` (pointing to deployed backend URL)

## Security Notes

- Never commit real credentials in `.env`.
- Use unique restricted MongoDB users for production.
- Keep `CORS_ORIGINS` explicit to deployed frontend domains.

## Confidential File Policy

`implemantationPlan.text` is treated as confidential and should remain local only (not pushed to GitHub).
