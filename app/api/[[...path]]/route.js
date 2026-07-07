import { MongoClient } from 'mongodb'
import { v4 as uuidv4 } from 'uuid'
import { NextResponse } from 'next/server'

// ---------------------------------------------------------------------------
// MongoDB connection (singleton)
// ---------------------------------------------------------------------------
let client
let db

async function connectToMongo() {
  if (!client) {
    client = new MongoClient(process.env.MONGO_URL)
    await client.connect()
    db = client.db(process.env.DB_NAME)
  }
  return db
}

// Business config
const WHATSAPP_PHONE = '254758378729'
const COMMISSION_RATE = 0.05 // 5% charged to vendors

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
// Seed data (OSARE - East Africa Safari Routes)
// ---------------------------------------------------------------------------
function seedListings() {
  const now = new Date()
  const safari = [
    {
      category: 'Safari Package',
      title: 'Masai Mara 3-Day Migration Safari',
      vendor: 'Mara Safari Lodges Ltd',
      vendorOffice: 'Utalii House, Nairobi CBD',
      location: 'Masai Mara National Reserve, Narok County',
      mapLink: 'https://maps.google.com/?q=Masai+Mara+National+Reserve',
      description: 'Experience the Big Five and the Great Migration. Includes game drives, park fees, transport from Nairobi and 2 nights at a tented camp with all meals.',
      includes: ['Park fees', 'Transport from Nairobi', '2 Nights Tented Camp', 'All Meals', 'Professional Guide'],
      priceValue: 350, currency: 'USD', priceLabel: '$350',
      offPeakValue: 280, offPeakLabel: '$280', season: 'Low season: Apr-Jun',
      image: 'https://images.unsplash.com/photo-1519659528534-7fd733a832a0?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1ODR8MHwxfHNlYXJjaHwxfHxNYXNhaSUyME1hcmF8ZW58MHx8fHwxNzgzMzgyMDcyfDA&ixlib=rb-4.1.0&q=85',
      keywords: ['mara', 'safari', 'kenya', 'wildlife', 'tour', 'trip', 'holiday', 'migration', 'big five']
    },
    {
      category: 'Safari Package',
      title: 'Serengeti Great Migration Safari',
      vendor: 'Wild Trails Tanzania',
      vendorOffice: 'Arusha Town Centre, Tanzania',
      location: 'Serengeti National Park, Tanzania',
      mapLink: 'https://maps.google.com/?q=Serengeti+National+Park',
      description: 'Witness the Great Wildebeest Migration. 4 days, 3 nights lodge stay with unlimited game drives and expert guides.',
      includes: ['Park fees', '3 Nights Lodge', 'All Meals', 'Unlimited Game Drives'],
      priceValue: 750, currency: 'USD', priceLabel: '$750',
      offPeakValue: 620, offPeakLabel: '$620', season: 'Low season: Mar-May',
      image: 'https://images.unsplash.com/photo-1597877774402-d04cad0b7596?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NzR8MHwxfHNlYXJjaHwxfHxTZXJlbmdldGklMjB3aWxkbGlmZXxlbnwwfHx8fDE3ODMzODIwNzN8MA&ixlib=rb-4.1.0&q=85',
      keywords: ['serengeti', 'migration', 'wildlife', 'tanzania', 'tour', 'safari']
    },
    {
      category: 'Kilimanjaro Climb',
      title: 'Kilimanjaro Machame Route 7-Day Climb',
      vendor: 'Summit Africa Treks',
      vendorOffice: 'Moshi, Kilimanjaro Region',
      location: 'Mount Kilimanjaro, Tanzania',
      mapLink: 'https://maps.google.com/?q=Mount+Kilimanjaro',
      description: 'Reach Uhuru Peak (5,895m) via the scenic Machame route. Includes certified mountain guides, porters, camping gear, park fees and all meals on the mountain.',
      includes: ['Certified Guides & Porters', 'Camping Gear', 'Park & Rescue Fees', 'All Mountain Meals', 'Airport Transfer'],
      priceValue: 1450, currency: 'USD', priceLabel: '$1,450',
      offPeakValue: 1200, offPeakLabel: '$1,200', season: 'Low season: Apr-May',
      image: 'https://images.unsplash.com/photo-1613061445510-e296bfedb73e?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwzfHxLaWxpbWFuamFyb3xlbnwwfHx8fDE3ODMzODIwNjZ8MA&ixlib=rb-4.1.0&q=85',
      keywords: ['kilimanjaro', 'mountain', 'climb', 'trek', 'hiking', 'peak', 'uhuru', 'tanzania']
    },
    {
      category: 'Safari Package',
      title: 'Amboseli Elephants & Kilimanjaro Views 2-Day',
      vendor: 'Tusker Safaris',
      vendorOffice: 'Kimathi Street, Nairobi CBD',
      location: 'Amboseli National Park, Kajiado County',
      mapLink: 'https://maps.google.com/?q=Amboseli+National+Park',
      description: 'Get up close to large elephant herds with Mount Kilimanjaro as your backdrop. Includes transport, park fees and lodge accommodation.',
      includes: ['Park fees', 'Transport', '1 Night Lodge', 'Meals', 'Guide'],
      priceValue: 290, currency: 'USD', priceLabel: '$290',
      offPeakValue: 240, offPeakLabel: '$240', season: 'Low season: Apr-Jun',
      image: 'https://images.unsplash.com/photo-1631646109206-4b5616964f84?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDJ8MHwxfHNlYXJjaHwxfHxLaWxpbWFuamFyb3xlbnwwfHx8fDE3ODMzODIwNjZ8MA&ixlib=rb-4.1.0&q=85',
      keywords: ['amboseli', 'elephant', 'kilimanjaro', 'safari', 'kenya', 'wildlife']
    },
    {
      category: 'Hotel & Resort',
      title: 'Zanzibar Beach Resort - 4 Days',
      vendor: 'Blue Ocean Resort',
      vendorOffice: 'Nungwi, Zanzibar',
      location: 'Nungwi Beach, Zanzibar, Tanzania',
      mapLink: 'https://maps.google.com/?q=Nungwi+Beach+Zanzibar',
      description: 'Relax on white sand beaches. 3 nights in a beachfront resort with breakfast, airport transfers and a sunset dhow cruise.',
      includes: ['3 Nights Beachfront Room', 'Breakfast', 'Airport Transfers', 'Sunset Dhow Cruise'],
      priceValue: 490, currency: 'USD', priceLabel: '$490',
      offPeakValue: 390, offPeakLabel: '$390', season: 'Low season: Apr-Jun',
      image: 'https://images.unsplash.com/photo-1646668072507-b2215b873c70?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODh8MHwxfHNlYXJjaHwzfHxaYW56aWJhciUyMGJlYWNofGVufDB8fHx8MTc4MzM4MjA2Nnww&ixlib=rb-4.1.0&q=85',
      keywords: ['zanzibar', 'beach', 'tanzania', 'holiday', 'island', 'vacation', 'resort', 'hotel']
    },
    {
      category: 'Hotel & Resort',
      title: 'Diani Beach Luxury Lodge',
      vendor: 'Coral Coast Resorts',
      vendorOffice: 'Diani Beach Road, Kwale County',
      location: 'Diani Beach, Kenyan Coast',
      mapLink: 'https://maps.google.com/?q=Diani+Beach+Kenya',
      description: 'Oceanfront luxury lodge with pool, spa and reef access. Rate is per night including breakfast.',
      includes: ['Ocean-view Room', 'Breakfast', 'Pool & Spa', 'Reef Access'],
      priceValue: 180, currency: 'USD', priceLabel: '$180/night',
      offPeakValue: 140, offPeakLabel: '$140/night', season: 'Low season: May-Jun',
      image: 'https://images.unsplash.com/photo-1667987566780-3b31fa5485c8?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1Mjh8MHwxfHNlYXJjaHw0fHxzYWZhcmklMjBsb2RnZXxlbnwwfHx8fDE3ODMzODIwNzh8MA&ixlib=rb-4.1.0&q=85',
      keywords: ['diani', 'beach', 'hotel', 'lodge', 'resort', 'coast', 'kenya', 'luxury']
    },
    {
      category: 'Car & Caravan Hire',
      title: '4x4 Land Cruiser Safari Car Hire',
      vendor: 'Nairobi Auto Rentals',
      vendorOffice: 'Mombasa Road, Nairobi',
      location: 'Pickup: Nairobi / JKIA Airport',
      mapLink: 'https://maps.google.com/?q=Jomo+Kenyatta+International+Airport',
      description: 'Fully equipped 4x4 Land Cruiser with pop-up roof, ideal for self-drive safaris. Rate per day, unlimited mileage.',
      includes: ['Pop-up Roof', 'Unlimited Mileage', 'Insurance', '24/7 Support'],
      priceValue: 120, currency: 'USD', priceLabel: '$120/day',
      offPeakValue: 95, offPeakLabel: '$95/day', season: 'Low season rates',
      image: 'https://images.unsplash.com/photo-1709402606682-400133d92ab2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA2MDV8MHwxfHNlYXJjaHwzfHxzYWZhcmklMjBqZWVwfGVufDB8fHx8MTc4MzM4MjA3M3ww&ixlib=rb-4.1.0&q=85',
      keywords: ['car', 'hire', 'rental', '4x4', 'land cruiser', 'self drive', 'vehicle', 'jeep']
    },
    {
      category: 'Car & Caravan Hire',
      title: 'Group Caravan / Overland Truck Hire',
      vendor: 'East Overland Co',
      vendorOffice: 'Karen, Nairobi',
      location: 'Pickup: Nairobi',
      mapLink: 'https://maps.google.com/?q=Karen+Nairobi',
      description: 'Overland truck / caravan for group sightseeing tours (up to 18 people). Includes driver and camping setup.',
      includes: ['Seats up to 18', 'Driver Included', 'Camping Setup', 'Cooler & Storage'],
      priceValue: 600, currency: 'USD', priceLabel: '$600/day',
      offPeakValue: 480, offPeakLabel: '$480/day', season: 'Group discounts',
      image: 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1OTV8MHwxfHNlYXJjaHw0fHxBZnJpY2FuJTIwc2FmYXJpfGVufDB8fHx8MTc4MzM4MjA2Nnww&ixlib=rb-4.1.0&q=85',
      keywords: ['caravan', 'overland', 'truck', 'group', 'bus', 'hire', 'sightseeing']
    },
    {
      category: 'Light Aircraft Charter',
      title: 'Light Aircraft Charter (Nairobi - Mara)',
      vendor: 'Savanna Wings Aviation',
      vendorOffice: 'Wilson Airport, Nairobi',
      location: 'Wilson Airport to Masai Mara Airstrips',
      mapLink: 'https://maps.google.com/?q=Wilson+Airport+Nairobi',
      description: 'Skip the road trip. Scheduled and charter light aircraft flights from Wilson Airport to the Mara. Price per seat, one way.',
      includes: ['Per Seat One-Way', '15kg Luggage', 'Scenic Flight', 'Airstrip Transfer'],
      priceValue: 260, currency: 'USD', priceLabel: '$260/seat',
      offPeakValue: 210, offPeakLabel: '$210/seat', season: 'Low season fares',
      image: 'https://images.unsplash.com/photo-1586063029643-fd87377743ef?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxsaWdodCUyMGFpcmNyYWZ0fGVufDB8fHx8MTc4MzM4MjA3OXww&ixlib=rb-4.1.0&q=85',
      keywords: ['aircraft', 'plane', 'flight', 'charter', 'fly', 'aviation', 'wilson', 'mara']
    },
    {
      category: 'Sightseeing',
      title: 'Nairobi City & Giraffe Centre Sightseeing Tour',
      vendor: 'City Explorers',
      vendorOffice: 'Moi Avenue, Nairobi CBD',
      location: 'Nairobi National Park, Giraffe Centre & City Tour',
      mapLink: 'https://maps.google.com/?q=Giraffe+Centre+Nairobi',
      description: 'Half-day guided city tour including Nairobi National Park, Giraffe Centre and the Karen Blixen Museum.',
      includes: ['Transport', 'Entry Fees', 'Guide', 'Bottled Water'],
      priceValue: 75, currency: 'USD', priceLabel: '$75',
      offPeakValue: 60, offPeakLabel: '$60', season: 'Daily departures',
      image: 'https://images.unsplash.com/photo-1564101160531-4838e8a5f4e7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1ODR8MHwxfHNlYXJjaHwzfHxNYXNhaSUyME1hcmF8ZW58MHx8fHwxNzgzMzgyMDcyfDA&ixlib=rb-4.1.0&q=85',
      keywords: ['nairobi', 'city', 'tour', 'sightseeing', 'giraffe', 'day trip', 'museum']
    }
  ]

  const local = [
    {
      category: 'Matatu / Shuttle',
      title: 'Local Shuttle & Matatu Transport',
      vendor: 'Kenya Mwananchi Sacco',
      vendorOffice: 'Tom Mboya Street, Nairobi CBD',
      location: 'Daily routes across Nairobi & towns',
      mapLink: 'https://maps.google.com/?q=Nairobi+CBD',
      description: 'Daily shuttle & matatu transport across cities and towns. Frequent departures throughout the day.',
      includes: ['Frequent Departures', 'Seated', 'Affordable'],
      priceValue: 1200, currency: 'KES', priceLabel: 'KES 1,200',
      offPeakValue: 1000, offPeakLabel: 'KES 1,000', season: 'Off-peak fares',
      image: 'https://images.unsplash.com/photo-1770283553885-bad1d6f7acd7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwxfHxtYXRhdHUlMjBidXN8ZW58MHx8fHwxNzgzMzgyMDc4fDA&ixlib=rb-4.1.0&q=85',
      keywords: ['bus', 'matatu', 'transport', 'travel', 'ride', 'shuttle', 'commute']
    },
    {
      category: 'Train (SGR)',
      title: 'SGR Train Transport (Nairobi \u2194 Mombasa)',
      vendor: 'Madaraka Express',
      vendorOffice: 'Syokimau Terminus, Nairobi',
      location: 'Nairobi \u2194 Mombasa railway',
      mapLink: 'https://maps.google.com/?q=Syokimau+SGR+Station',
      description: 'Fast, comfortable Standard Gauge Railway service between Nairobi and Mombasa. Book economy or first class.',
      includes: ['Economy / First Class', 'Reserved Seat', 'On-time', 'Scenic Route'],
      priceValue: 1500, currency: 'KES', priceLabel: 'KES 1,500',
      offPeakValue: 1000, offPeakLabel: 'KES 1,000', season: 'Economy fare',
      image: 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1OTV8MHwxfHNlYXJjaHw0fHxBZnJpY2FuJTIwc2FmYXJpfGVufDB8fHx8MTc4MzM4MjA2Nnww&ixlib=rb-4.1.0&q=85',
      keywords: ['train', 'sgr', 'rail', 'mombasa', 'nairobi', 'madaraka']
    },
    {
      category: 'Taxi / Car Hire',
      title: 'Taxi & Car Hire',
      vendor: 'CBD Cabs Kenya',
      vendorOffice: 'Kenyatta Avenue, Nairobi CBD',
      location: 'Nairobi CBD & environs',
      mapLink: 'https://maps.google.com/?q=Kenyatta+Avenue+Nairobi',
      description: 'Affordable ride and car hire services within Nairobi CBD and its environs. Metered and fixed-rate options.',
      includes: ['Metered / Fixed Rate', 'Airport Runs', 'Daily Hire'],
      priceValue: 8000, currency: 'KES', priceLabel: 'KES 8,000/day',
      offPeakValue: 6500, offPeakLabel: 'KES 6,500/day', season: 'Daily hire rate',
      image: 'https://images.unsplash.com/photo-1709402606682-400133d92ab2?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA2MDV8MHwxfHNlYXJjaHwzfHxzYWZhcmklMjBqZWVwfGVufDB8fHx8MTc4MzM4MjA3M3ww&ixlib=rb-4.1.0&q=85',
      keywords: ['taxi', 'car', 'hire', 'vehicle', 'uber', 'cab', 'ride']
    },
    {
      category: 'Matatu / Shuttle',
      title: 'Nairobi CBD Commuter Matatu (Sacco)',
      vendor: 'Embassava Sacco',
      vendorOffice: 'Ambassadeur Stage, CBD',
      location: 'CBD to Eastlands, Westlands, Rongai routes',
      mapLink: 'https://maps.google.com/?q=Ambassadeur+Nairobi',
      description: 'Everyday commuter matatu service to and from Nairobi CBD. Peak and off-peak fares apply.',
      includes: ['CBD Estates', 'Peak / Off-peak Fares', 'High Frequency'],
      priceValue: 100, currency: 'KES', priceLabel: 'KES 100',
      offPeakValue: 70, offPeakLabel: 'KES 70', season: 'Off-peak fare',
      image: 'https://images.unsplash.com/photo-1770283553885-bad1d6f7acd7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwxfHxtYXRhdHUlMjBidXN8ZW58MHx8fHwxNzgzMzgyMDc4fDA&ixlib=rb-4.1.0&q=85',
      keywords: ['matatu', 'commuter', 'cbd', 'nairobi', 'eastlands', 'westlands', 'rongai', 'work']
    },
    {
      category: 'Airport Transfer',
      title: 'Airport Shuttle (JKIA \u2194 CBD)',
      vendor: 'JKIA Shuttle Services',
      vendorOffice: 'JKIA Terminal 1A',
      location: 'JKIA Airport \u2194 Nairobi CBD',
      mapLink: 'https://maps.google.com/?q=Jomo+Kenyatta+International+Airport',
      description: 'Reliable shuttle between JKIA airport and the CBD. Fixed fare, meet & greet available.',
      includes: ['Fixed Fare', 'Meet & Greet', 'Luggage Space'],
      priceValue: 1500, currency: 'KES', priceLabel: 'KES 1,500',
      offPeakValue: 1200, offPeakLabel: 'KES 1,200', season: 'Shared shuttle',
      image: 'https://images.unsplash.com/photo-1586063029643-fd87377743ef?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NjZ8MHwxfHNlYXJjaHwzfHxsaWdodCUyMGFpcmNyYWZ0fGVufDB8fHx8MTc4MzM4MjA3OXww&ixlib=rb-4.1.0&q=85',
      keywords: ['airport', 'jkia', 'shuttle', 'transfer', 'cbd', 'nairobi']
    }
  ]

  const all = [
    ...safari.map((s) => ({ ...s, type: 'safari' })),
    ...local.map((l) => ({ ...l, type: 'local' }))
  ]

  return all.map((item) => ({
    id: uuidv4(),
    ...item,
    commissionRate: 5,
    createdAt: now
  }))
}

