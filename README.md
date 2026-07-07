# OSARE — East Africa Safari Routes & Transit Hub

> Free information assistant & booking hub for **tourists** and **locals** across East Africa.
> A two-tier platform: **Safari / Tourism** and **Local Commute** — with photos, prices,
> off-peak deals, trusted vendor info, and one-tap **WhatsApp booking**.

Domain: **www.easafariroutes.com** · Repo: **JakasipulLab/eatransport-API**

---

## Business model

- The platform is **100% free for tourists / commuters**.
- **Vendors pay a 5% commission** on confirmed bookings — never the traveller.
  (The rate is a single constant `COMMISSION_RATE` in the API and can be changed anytime.)
- Bookings are captured as **WhatsApp leads** to `+254 758 378 729`, so every enquiry
  is tracked and shown in the **Revenue Dashboard**.

---

## Tech stack

| Layer      | Technology                                              |
|------------|---------------------------------------------------------|
| Framework  | **Next.js 15** (App Router) — frontend + API in one app |
| UI         | React 18, Tailwind CSS, shadcn/ui, lucide-react, Recharts |
| Database   | **PostgreSQL** via **NEON** (using the `pg` driver)     |
| Deployment | **Render.com** (Node web service, `output: standalone`) |

> The whole app (pages **and** backend API) runs as a single Next.js service.
> The original `server.py` (FastAPI) logic has been re-implemented as Next.js API routes.

---

## Project structure

```
/
├── app/
│   ├── page.js                 # OSARE UI: Home, Safari, Local, About, Dashboard, Vendor Portal, Admin
│   ├── layout.js               # Root layout + metadata
│   ├── globals.css             # Global styles / design tokens
│   └── api/[[...path]]/route.js # Backend API (listings, leads, stats, vendor auth, seed) on PostgreSQL
├── components/ui/              # shadcn/ui components
├── next.config.js              # standalone output for Render
├── render.yaml                 # Render Blueprint (NEON DATABASE_URL)
├── .env.example                # Environment variable template
└── package.json
```

Tables are auto-created on first request: `listings`, `leads`, `vendors`, `sessions`.

---

## API reference (all routes prefixed with `/api`)

| Method | Route                    | Description                                        |
|--------|--------------------------|----------------------------------------------------|
| GET    | `/api/listings`          | List/search. Query: `type`, `q`, `category`        |
| POST   | `/api/listings`          | Create a listing (attaches `ownerId` if logged in) |
| PUT    | `/api/listings/:id`      | Update a listing                                   |
| DELETE | `/api/listings/:id`      | Delete a listing                                   |
| POST   | `/api/leads`             | Create a booking lead → returns a `whatsappUrl`    |
| GET    | `/api/leads`             | List all booking leads                             |
| GET    | `/api/stats`             | Dashboard stats + estimated 5% commission revenue  |
| POST   | `/api/seed`              | Reset & load 15 sample listings                    |
| POST   | `/api/auth/register`     | Vendor sign-up → `{ token, vendor }`               |
| POST   | `/api/auth/login`        | Vendor login → `{ token, vendor }`                 |
| GET    | `/api/auth/me`           | Current vendor (Bearer token)                      |
| GET    | `/api/my-listings`       | Vendor's own listings (Bearer token)               |
| GET    | `/api/my-stats`          | Vendor's leads + commission owed (Bearer token)    |

Every record uses a **UUID `id`**. Vendor auth uses built-in `crypto` (scrypt) password
hashing + bearer session tokens — no external auth service required.

---

## Environment variables

See [`.env.example`](./.env.example). Required:

| Variable              | Purpose                                             |
|-----------------------|-----------------------------------------------------|
| `DATABASE_URL`        | NEON PostgreSQL connection string                   |
| `NEXT_PUBLIC_BASE_URL`| Public URL of the deployed app                      |
| `CORS_ORIGINS`        | Allowed origins (`*` for open access)               |

> The app automatically strips `&channel_binding=require` from `DATABASE_URL`
> because the Node `pg` driver does not support SCRAM channel binding. SSL is
> enabled automatically.

---

## Run locally

```bash
yarn install
cp .env.example .env      # then paste your NEON DATABASE_URL
yarn dev                  # http://localhost:3000
```

On first load the app auto-seeds sample data. You can also POST `/api/seed`
or click **"Reset & load sample data"** on the Admin page.

---

## Deploy to Render.com with NEON

### Step 1 — NEON database
1. Create a project at <https://neon.tech> (free).
2. Copy the **connection string** from **Connection Details**
   (`postgresql://...neon.tech/...?sslmode=require`).

### Step 2 — Deploy the web service
1. Push this repo to `JakasipulLab/eatransport-API`.
2. In Render: **New + → Blueprint** (uses `render.yaml`) or a **Web Service**:
   - **Build:** `yarn install && yarn build`
   - **Start:** `yarn start`
   - **Environment:** Node 20
3. Environment variables:
   - `DATABASE_URL` = your NEON connection string
   - `NEXT_PUBLIC_BASE_URL` = your Render / `easafariroutes.com` URL
   - `CORS_ORIGINS` = `*`
4. Deploy. Tables auto-create on first request; POST `/api/seed` once to load samples.

### Step 3 — Custom domain
In Render → **Custom Domains**, add `easafariroutes.com` and follow the DNS steps.

---

## Changing the commission rate

Open `app/api/[[...path]]/route.js` and edit:
```js
const COMMISSION_RATE = 0.05 // 5% — change to 0.10 for 10%, 0 for free, etc.
```

---

## License

© 2026 OSARE — easafariroutes.com. All rights reserved.
