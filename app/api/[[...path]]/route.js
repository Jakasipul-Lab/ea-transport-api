import { v4 as uuidv4 } from 'uuid'
import { NextResponse } from 'next/server'
import crypto from 'crypto'
import pg from 'pg'

const { Pool } = pg

// ---------------------------------------------------------------------------
// PostgreSQL (NEON) connection (singleton) + schema init
// ---------------------------------------------------------------------------
let pool
let initPromise

function getPool() {
  if (!pool) {
    // node-postgres does not support SCRAM channel binding; strip it.
    const cs = (process.env.DATABASE_URL || '').replace(/&?channel_binding=require/gi, '')
    pool = new Pool({
      connectionString: cs,
      ssl: { rejectUnauthorized: false },
      max: 5,
      idleTimeoutMillis: 30000,
    })
  }
  return pool
}

async function initDb() {
  const p = getPool()
  await p.query(`
    CREATE TABLE IF NOT EXISTS listings (
      id UUID PRIMARY KEY,
      owner_id UUID,
      type TEXT,
      category TEXT,
      title TEXT,
      vendor TEXT,
      vendor_office TEXT,
      location TEXT,
      map_link TEXT,
      description TEXT,
      includes JSONB DEFAULT '[]'::jsonb,
      price_value NUMERIC DEFAULT 0,
      currency TEXT DEFAULT 'USD',
      price_label TEXT,
      off_peak_value NUMERIC DEFAULT 0,
      off_peak_label TEXT,
      season TEXT,
      image TEXT,
      keywords JSONB DEFAULT '[]'::jsonb,
      commission_rate INTEGER DEFAULT 5,
      created_at TIMESTAMPTZ DEFAULT now()
    )`)
  await p.query(`
    CREATE TABLE IF NOT EXISTS leads (
      id UUID PRIMARY KEY,
      listing_id UUID,
      listing_title TEXT,
      vendor TEXT,
      category TEXT,
      type TEXT,
      price_label TEXT,
      price_value NUMERIC DEFAULT 0,
      currency TEXT DEFAULT 'USD',
      commission NUMERIC DEFAULT 0,
      channel TEXT DEFAULT 'whatsapp',
      created_at TIMESTAMPTZ DEFAULT now()
    )`)
  await p.query(`
    CREATE TABLE IF NOT EXISTS vendors (
      id UUID PRIMARY KEY,
      name TEXT,
      company TEXT,
      email TEXT UNIQUE,
      phone TEXT,
      password_hash TEXT,
      created_at TIMESTAMPTZ DEFAULT now()
    )`)
  await p.query(`
    CREATE TABLE IF NOT EXISTS sessions (
      token TEXT PRIMARY KEY,
      vendor_id UUID,
      created_at TIMESTAMPTZ DEFAULT now()
    )`)
}

async function ensureDb() {
  if (!initPromise) initPromise = initDb()
  await initPromise
}

async function q(text, params) {
  const p = getPool()
  return p.query(text, params)
}

// Business config
const WHATSAPP_PHONE = '254758378729'
const COMMISSION_RATE = 0.05 // 5% charged to vendors

// ---------------------------------------------------------------------------
// Row mappers (snake_case -> camelCase, numeric -> Number)
// ---------------------------------------------------------------------------
function rowToListing(r) {
  if (!r) return null
  return {
    id: r.id,
    ownerId: r.owner_id,
    type: r.type,
    category: r.category,
    title: r.title,
    vendor: r.vendor,
    vendorOffice: r.vendor_office,
    location: r.location,
    mapLink: r.map_link,
    description: r.description,
    includes: r.includes || [],
    priceValue: r.price_value != null ? Number(r.price_value) : 0,
    currency: r.currency,
    priceLabel: r.price_label,
    offPeakValue: r.off_peak_value != null ? Number(r.off_peak_value) : 0,
    offPeakLabel: r.off_peak_label,
    season: r.season,
    image: r.image,
    keywords: r.keywords || [],
    commissionRate: r.commission_rate,
    createdAt: r.created_at,
  }
}

function rowToLead(r) {
  if (!r) return null
  return {
    id: r.id,
    listingId: r.listing_id,
    listingTitle: r.listing_title,
    vendor: r.vendor,
    category: r.category,
    type: r.type,
    priceLabel: r.price_label,
    priceValue: r.price_value != null ? Number(r.price_value) : 0,
    currency: r.currency,
    commission: r.commission != null ? Number(r.commission) : 0,
    channel: r.channel,
    createdAt: r.created_at,
  }
}

function cleanVendor(r) {
  if (!r) return null
  return { id: r.id, name: r.name, company: r.company, email: r.email, phone: r.phone, createdAt: r.created_at }
}