// Smart keyword matcher (server-side)
function matchesQuery(item, q) {
  if (!q) return true
  const query = q.toLowerCase().trim()
  const words = query.split(/\s+/)
  const haystack = [
    item.title, item.vendor, item.location, item.category, item.description,
    ...(item.keywords || [])
  ].join(' ').toLowerCase()
  if (haystack.includes(query)) return true
  return words.some((w) => w.length > 1 && haystack.includes(w))
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
    const db = await connectToMongo()

    // Health
    if ((route === '/' || route === '/root') && method === 'GET') {
      return handleCORS(NextResponse.json({ message: 'OSARE API running', whatsapp: WHATSAPP_PHONE }))
    }

    // Seed sample data
    if (route === '/seed' && method === 'POST') {
      await db.collection('listings').deleteMany({})
      const docs = seedListings()
      await db.collection('listings').insertMany(docs)
      return handleCORS(NextResponse.json({ inserted: docs.length }))
    }

    // List / search listings
    if (route === '/listings' && method === 'GET') {
      const type = url.searchParams.get('type')
      const q = url.searchParams.get('q')
      const category = url.searchParams.get('category')

      const filter = {}
      if (type) filter.type = type
      if (category && category !== 'All') filter.category = category

      let items = await db.collection('listings').find(filter).sort({ createdAt: -1 }).limit(500).toArray()
      items = items.map(({ _id, ...rest }) => rest)
      if (q) items = items.filter((it) => matchesQuery(it, q))
      return handleCORS(NextResponse.json(items))
    }

    // Create listing
    if (route === '/listings' && method === 'POST') {
      const body = await request.json()
      if (!body.title || !body.type) {
        return handleCORS(NextResponse.json({ error: 'title and type are required' }, { status: 400 }))
      }
      const doc = {
        id: uuidv4(),
        type: body.type,
        category: body.category || 'General',
        title: body.title,
        vendor: body.vendor || 'Unknown Vendor',
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
        createdAt: new Date()
      }
      await db.collection('listings').insertOne(doc)
      const { _id, ...clean } = doc
      return handleCORS(NextResponse.json(clean))
    }

    // Update listing - /listings/:id
    if (path[0] === 'listings' && path[1] && method === 'PUT') {
      const id = path[1]
      const body = await request.json()
      delete body._id
      delete body.id
      await db.collection('listings').updateOne({ id }, { $set: body })
      const updated = await db.collection('listings').findOne({ id })
      if (!updated) return handleCORS(NextResponse.json({ error: 'Not found' }, { status: 404 }))
      const { _id, ...clean } = updated
      return handleCORS(NextResponse.json(clean))
    }

    // Delete listing - /listings/:id
    if (path[0] === 'listings' && path[1] && method === 'DELETE') {
      const id = path[1]
      await db.collection('listings').deleteOne({ id })
      return handleCORS(NextResponse.json({ deleted: true, id }))
    }

    // Create booking lead (WhatsApp) - returns wa.me url
    if (route === '/leads' && method === 'POST') {
      const body = await request.json()
      let listing = null
      if (body.listingId) {
        listing = await db.collection('listings').findOne({ id: body.listingId })
      }
      const title = listing?.title || body.title || 'a listing'
      const priceLabel = listing?.priceLabel || body.priceLabel || ''
      const priceValue = listing?.priceValue || Number(body.priceValue) || 0
      const currency = listing?.currency || body.currency || 'USD'
      const vendor = listing?.vendor || body.vendor || ''
      const commission = Math.round(priceValue * COMMISSION_RATE * 100) / 100

      const lead = {
        id: uuidv4(),
        listingId: body.listingId || null,
        listingTitle: title,
        vendor,
        category: listing?.category || body.category || '',
        type: listing?.type || body.type || '',
        priceLabel,
        priceValue,
        currency,
        commission,
        channel: 'whatsapp',
        createdAt: new Date()
      }
      await db.collection('leads').insertOne(lead)

      const message = `Hello OSARE, I'd like to book: ${title}${priceLabel ? ' (' + priceLabel + ')' : ''}${vendor ? ' with ' + vendor : ''}. [Ref: ${lead.id.slice(0, 8)}]`
      const whatsappUrl = `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(message)}`
      const { _id, ...clean } = lead
      return handleCORS(NextResponse.json({ ...clean, whatsappUrl }))
    }

    // List leads
    if (route === '/leads' && method === 'GET') {
      let leads = await db.collection('leads').find({}).sort({ createdAt: -1 }).limit(500).toArray()
      leads = leads.map(({ _id, ...rest }) => rest)
      return handleCORS(NextResponse.json(leads))
    }

    // Dashboard stats
    if (route === '/stats' && method === 'GET') {
      const listings = await db.collection('listings').find({}).toArray()
      const leads = await db.collection('leads').find({}).toArray()

      const totalListings = listings.length
      const safariCount = listings.filter((l) => l.type === 'safari').length
      const localCount = listings.filter((l) => l.type === 'local').length
      const totalLeads = leads.length

      // Estimated commission revenue (USD-equivalent, KES converted ~ /150)
      let estRevenueUSD = 0
      const leadsByCategory = {}
      const leadsByType = { safari: 0, local: 0 }
      for (const l of leads) {
        const usd = l.currency === 'KES' ? (l.priceValue / 150) : l.priceValue
        estRevenueUSD += usd * COMMISSION_RATE
        leadsByCategory[l.category || 'Other'] = (leadsByCategory[l.category || 'Other'] || 0) + 1
        if (l.type === 'safari') leadsByType.safari += 1
        else if (l.type === 'local') leadsByType.local += 1
      }

      return handleCORS(NextResponse.json({
        totalListings,
        safariCount,
        localCount,
        totalLeads,
        estRevenueUSD: Math.round(estRevenueUSD * 100) / 100,
        commissionRate: 5,
        leadsByCategory: Object.entries(leadsByCategory).map(([name, value]) => ({ name, value })),
        leadsByType
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
