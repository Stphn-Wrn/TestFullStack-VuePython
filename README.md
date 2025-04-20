# Full Stack Project Setup Guide (Vue 3 + Python)

I'm aware that some things haven't been implemented in full, or perhaps only in part, or that others need to be improved. 

I was able to discover Vue3 and its API composition, which I'd never used before, or JWT directly via cookies with interceptors. It was all very interesting. 
As for Python, I'd already used it for a few scripts in my personal projects, but never really for the web. It was fun to use and I enjoyed it. 

As for the tests, I didn't have the time to do them all for all the features, but if I'd had the time, I'd have set up a complete e2e, I think. It's a test I didn't know about and the principle is great.

## 1. Environment Configuration

Create the environment files:

- At the project root: `.env`
- Inside `backend/environment`: `.compose.env`

Copy them from the corresponding `.dev` files and update the values marked as `to_change`.

---

## 2. Backend Setup

Navigate to the `backend` folder and run:

```bash
pip install -U pip setuptools
pip install poetry
poetry install  # Run this only if poetry is already installed
```

---

## 3. Start the Project with Docker

From the project root, build and run the Docker containers:

```bash
docker compose --env-file ./backend/environment/.compose.env up --build -d
```

### Optional: Use the Shell Script

```bash
chmod +x start_dev.sh
sh start_dev.sh
```
Note: This docker configuration is stuffed with a Hot Reload Module system, you shouldn't need to relaunch at each change.

---

## 4. Apply Database Migrations

After building the containers, run migrations from the `backend` directory:

```bash
poetry run alembic upgrade head
```

To generate a new migration after modifying a model:

```bash
poetry run alembic revision --autogenerate -m "brief description of the migration"
```

---

## 5. Start the Frontend

From the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: [http://localhost:3000/](http://localhost:3000/)

---

## 6. Testing

### Backend Unit Tests

```bash
cd backend
poetry run pytest tests/unit
```

### Frontend E2E Tests with Cypress

**Headless mode:**

```bash
cd frontend
npx cypress run --spec "frontend/cypress/e2e/file_to_test.cy.js"
```

**GUI mode (Electron):**

```bash
cd frontend
npx cypress open
# Then go to: E2E Testing → Start E2E Testing in Electron → Select your test script
```

---

## 7. Linting (Frontend)

Run ESLint to automatically fix issues:

```bash
cd frontend
eslint --fix ./src
```