// ---------------------------------------------------------------------------
// Vendor auth helpers
// ---------------------------------------------------------------------------
function hashPassword(password) {
  const salt = crypto.randomBytes(16).toString('hex')
  const hash = crypto.scryptSync(String(password), salt, 64).toString('hex')
  return `${salt}:${hash}`
}

function verifyPassword(password, stored) {
  if (!stored || !stored.includes(':')) return false
  const [salt, hash] = stored.split(':')
  const test = crypto.scryptSync(String(password), salt, 64).toString('hex')
  const a = Buffer.from(hash, 'hex')
  const b = Buffer.from(test, 'hex')
  return a.length === b.length && crypto.timingSafeEqual(a, b)
}

async function getVendorFromRequest(request) {
  const auth = request.headers.get('authorization') || ''
  const token = auth.startsWith('Bearer ') ? auth.slice(7) : null
  if (!token) return null
  const s = await q('SELECT vendor_id FROM sessions WHERE token = $1', [token])
  if (!s.rows.length) return null
  const v = await q('SELECT * FROM vendors WHERE id = $1', [s.rows[0].vendor_id])
  return v.rows[0] || null
}

// ---------------------------------------------------------------------------
// CORS helpers
// ---------------------------------------------------------------------------
function handleCORS(response) {
  response.headers.set('Access-Control-Allow-Origin', process.env.CORS_ORIGINS || '*')
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  response.headers.set('Access-Control-Allow-Credentials', 'true')
  return response
}

export async function OPTIONS() {
  return handleCORS(new NextResponse(null, { status: 200 }))
}

// ---------------------------------------------------------------------------
// Seed data
// ---------------------------------------------------------------------------
function seedListings() {
  const now = new Date()
  const safari = [
    { category: 'Safari Package', title: 'Masai Mara 3-Day Migration Safari', vendor: 'Mara Safari Lodges Ltd', vendorOffice: 'Utalii House, Nairobi CBD', location: 'Masai Mara National Reserve, Narok County', mapLink: 'https://maps.google.com/?q=Masai+Mara+National+Reserve', description: 'Experience the Big Five and the Great Migration. Includes game drives, park fees, transport from Nairobi and 2 nights at a tented camp with all meals.', includes: ['Park fees', 'Transport from Nairobi', '2 Nights Tented Camp', 'All Meals', 'Professional Guide'], priceValue: 350, currency: 'USD', priceLabel: '$350', offPeakValue: 280, offPeakLabel: '$280', season: 'Low season: Apr-Jun', image: 'https://images.unsplash.com/photo-1519659528534-7fd733a832a0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1ODR8MHwxfHNlYXJjaHwxfHxNYXNhaSUyME1hcmF8ZW58MHx8fHwxNzgzMzgyMDcyfDA&ixlib=rb-4.1.0&q=85', keywords: ['mara', 'safari', 'kenya', 'wildlife', 'tour', 'trip', 'holiday', 'migration', 'big five'] },
    { category: 'Safari Package', title: 'Serengeti Great Migration Safari', vendor: 'Wild Trails Tanzania', vendorOffice: 'Arusha Town Centre, Tanzania', location: 'Serengeti National Park, Tanzania', mapLink: 'https://maps.google.com/?q=Serengeti+National+Park', description: 'Witness the Great Wildebeest Migration. 4 days, 3 nights lodge stay with unlimited game drives and expert guides.', includes: ['Park fees', '3 Nights Lodge', 'All Meals', 'Unlimited Game Drives'], priceValue: 750, currency: 'USD', priceLabel: '$750', offPeakValue: 620, offPeakLabel: '$620', season: 'Low season: Mar-May', image: 'https://images.unsplash.com/photo-1597877774402-d04cad0b7596?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NzR8MHwxfHNlYXJjaHwxfHxTZXJlbmdldGklMjB3aWxkbGlmZXxlbnwwfHx8fDE3ODMzODIwNzN8MA&ixlib=rb-4.1.0&q=85', keywords: ['serengeti', 'migration', 'wildlife', 'tanzania', 'tour', 'safari'] },
    { category: 'Kilimanjaro Climb', title: 'Kilimanjaro Machame Route 7-Day Climb', vendor: 'Summit Africa Treks', vendorOffice: 'Moshi, Kilimanjaro Region', location: 'Mount Kilimanjaro, Tanzania', mapLink: 'https://maps.google.com/?q=Mount+Kilimanjaro', description: 'Reach Uhuru Peak (5,895m) via the scenic Machame route. Includes certified mountain guides, porters, camping gear, park fees and all meals on the mountain.', includes: ['Certified Guides & Porters', 'Camping Gear', 'Park & Rescue Fees', 'All Mountain Meals', 'Airport Transfer'], priceValue: 1450, currency: 'USD', priceLabel: '$1,450', offPeakValue: 1200, offPeakLabel: '$1,200', season: 'Low season: Apr-May', image: 'https://images.unsplash.com/photo-1613061445510-e296bfedb73e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxLaWxpbWFuamFyb3xlbnwwfHx8fDE3ODMzODIwNjZ8MA&ixlib=rb-4.1.0&q=85', keywords: ['kilimanjaro', 'mountain', 'climb', 'trek', 'hiking', 'peak', 'uhuru', 'tanzania'] },
    { category: 'Safari Package', title: 'Amboseli Elephants & Kilimanjaro Views 2-Day', vendor: 'Tusker Safaris', vendorOffice: 'Kimathi Street, Nairobi CBD', location: 'Amboseli National Park, Kajiado County', mapLink: 'https://maps.google.com/?q=Amboseli+National+Park', description: 'Get up close to large elephant herds with Mount Kilimanjaro as your backdrop. Includes transport, park fees and lodge accommodation.', includes: ['Park fees', 'Transport', '1 Night Lodge', 'Meals', 'Guide'], priceValue: 290, currency: 'USD', priceLabel: '$290', offPeakValue: 240, offPeakLabel: '$240', season: 'Low season: Apr-Jun', image: 'https://images.unsplash.com/photo-1631646109206-4b5616964f84?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxLaWxpbWFuamFyb3xlbnwwfHx8fDE3ODMzODIwNjZ8MA&ixlib=rb-4.1.0&q=85', keywords: ['amboseli', 'elephant', 'kilimanjaro', 'safari', 'kenya', 'wildlife'] },
    { category: 'Hotel & Resort', title: 'Zanzibar Beach Resort - 4 Days', vendor: 'Blue Ocean Resort', vendorOffice: 'Nungwi, Zanzibar', location: 'Nungwi Beach, Zanzibar, Tanzania', mapLink: 'https://maps.google.com/?q=Nungwi+Beach+Zanzibar', description: 'Relax on white sand beaches. 3 nights in a beachfront resort with breakfast, airport transfers and a sunset dhow cruise.', includes: ['3 Nights Beachfront Room', 'Breakfast', 'Airport Transfers', 'Sunset Dhow Cruise'], priceValue: 490, currency: 'USD', priceLabel: '$490', offPeakValue: 390, offPeakLabel: '$390', season: 'Low season: Apr-Jun', image: 'https://images.unsplash.com/photo-1646668072507-b2215b873c70?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODh8MHwxfHNlYXJjaHwzfHxaYW56aWJhciUyMGJlYWNofGVufDB8fHx8MTc4MzM4MjA2Nnww&ixlib=rb-4.1.0&q=85', keywords: ['zanzibar', 'beach', 'tanzania', 'holiday', 'island', 'vacation', 'resort', 'hotel'] },
    { category: 'Hotel & Resort', title: 'Diani Beach Luxury Lodge', vendor: 'Coral Coast Resorts', vendorOffice: 'Diani Beach Road, Kwale County', location: 'Diani Beach, Kenyan Coast', mapLink: 'https://maps.google.com/?q=Diani+Beach+Kenya', description: 'Oceanfront luxury lodge with pool, spa and reef access. Rate is per night including breakfast.', includes: ['Ocean-view Room', 'Breakfast', 'Pool & Spa', 'Reef Access'], priceValue: 180, currency: 'USD', priceLabel: '$180/night', offPeakValue: 140, offPeakLabel: '$140/night', season: 'Low season: May-Jun', image: 'https://images.unsplash.com/photo-1667987566780-3b31fa5485c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1Mjh8MHwxfHNlYXJjaHw0fHxzYWZhcmklMjBsb2RnZXxlbnwwfHx8fDE3ODMzODIwNzh8MA&ixlib=rb-4.1.0&q=85', keywords: ['diani', 'beach', 'hotel', 'lodge', 'resort', 'coast', 'kenya', 'luxury'] },
    { category: 'Car & Caravan Hire', title: '4x4 Land Cruiser Safari Car Hire', vendor: 'Nairobi Auto Rentals', vendorOffice: 'Mombasa Road, Nairobi', location: 'Pickup: Nairobi / JKIA Airport', mapLink: 'https://maps.google.com/?q=Jomo+Kenyatta+International+Airport', description: 'Fully equipped 4x4 Land Cruiser with pop-up roof, ideal for self-drive safaris. Rate per day, unlimited mileage.', includes: ['Pop-up Roof', 'Unlimited Mileage', 'Insurance', '24/7 Support'], priceValue: 120, currency: 'USD', priceLabel: '$120/day', offPeakValue: 95, offPeakLabel: '$95/day', season: 'Low season rates', image: 'https://images.unsplash.com/photo-1709402606682-400133d92ab2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA2MDV8MHwxfHNlYXJjaHwzfHxzYWZhcmklMjBqZWVwfGVufDB8fHx8MTc4MzM4MjA3M3ww&ixlib=rb-4.1.0&q=85', keywords: ['car', 'hire', 'rental', '4x4', 'land cruiser', 'self drive', 'vehicle', 'jeep'] },
    { category: 'Car & Caravan Hire', title: 'Group Caravan / Overland Truck Hire', vendor: 'East Overland Co', vendorOffice: 'Karen, Nairobi', location: 'Pickup: Nairobi', mapLink: 'https://maps.google.com/?q=Karen+Nairobi', description: 'Overland truck / caravan for group sightseeing tours (up to 18 people). Includes driver and camping setup.', includes: ['Seats up to 18', 'Driver Included', 'Camping Setup', 'Cooler & Storage'], priceValue: 600, currency: 'USD', priceLabel: '$600/day', offPeakValue: 480, offPeakLabel: '$480/day', season: 'Group discounts', image: 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1OTV8MHwxfHNlYXJjaHw0fHxBZnJpY2FuJTIwc2FmYXJpfGVufDB8fHx8MTc4MzM4MjA2Nnww&ixlib=rb-4.1.0&q=85', keywords: ['caravan', 'overland', 'truck', 'group', 'bus', 'hire', 'sightseeing'] },
    { category: 'Light Aircraft Charter', title: 'Light Aircraft Charter (Nairobi - Mara)', vendor: 'Savanna Wings Aviation', vendorOffice: 'Wilson Airport, Nairobi', location: 'Wilson Airport to Masai Mara Airstrips', mapLink: 'https://maps.google.com/?q=Wilson+Airport+Nairobi', description: 'Skip the road trip. Scheduled and charter light aircraft flights from Wilson Airport to the Mara. Price per seat, one way.', includes: ['Per Seat One-Way', '15kg Luggage', 'Scenic Flight', 'Airstrip Transfer'], priceValue: 260, currency: 'USD', priceLabel: '$260/seat', offPeakValue: 210, offPeakLabel: '$210/seat', season: 'Low season fares', image: 'https://images.unsplash.com/photo-1586063029643-fd87377743ef?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxsaWdodCUyMGFpcmNyYWZ0fGVufDB8fHx8MTc4MzM4MjA3OXww&ixlib=rb-4.1.0&q=85', keywords: ['aircraft', 'plane', 'flight', 'charter', 'fly', 'aviation', 'wilson', 'mara'] },
    { category: 'Sightseeing', title: 'Nairobi City & Giraffe Centre Sightseeing Tour', vendor: 'City Explorers', vendorOffice: 'Moi Avenue, Nairobi CBD', location: 'Nairobi National Park, Giraffe Centre & City Tour', mapLink: 'https://maps.google.com/?q=Giraffe+Centre+Nairobi', description: 'Half-day guided city tour including Nairobi National Park, Giraffe Centre and the Karen Blixen Museum.', includes: ['Transport', 'Entry Fees', 'Guide', 'Bottled Water'], priceValue: 75, currency: 'USD', priceLabel: '$75', offPeakValue: 60, offPeakLabel: '$60', season: 'Daily departures', image: 'https://images.unsplash.com/photo-1564101160531-4838e8a5f4e7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1ODR8MHwxfHNlYXJjaHwzfHxNYXNhaSUyME1hcmF8ZW58MHx8fHwxNzgzMzgyMDcyfDA&ixlib=rb-4.1.0&q=85', keywords: ['nairobi', 'city', 'tour', 'sightseeing', 'giraffe', 'day trip', 'museum'] },
  ]

  const local = [
    { category: 'Matatu / Shuttle', title: 'Local Shuttle & Matatu Transport', vendor: 'Kenya Mwananchi Sacco', vendorOffice: 'Tom Mboya Street, Nairobi CBD', location: 'Daily routes across Nairobi & towns', mapLink: 'https://maps.google.com/?q=Nairobi+CBD', description: 'Daily shuttle & matatu transport across cities and towns. Frequent departures throughout the day.', includes: ['Frequent Departures', 'Seated', 'Affordable'], priceValue: 1200, currency: 'KES', priceLabel: 'KES 1,200', offPeakValue: 1000, offPeakLabel: 'KES 1,000', season: 'Off-peak fares', image: 'https://images.unsplash.com/photo-1770283553885-bad1d6f7acd7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwxfHxtYXRhdHUlMjBidXN8ZW58MHx8fHwxNzgzMzgyMDc4fDA&ixlib=rb-4.1.0&q=85', keywords: ['bus', 'matatu', 'transport', 'travel', 'ride', 'shuttle', 'commute'] },
    { category: 'Train (SGR)', title: 'SGR Train Transport (Nairobi \u2194 Mombasa)', vendor: 'Madaraka Express', vendorOffice: 'Syokimau Terminus, Nairobi', location: 'Nairobi \u2194 Mombasa railway', mapLink: 'https://maps.google.com/?q=Syokimau+SGR+Station', description: 'Fast, comfortable Standard Gauge Railway service between Nairobi and Mombasa. Book economy or first class.', includes: ['Economy / First Class', 'Reserved Seat', 'On-time', 'Scenic Route'], priceValue: 1500, currency: 'KES', priceLabel: 'KES 1,500', offPeakValue: 1000, offPeakLabel: 'KES 1,000', season: 'Economy fare', image: 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1OTV8MHwxfHNlYXJjaHw0fHxBZnJpY2FuJTIwc2FmYXJpfGVufDB8fHx8MTc4MzM4MjA2Nnww&ixlib=rb-4.1.0&q=85', keywords: ['train', 'sgr', 'rail', 'mombasa', 'nairobi', 'madaraka'] },
    { category: 'Taxi / Car Hire', title: 'Taxi & Car Hire', vendor: 'CBD Cabs Kenya', vendorOffice: 'Kenyatta Avenue, Nairobi CBD', location: 'Nairobi CBD & environs', mapLink: 'https://maps.google.com/?q=Kenyatta+Avenue+Nairobi', description: 'Affordable ride and car hire services within Nairobi CBD and its environs. Metered and fixed-rate options.', includes: ['Metered / Fixed Rate', 'Airport Runs', 'Daily Hire'], priceValue: 8000, currency: 'KES', priceLabel: 'KES 8,000/day', offPeakValue: 6500, offPeakLabel: 'KES 6,500/day', season: 'Daily hire rate', image: 'https://images.unsplash.com/photo-1709402606682-400133d92ab2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA2MDV8MHwxfHNlYXJjaHwzfHxzYWZhcmklMjBqZWVwfGVufDB8fHx8MTc4MzM4MjA3M3ww&ixlib=rb-4.1.0&q=85', keywords: ['taxi', 'car', 'hire', 'vehicle', 'uber', 'cab', 'ride'] },
    { category: 'Matatu / Shuttle', title: 'Nairobi CBD Commuter Matatu (Sacco)', vendor: 'Embassava Sacco', vendorOffice: 'Ambassadeur Stage, CBD', location: 'CBD to Eastlands, Westlands, Rongai routes', mapLink: 'https://maps.google.com/?q=Ambassadeur+Nairobi', description: 'Everyday commuter matatu service to and from Nairobi CBD. Peak and off-peak fares apply.', includes: ['CBD Estates', 'Peak / Off-peak Fares', 'High Frequency'], priceValue: 100, currency: 'KES', priceLabel: 'KES 100', offPeakValue: 70, offPeakLabel: 'KES 70', season: 'Off-peak fare', image: 'https://images.unsplash.com/photo-1770283553885-bad1d6f7acd7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwxfHxtYXRhdHUlMjBidXN8ZW58MHx8fHwxNzgzMzgyMDc4fDA&ixlib=rb-4.1.0&q=85', keywords: ['matatu', 'commuter', 'cbd', 'nairobi', 'eastlands', 'westlands', 'rongai', 'work'] },
    { category: 'Airport Transfer', title: 'Airport Shuttle (JKIA \u2194 CBD)', vendor: 'JKIA Shuttle Services', vendorOffice: 'JKIA Terminal 1A', location: 'JKIA Airport \u2194 Nairobi CBD', mapLink: 'https://maps.google.com/?q=Jomo+Kenyatta+International+Airport', description: 'Reliable shuttle between JKIA airport and the CBD. Fixed fare, meet & greet available.', includes: ['Fixed Fare', 'Meet & Greet', 'Luggage Space'], priceValue: 1500, currency: 'KES', priceLabel: 'KES 1,500', offPeakValue: 1200, offPeakLabel: 'KES 1,200', season: 'Shared shuttle', image: 'https://images.unsplash.com/photo-1586063029643-fd87377743ef?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxsaWdodCUyMGFpcmNyYWZ0fGVufDB8fHx8MTc4MzM4MjA3OXww&ixlib=rb-4.1.0&q=85', keywords: ['airport', 'jkia', 'shuttle', 'transfer', 'cbd', 'nairobi'] },
  ]

  const all = [
    ...safari.map((s) => ({ ...s, type: 'safari' })),
    ...local.map((l) => ({ ...l, type: 'local' })),
  ]

  return all.map((item) => ({ id: uuidv4(), ownerId: null, ...item, commissionRate: 5, createdAt: now }))
}

async function insertListingRow(d) {
  await q(
    `INSERT INTO listings
      (id, owner_id, type, category, title, vendor, vendor_office, location, map_link, description,
       includes, price_value, currency, price_label, off_peak_value, off_peak_label, season, image, keywords, commission_rate, created_at)
     VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11::jsonb,$12,$13,$14,$15,$16,$17,$18,$19::jsonb,$20,$21)`,
    [
      d.id, d.ownerId || null, d.type, d.category, d.title, d.vendor, d.vendorOffice || '', d.location || '',
      d.mapLink || '', d.description || '', JSON.stringify(d.includes || []), d.priceValue || 0, d.currency || 'USD',
      d.priceLabel || '', d.offPeakValue || 0, d.offPeakLabel || '', d.season || '', d.image || '',
      JSON.stringify(d.keywords || []), d.commissionRate || 5, d.createdAt || new Date(),
    ]
  )
}

// Smart keyword matcher (applied in JS after SQL filter)
function matchesQuery(item, query) {
  if (!query) return true
  const s = query.toLowerCase().trim()
  const words = s.split(/\s+/)
  const haystack = [item.title, item.vendor, item.location, item.category, item.description, ...(item.keywords || [])].join(' ').toLowerCase()
  if (haystack.includes(s)) return true
  return words.some((w) => w.length > 1 && haystack.includes(w))
}

// Column map for updates
const LISTING_COLS = {
  ownerId: 'owner_id', type: 'type', category: 'category', title: 'title', vendor: 'vendor',
  vendorOffice: 'vendor_office', location: 'location', mapLink: 'map_link', description: 'description',
  includes: 'includes', priceValue: 'price_value', currency: 'currency', priceLabel: 'price_label',
  offPeakValue: 'off_peak_value', offPeakLabel: 'off_peak_label', season: 'season', image: 'image',
  keywords: 'keywords', commissionRate: 'commission_rate',
}

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------
async function handleRoute(request, { params }) {
  const { path = [] } = await params
  const route = `/${path.join('/')}`
  const method = request.method
  const url = new URL(request.url)

  try {
    await ensureDb()

    // Health
    if ((route === '/' || route === '/root') && method === 'GET') {
      return handleCORS(NextResponse.json({ message: 'OSARE API running (PostgreSQL/NEON)', whatsapp: WHATSAPP_PHONE }))
    }

    // Seed sample data
    if (route === '/seed' && method === 'POST') {
      await q('DELETE FROM listings')
      const docs = seedListings()
      await Promise.all(docs.map(insertListingRow))
      return handleCORS(NextResponse.json({ inserted: docs.length }))
    }

    // ---------------- Vendor auth ----------------
    if (route === '/auth/register' && method === 'POST') {
      const body = await request.json()
      if (!body.email || !body.password) {
        return handleCORS(NextResponse.json({ error: 'email and password are required' }, { status: 400 }))
      }
      const email = String(body.email).toLowerCase().trim()
      const existing = await q('SELECT id FROM vendors WHERE email = $1', [email])
      if (existing.rows.length) {
        return handleCORS(NextResponse.json({ error: 'Email already registered' }, { status: 409 }))
      }
      const id = uuidv4()
      const row = (await q(
        `INSERT INTO vendors (id, name, company, email, phone, password_hash, created_at)
         VALUES ($1,$2,$3,$4,$5,$6, now()) RETURNING *`,
        [id, body.name || '', body.company || '', email, body.phone || '', hashPassword(body.password)]
      )).rows[0]
      const token = uuidv4()
      await q('INSERT INTO sessions (token, vendor_id, created_at) VALUES ($1,$2, now())', [token, id])
      return handleCORS(NextResponse.json({ token, vendor: cleanVendor(row) }))
    }

    if (route === '/auth/login' && method === 'POST') {
      const body = await request.json()
      const email = String(body.email || '').toLowerCase().trim()
      const row = (await q('SELECT * FROM vendors WHERE email = $1', [email])).rows[0]
      if (!row || !verifyPassword(body.password || '', row.password_hash)) {
        return handleCORS(NextResponse.json({ error: 'Invalid email or password' }, { status: 401 }))
      }
      const token = uuidv4()
      await q('INSERT INTO sessions (token, vendor_id, created_at) VALUES ($1,$2, now())', [token, row.id])
      return handleCORS(NextResponse.json({ token, vendor: cleanVendor(row) }))
    }

    if (route === '/auth/me' && method === 'GET') {
      const vendor = await getVendorFromRequest(request)
      if (!vendor) return handleCORS(NextResponse.json({ error: 'Unauthorized' }, { status: 401 }))
      return handleCORS(NextResponse.json({ vendor: cleanVendor(vendor) }))
    }

    // Vendor's own listings
    if (route === '/my-listings' && method === 'GET') {
      const vendor = await getVendorFromRequest(request)
      if (!vendor) return handleCORS(NextResponse.json({ error: 'Unauthorized' }, { status: 401 }))
      const rows = (await q('SELECT * FROM listings WHERE owner_id = $1 ORDER BY created_at DESC', [vendor.id])).rows
      return handleCORS(NextResponse.json(rows.map(rowToListing)))
    }

    // Vendor revenue stats
    if (route === '/my-stats' && method === 'GET') {
      const vendor = await getVendorFromRequest(request)
      if (!vendor) return handleCORS(NextResponse.json({ error: 'Unauthorized' }, { status: 401 }))
      const myListings = (await q('SELECT id FROM listings WHERE owner_id = $1', [vendor.id])).rows
      const ids = myListings.map((r) => r.id)
      let leadRows = []
      if (ids.length) {
        leadRows = (await q('SELECT * FROM leads WHERE listing_id = ANY($1::uuid[]) ORDER BY created_at DESC', [ids])).rows
      }
      const leads = leadRows.map(rowToLead)
      let commissionOwedUSD = 0
      for (const l of leads) {
        const usd = l.currency === 'KES' ? l.priceValue / 150 : l.priceValue
        commissionOwedUSD += usd * COMMISSION_RATE
      }
      return handleCORS(NextResponse.json({
        listings: myListings.length,
        leads: leads.length,
        commissionOwedUSD: Math.round(commissionOwedUSD * 100) / 100,
        recentLeads: leads.slice(0, 20),
      }))
    }

    // ---------------- Listings ----------------
    if (route === '/listings' && method === 'GET') {
      const type = url.searchParams.get('type')
      const category = url.searchParams.get('category')
      const search = url.searchParams.get('q')

      const clauses = []
      const args = []
      if (type) { args.push(type); clauses.push(`type = $${args.length}`) }
      if (category && category !== 'All') { args.push(category); clauses.push(`category = $${args.length}`) }
      const where = clauses.length ? `WHERE ${clauses.join(' AND ')}` : ''
      const rows = (await q(`SELECT * FROM listings ${where} ORDER BY created_at DESC LIMIT 500`, args)).rows
      let items = rows.map(rowToListing)
      if (search) items = items.filter((it) => matchesQuery(it, search))
      return handleCORS(NextResponse.json(items))
    }

    if (route === '/listings' && method === 'POST') {
      const body = await request.json()
      if (!body.title || !body.type) {
        return handleCORS(NextResponse.json({ error: 'title and type are required' }, { status: 400 }))
      }
      const vendorAuth = await getVendorFromRequest(request)
      const doc = {
        id: uuidv4(),
        ownerId: vendorAuth ? vendorAuth.id : (body.ownerId || null),
        type: body.type,
        category: body.category || 'General',
        title: body.title,
        vendor: body.vendor || vendorAuth?.company || vendorAuth?.name || 'Unknown Vendor',
        vendorOffice: body.vendorOffice || '',
        location: body.location || '',
        mapLink: body.mapLink || '',
        description: body.description || '',
        includes: Array.isArray(body.includes) ? body.includes : (body.includes ? String(body.includes).split(',').map((s) => s.trim()).filter(Boolean) : []),
        priceValue: Number(body.priceValue) || 0,
        currency: body.currency || 'USD',
        priceLabel: body.priceLabel || '',
        offPeakValue: Number(body.offPeakValue) || 0,
        offPeakLabel: body.offPeakLabel || '',
        season: body.season || '',
        image: body.image || 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?q=80&w=800',
        keywords: Array.isArray(body.keywords) ? body.keywords : (body.keywords ? String(body.keywords).split(',').map((s) => s.trim()).filter(Boolean) : []),
        commissionRate: 5,
        createdAt: new Date(),
      }
      await insertListingRow(doc)
      return handleCORS(NextResponse.json(doc))
    }

    // Update listing - /listings/:id
    if (path[0] === 'listings' && path[1] && method === 'PUT') {
      const id = path[1]
      const body = await request.json()
      const sets = []
      const args = []
      for (const [k, v] of Object.entries(body)) {
        const col = LISTING_COLS[k]
        if (!col) continue
        if (k === 'includes' || k === 'keywords') {
          const arr = Array.isArray(v) ? v : String(v).split(',').map((s) => s.trim()).filter(Boolean)
          args.push(JSON.stringify(arr))
          sets.push(`${col} = $${args.length}::jsonb`)
        } else {
          args.push(v)
          sets.push(`${col} = $${args.length}`)
        }
      }
      if (!sets.length) {
        return handleCORS(NextResponse.json({ error: 'No valid fields to update' }, { status: 400 }))
      }
      args.push(id)
      const rows = (await q(`UPDATE listings SET ${sets.join(', ')} WHERE id = $${args.length} RETURNING *`, args)).rows
      if (!rows.length) return handleCORS(NextResponse.json({ error: 'Not found' }, { status: 404 }))
      return handleCORS(NextResponse.json(rowToListing(rows[0])))
    }

    // Delete listing - /listings/:id
    if (path[0] === 'listings' && path[1] && method === 'DELETE') {
      const id = path[1]
      await q('DELETE FROM listings WHERE id = $1', [id])
      return handleCORS(NextResponse.json({ deleted: true, id }))
    }

    // ---------------- Leads ----------------
    if (route === '/leads' && method === 'POST') {
      const body = await request.json()
      let listing = null
      if (body.listingId) {
        listing = (await q('SELECT * FROM listings WHERE id = $1', [body.listingId])).rows[0] || null
      }
      const title = listing?.title || body.title || 'a listing'
      const priceLabel = listing?.price_label || body.priceLabel || ''
      const priceValue = listing ? Number(listing.price_value) : (Number(body.priceValue) || 0)
      const currency = listing?.currency || body.currency || 'USD'
      const vendor = listing?.vendor || body.vendor || ''
      const category = listing?.category || body.category || ''
      const type = listing?.type || body.type || ''
      const commission = Math.round(priceValue * COMMISSION_RATE * 100) / 100

      const id = uuidv4()
      await q(
        `INSERT INTO leads (id, listing_id, listing_title, vendor, category, type, price_label, price_value, currency, commission, channel, created_at)
         VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,'whatsapp', now())`,
        [id, body.listingId || null, title, vendor, category, type, priceLabel, priceValue, currency, commission]
      )
      const message = `Hello OSARE, I'd like to book: ${title}${priceLabel ? ' (' + priceLabel + ')' : ''}${vendor ? ' with ' + vendor : ''}. [Ref: ${id.slice(0, 8)}]`
      const whatsappUrl = `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(message)}`
      return handleCORS(NextResponse.json({
        id, listingId: body.listingId || null, listingTitle: title, vendor, category, type,
        priceLabel, priceValue, currency, commission, channel: 'whatsapp', whatsappUrl,
      }))
    }

    if (route === '/leads' && method === 'GET') {
      const rows = (await q('SELECT * FROM leads ORDER BY created_at DESC LIMIT 500')).rows
      return handleCORS(NextResponse.json(rows.map(rowToLead)))
    }

    // ---------------- Dashboard stats ----------------
    if (route === '/stats' && method === 'GET') {
      const listingRows = (await q('SELECT type FROM listings')).rows
      const leadRows = (await q('SELECT * FROM leads')).rows
      const leads = leadRows.map(rowToLead)

      const totalListings = listingRows.length
      const safariCount = listingRows.filter((l) => l.type === 'safari').length
      const localCount = listingRows.filter((l) => l.type === 'local').length
      const totalLeads = leads.length

      let estRevenueUSD = 0
      const leadsByCategory = {}
      const leadsByType = { safari: 0, local: 0 }
      for (const l of leads) {
        const usd = l.currency === 'KES' ? l.priceValue / 150 : l.priceValue
        estRevenueUSD += usd * COMMISSION_RATE
        leadsByCategory[l.category || 'Other'] = (leadsByCategory[l.category || 'Other'] || 0) + 1
        if (l.type === 'safari') leadsByType.safari += 1
        else if (l.type === 'local') leadsByType.local += 1
      }

      return handleCORS(NextResponse.json({
        totalListings, safariCount, localCount, totalLeads,
        estRevenueUSD: Math.round(estRevenueUSD * 100) / 100,
        commissionRate: 5,
        leadsByCategory: Object.entries(leadsByCategory).map(([name, value]) => ({ name, value })),
        leadsByType,
      }))
    }

    return handleCORS(NextResponse.json({ error: `Route ${route} not found` }, { status: 404 }))
  } catch (error) {
    console.error('API Error:', error)
    return handleCORS(NextResponse.json({ error: 'Internal server error', detail: String(error) }, { status: 500 }))
  }
}

export const GET = handleRoute
export const POST = handleRoute
export const PUT = handleRoute
export const DELETE = handleRoute
export const PATCH = handleRoute
