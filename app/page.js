'use client'

import { useEffect, useState, useCallback } from 'react'
import {
  Search, MapPin, Menu, X, Compass, Bus, Plane, Car, Hotel, Mountain,
  Binoculars, Building2, Phone, ShieldCheck, TrendingUp, Percent, Users,
  Leaf, Sparkles, ArrowRight, Trash2, Plus, Loader2, MessageCircle, Tag
} from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '@/components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Toaster } from '@/components/ui/sonner'
import { toast } from 'sonner'
import {
  BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer
} from 'recharts'

const HERO = 'https://images.unsplash.com/photo-1516026672322-bc52d61a55d5?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1OTV8MHwxfHNlYXJjaHw0fHxBZnJpY2FuJTIwc2FmYXJpfGVufDB8fHx8MTc4MzM4MjA2Nnww&ixlib=rb-4.1.0&q=85'
const LOCAL_HERO = 'https://images.unsplash.com/photo-1770283553885-bad1d6f7acd7?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzR8MHwxfHNlYXJjaHwxfHxtYXRhdHUlMjBidXN8ZW58MHx8fHwxNzgzMzgyMDc4fDA&ixlib=rb-4.1.0&q=85'

const NAV = [
  { key: 'home', label: 'Home' },
  { key: 'safari', label: 'Safari' },
  { key: 'local', label: 'Local Transit' },
  { key: 'about', label: 'About' },
  { key: 'dashboard', label: 'Dashboard' },
  { key: 'admin', label: 'Admin' },
]

const SAFARI_CATS = ['All', 'Safari Package', 'Kilimanjaro Climb', 'Hotel & Resort', 'Car & Caravan Hire', 'Light Aircraft Charter', 'Sightseeing']
const LOCAL_CATS = ['All', 'Matatu / Shuttle', 'Train (SGR)', 'Taxi / Car Hire', 'Airport Transfer']
const CHART_COLORS = ['#f97316', '#1e3a8a', '#3b82f6', '#10b981', '#eab308', '#8b5cf6', '#ef4444']

const catIcon = (cat) => {
  if (/kilimanjaro/i.test(cat)) return <Mountain className="h-4 w-4" />
  if (/hotel|resort/i.test(cat)) return <Hotel className="h-4 w-4" />
  if (/car|caravan/i.test(cat)) return <Car className="h-4 w-4" />
  if (/aircraft/i.test(cat)) return <Plane className="h-4 w-4" />
  if (/sightseeing/i.test(cat)) return <Binoculars className="h-4 w-4" />
  if (/train/i.test(cat)) return <Bus className="h-4 w-4" />
  if (/taxi/i.test(cat)) return <Car className="h-4 w-4" />
  if (/matatu|shuttle/i.test(cat)) return <Bus className="h-4 w-4" />
  if (/airport/i.test(cat)) return <Plane className="h-4 w-4" />
  return <Compass className="h-4 w-4" />
}

// ---------------------------------------------------------------------------
// Listing card
// ---------------------------------------------------------------------------
function ListingCard({ item, onBook, booking }) {
  const accent = item.type === 'safari' ? '#f97316' : '#1e3a8a'
  return (
    <Card className="overflow-hidden border-slate-200 hover:shadow-xl transition-shadow duration-300 flex flex-col">
      <div className="relative h-52 w-full overflow-hidden">
        <img src={item.image} alt={item.title} className="h-full w-full object-cover transition-transform duration-500 hover:scale-105" />
        <Badge className="absolute left-3 top-3 gap-1 border-0 text-white shadow" style={{ backgroundColor: accent }}>
          {catIcon(item.category)} {item.category}
        </Badge>
        {item.offPeakLabel ? (
          <Badge className="absolute right-3 top-3 gap-1 bg-emerald-600 text-white border-0 shadow">
            <Tag className="h-3 w-3" /> Off-peak {item.offPeakLabel}
          </Badge>
        ) : null}
      </div>
      <CardContent className="flex flex-1 flex-col p-5">
        <h3 className="text-lg font-bold text-slate-900 leading-snug">{item.title}</h3>
        <p className="mt-1 text-sm font-semibold" style={{ color: accent }}>By {item.vendor}</p>
        <a href={item.mapLink} target="_blank" rel="noopener noreferrer" className="mt-1 flex items-center gap-1 text-xs text-slate-500 hover:text-slate-700">
          <MapPin className="h-3 w-3" /> {item.location}
        </a>
        <p className="mt-3 text-sm text-slate-600 line-clamp-3">{item.description}</p>

        {item.includes?.length ? (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {item.includes.slice(0, 4).map((inc, i) => (
              <span key={i} className="rounded-full bg-slate-100 px-2.5 py-0.5 text-[11px] font-medium text-slate-600">{inc}</span>
            ))}
          </div>
        ) : null}

        <div className="mt-4 flex items-end justify-between border-t border-slate-100 pt-3">
          <div>
            <p className="text-2xl font-extrabold text-emerald-600">{item.priceLabel}</p>
            {item.season ? <p className="text-[11px] text-slate-400">{item.season}</p> : null}
          </div>
          <p className="flex items-center gap-1 text-[11px] text-slate-400"><Building2 className="h-3 w-3" /> {item.vendorOffice}</p>
        </div>

        <Button
          onClick={() => onBook(item)}
          disabled={booking === item.id}
          className="mt-4 w-full gap-2 bg-[#25d366] text-white hover:bg-[#1ebe5b]"
        >
          {booking === item.id ? <Loader2 className="h-4 w-4 animate-spin" /> : <MessageCircle className="h-4 w-4" />}
          Book via WhatsApp
        </Button>
      </CardContent>
    </Card>
  )
}

// ---------------------------------------------------------------------------
// Search + results section (shared by Safari & Local)
// ---------------------------------------------------------------------------
function TierExplorer({ type }) {
  const isSafari = type === 'safari'
  const cats = isSafari ? SAFARI_CATS : LOCAL_CATS
  const accent = isSafari ? '#f97316' : '#1e3a8a'
  const [q, setQ] = useState('')
  const [cat, setCat] = useState('All')
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [booking, setBooking] = useState(null)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams({ type })
      if (q) params.set('q', q)
      if (cat && cat !== 'All') params.set('category', cat)
      const res = await fetch(`/api/listings?${params.toString()}`)
      const data = await res.json()
      setItems(Array.isArray(data) ? data : [])
    } catch (e) {
      toast.error('Failed to load listings')
    } finally {
      setLoading(false)
    }
  }, [type, q, cat])

  useEffect(() => { load() }, [cat]) // eslint-disable-line

  useEffect(() => { load() }, []) // eslint-disable-line

  const handleBook = async (item) => {
    setBooking(item.id)
    try {
      const res = await fetch('/api/leads', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ listingId: item.id })
      })
      const data = await res.json()
      toast.success('Opening WhatsApp to complete your booking...')
      window.open(data.whatsappUrl, '_blank')
    } catch (e) {
      toast.error('Could not start booking')
    } finally {
      setBooking(null)
    }
  }

  return (
    <div>
      {/* Banner */}
      <div className="relative h-64 w-full overflow-hidden">
        <img src={isSafari ? HERO : LOCAL_HERO} alt="banner" className="h-full w-full object-cover" />
        <div className="absolute inset-0" style={{ background: isSafari ? 'linear-gradient(135deg, rgba(249,115,22,.85), rgba(30,58,138,.7))' : 'linear-gradient(135deg, rgba(30,58,138,.9), rgba(59,130,246,.75))' }} />
        <div className="absolute inset-0 mx-auto flex max-w-5xl flex-col justify-center px-5 text-white">
          <h1 className="text-3xl font-extrabold md:text-4xl">{isSafari ? 'Tourist Assistance — East Africa' : 'Local Commute — Nairobi & Beyond'}</h1>
          <p className="mt-2 max-w-2xl text-white/90">{isSafari ? 'Safaris, Kilimanjaro climbs, hotels, car & aircraft hire — compare and book instantly.' : 'Compare matatus, SGR trains, taxis & airport shuttles across Nairobi CBD and its environs.'}</p>
        </div>
      </div>

      {/* Search bar */}
      <div className="mx-auto -mt-8 max-w-4xl px-5">
        <Card className="border-slate-200 shadow-lg">
          <CardContent className="flex flex-col gap-3 p-4 md:flex-row md:items-center">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
              <Input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && load()}
                placeholder={isSafari ? 'e.g. Mara safari, Kilimanjaro, car hire, Zanzibar...' : 'e.g. SGR train, matatu, taxi, airport...'}
                className="h-12 pl-10 text-base"
              />
            </div>
            <Select value={cat} onValueChange={setCat}>
              <SelectTrigger className="h-12 md:w-56"><SelectValue placeholder="Category" /></SelectTrigger>
              <SelectContent>
                {cats.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}
              </SelectContent>
            </Select>
            <Button onClick={load} className="h-12 gap-2 px-6 text-white" style={{ backgroundColor: accent }}>
              <Search className="h-4 w-4" /> Search
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Results */}
      <div className="mx-auto max-w-7xl px-5 py-10">
        <div className="mb-5 flex items-center justify-between">
          <p className="text-sm text-slate-500">{loading ? 'Searching…' : `${items.length} option${items.length === 1 ? '' : 's'} found`}</p>
        </div>
        {loading ? (
          <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin text-slate-400" /></div>
        ) : items.length === 0 ? (
          <div className="rounded-xl border border-dashed border-slate-300 py-20 text-center text-slate-500">
            No matches found. Try broader terms like {isSafari ? '"safari", "beach", "hotel"' : '"train", "taxi", "matatu"'}.
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {items.map((item) => <ListingCard key={item.id} item={item} onBook={handleBook} booking={booking} />)}
          </div>
        )}
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Home
// ---------------------------------------------------------------------------
function Home({ go }) {
  const [q, setQ] = useState('')
  const [tier, setTier] = useState('safari')

  const search = () => {
    go(tier, q)
  }

  return (
    <div>
      {/* Hero */}
      <div className="relative min-h-[560px] w-full overflow-hidden">
        <img src={HERO} alt="hero" className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-br from-[#1e3a8a]/85 via-[#1e3a8a]/60 to-[#f97316]/70" />
        <div className="relative mx-auto flex max-w-5xl flex-col items-center px-5 py-24 text-center text-white">
          <Badge className="mb-4 gap-1 border-white/30 bg-white/15 text-white backdrop-blur">
            <Sparkles className="h-3 w-3" /> Free information assistant • Book direct
          </Badge>
          <h1 className="text-4xl font-extrabold leading-tight md:text-6xl">
            OSARE — East Africa<br className="hidden md:block" /> Safari Routes & Transit
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-white/90">
            Everything a tourist or local needs at their fingertips. Compare safaris, Kilimanjaro climbs, hotels, car & aircraft hire — and Nairobi transit — then book direct. What you see is what you get.
          </p>

          {/* Tier toggle + search */}
          <div className="mt-8 w-full max-w-2xl">
            <div className="mb-3 flex justify-center gap-3">
              <button onClick={() => setTier('safari')} className={`rounded-full px-6 py-2 text-sm font-bold transition ${tier === 'safari' ? 'bg-[#f97316] text-white' : 'bg-white/20 text-white hover:bg-white/30'}`}>Tourist Assistance</button>
              <button onClick={() => setTier('local')} className={`rounded-full px-6 py-2 text-sm font-bold transition ${tier === 'local' ? 'bg-white text-[#1e3a8a]' : 'bg-white/20 text-white hover:bg-white/30'}`}>Local Commute</button>
            </div>
            <div className="flex gap-2 rounded-2xl bg-white p-2 shadow-2xl">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-slate-400" />
                <Input
                  value={q}
                  onChange={(e) => setQ(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && search()}
                  placeholder={tier === 'safari' ? 'Mara migration, Kilimanjaro, Zanzibar, car hire…' : 'Nairobi to Mombasa, matatu, taxi, SGR…'}
                  className="h-12 border-0 pl-10 text-base text-slate-900 focus-visible:ring-0"
                />
              </div>
              <Button onClick={search} className="h-12 gap-2 px-6 text-white" style={{ backgroundColor: tier === 'safari' ? '#f97316' : '#1e3a8a' }}>
                Search <ArrowRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Two tiers */}
      <div className="mx-auto max-w-6xl px-5 py-16">
        <h2 className="text-center text-3xl font-extrabold text-slate-900">Two platforms. One trusted hub.</h2>
        <p className="mt-2 text-center text-slate-500">Choose your journey.</p>
        <div className="mt-10 grid gap-6 md:grid-cols-2">
          <button onClick={() => go('safari')} className="group relative h-72 overflow-hidden rounded-2xl text-left shadow-lg">
            <img src={HERO} alt="safari" className="absolute inset-0 h-full w-full object-cover transition-transform duration-500 group-hover:scale-105" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
            <div className="absolute bottom-0 p-6 text-white">
              <Badge className="mb-2 gap-1 border-0 bg-[#f97316] text-white"><Compass className="h-3 w-3" /> Tier 1</Badge>
              <h3 className="text-2xl font-bold">Safari & Tourism</h3>
              <p className="mt-1 text-sm text-white/85">Mara migration, Kilimanjaro, hotels, car & aircraft hire, sightseeing.</p>
              <span className="mt-3 inline-flex items-center gap-1 text-sm font-semibold text-orange-300">Explore safaris <ArrowRight className="h-4 w-4" /></span>
            </div>
          </button>
          <button onClick={() => go('local')} className="group relative h-72 overflow-hidden rounded-2xl text-left shadow-lg">
            <img src={LOCAL_HERO} alt="local" className="absolute inset-0 h-full w-full object-cover transition-transform duration-500 group-hover:scale-105" />
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent" />
            <div className="absolute bottom-0 p-6 text-white">
              <Badge className="mb-2 gap-1 border-0 bg-[#1e3a8a] text-white"><Bus className="h-3 w-3" /> Tier 2</Badge>
              <h3 className="text-2xl font-bold">Local Commute</h3>
              <p className="mt-1 text-sm text-white/85">Nairobi CBD transit: matatus, SGR trains, taxis & airport shuttles.</p>
              <span className="mt-3 inline-flex items-center gap-1 text-sm font-semibold text-blue-300">Find transit <ArrowRight className="h-4 w-4" /></span>
            </div>
          </button>
        </div>
      </div>

      {/* Value props */}
      <div className="bg-slate-50 py-16">
        <div className="mx-auto max-w-6xl px-5">
          <h2 className="text-center text-3xl font-extrabold text-slate-900">Why OSARE</h2>
          <div className="mt-10 grid gap-6 md:grid-cols-4">
            {[
              { icon: <ShieldCheck className="h-6 w-6" />, t: 'Trusted vendors', d: 'Verified operators with office & location shown.' },
              { icon: <Percent className="h-6 w-6" />, t: 'Free for tourists', d: 'You pay nothing extra. Vendors pay us 5%, not you.' },
              { icon: <TrendingUp className="h-6 w-6" />, t: 'Off-peak prices', d: 'Low-season deals surfaced automatically.' },
              { icon: <MessageCircle className="h-6 w-6" />, t: 'Book on WhatsApp', d: 'One tap to reach the vendor and confirm.' },
            ].map((f, i) => (
              <Card key={i} className="border-slate-200">
                <CardContent className="p-6">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#f97316]/10 text-[#f97316]">{f.icon}</div>
                  <h3 className="mt-4 font-bold text-slate-900">{f.t}</h3>
                  <p className="mt-1 text-sm text-slate-500">{f.d}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

// ---------------------------------------------------------------------------
// About
// ---------------------------------------------------------------------------
function About() {
  return (
    <div className="mx-auto max-w-4xl px-5 py-16">
      <Badge className="gap-1 bg-[#f97316] text-white border-0"><Leaf className="h-3 w-3" /> About OSARE</Badge>
      <h1 className="mt-4 text-4xl font-extrabold text-slate-900">Organising East Africa tourism with trusted information.</h1>
      <p className="mt-4 text-lg text-slate-600">
        OSARE is a two-tier information & booking hub. Tier 1 serves tourists with safaris, Kilimanjaro climbs, hotels, car & aircraft hire and sightseeing. Tier 2 serves locals with Nairobi CBD transit information. Our goal: put reliable, trustworthy information at everyone's fingertips.
      </p>

      <div className="mt-10 grid gap-6 md:grid-cols-3">
        <Card className="border-slate-200"><CardContent className="p-6"><Users className="h-7 w-7 text-[#1e3a8a]" /><h3 className="mt-3 font-bold">For tourists</h3><p className="mt-1 text-sm text-slate-500">Compare options with photos, prices and off-peak deals. Book direct via WhatsApp.</p></CardContent></Card>
        <Card className="border-slate-200"><CardContent className="p-6"><Building2 className="h-7 w-7 text-[#1e3a8a]" /><h3 className="mt-3 font-bold">For vendors</h3><p className="mt-1 text-sm text-slate-500">Reach travellers directly. We charge a simple 5% on confirmed bookings.</p></CardContent></Card>
        <Card className="border-slate-200"><CardContent className="p-6"><Percent className="h-7 w-7 text-emerald-600" /><h3 className="mt-3 font-bold">Our revenue</h3><p className="mt-1 text-sm text-slate-500">5% commission paid by vendors — never by the tourist. Fair and transparent.</p></CardContent></Card>
      </div>

      <Card className="mt-10 border-slate-200 bg-slate-50">
        <CardContent className="p-6">
          <h3 className="font-bold text-slate-900">Contact & booking</h3>
          <p className="mt-2 flex items-center gap-2 text-slate-600"><Phone className="h-4 w-4 text-[#25d366]" /> WhatsApp bookings: +254 758 378 729</p>
          <p className="mt-1 flex items-center gap-2 text-slate-600"><MapPin className="h-4 w-4 text-[#1e3a8a]" /> Nairobi CBD, Kenya</p>
        </CardContent>
      </Card>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Dashboard
// ---------------------------------------------------------------------------
function Dashboard() {
  const [stats, setStats] = useState(null)
  const [leads, setLeads] = useState([])
  const [loading, setLoading] = useState(true)

  const load = async () => {
    setLoading(true)
    try {
      const [s, l] = await Promise.all([
        fetch('/api/stats').then((r) => r.json()),
        fetch('/api/leads').then((r) => r.json()),
      ])
      setStats(s)
      setLeads(Array.isArray(l) ? l : [])
    } catch (e) {
      toast.error('Failed to load dashboard')
    } finally {
      setLoading(false)
    }
  }
  useEffect(() => { load() }, [])

  if (loading || !stats) return <div className="flex justify-center py-24"><Loader2 className="h-8 w-8 animate-spin text-slate-400" /></div>

  const cards = [
    { label: 'Total Listings', value: stats.totalListings, icon: <Compass className="h-5 w-5" />, color: '#1e3a8a' },
    { label: 'Booking Leads', value: stats.totalLeads, icon: <MessageCircle className="h-5 w-5" />, color: '#f97316' },
    { label: 'Est. Commission (5%)', value: `$${stats.estRevenueUSD}`, icon: <Percent className="h-5 w-5" />, color: '#10b981' },
    { label: 'Safari / Local', value: `${stats.safariCount} / ${stats.localCount}`, icon: <Users className="h-5 w-5" />, color: '#3b82f6' },
  ]

  return (
    <div className="mx-auto max-w-6xl px-5 py-12">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900">Vendor Revenue Dashboard</h1>
          <p className="text-slate-500">Track booking leads and estimated 5% commission revenue.</p>
        </div>
        <Button variant="outline" onClick={load}>Refresh</Button>
      </div>

      <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {cards.map((c, i) => (
          <Card key={i} className="border-slate-200">
            <CardContent className="p-5">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-500">{c.label}</span>
                <span className="flex h-9 w-9 items-center justify-center rounded-lg text-white" style={{ backgroundColor: c.color }}>{c.icon}</span>
              </div>
              <p className="mt-3 text-3xl font-extrabold text-slate-900">{c.value}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <Card className="border-slate-200">
          <CardHeader><CardTitle className="text-base">Leads by category</CardTitle></CardHeader>
          <CardContent className="h-72">
            {stats.leadsByCategory?.length ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={stats.leadsByCategory}>
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} interval={0} angle={-15} textAnchor="end" height={60} />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                    {stats.leadsByCategory.map((e, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : <EmptyChart />}
          </CardContent>
        </Card>

        <Card className="border-slate-200">
          <CardHeader><CardTitle className="text-base">Safari vs Local leads</CardTitle></CardHeader>
          <CardContent className="h-72">
            {stats.totalLeads ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={[{ name: 'Safari', value: stats.leadsByType.safari }, { name: 'Local', value: stats.leadsByType.local }]}
                    dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label
                  >
                    <Cell fill="#f97316" />
                    <Cell fill="#1e3a8a" />
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : <EmptyChart />}
          </CardContent>
        </Card>
      </div>

      <Card className="mt-8 border-slate-200">
        <CardHeader><CardTitle className="text-base">Recent booking leads</CardTitle></CardHeader>
        <CardContent>
          {leads.length === 0 ? (
            <p className="py-8 text-center text-slate-400">No booking leads yet. Book a listing to see it here.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Listing</TableHead>
                  <TableHead>Vendor</TableHead>
                  <TableHead>Price</TableHead>
                  <TableHead className="text-right">Est. 5%</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {leads.slice(0, 15).map((l) => (
                  <TableRow key={l.id}>
                    <TableCell className="font-medium">{l.listingTitle}</TableCell>
                    <TableCell className="text-slate-500">{l.vendor}</TableCell>
                    <TableCell>{l.priceLabel}</TableCell>
                    <TableCell className="text-right font-semibold text-emerald-600">{l.currency === 'KES' ? `KES ${Math.round(l.priceValue * 0.05)}` : `$${l.commission}`}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

function EmptyChart() {
  return <div className="flex h-full items-center justify-center text-sm text-slate-400">No lead data yet</div>
}

// ---------------------------------------------------------------------------
// Admin
// ---------------------------------------------------------------------------
const EMPTY_FORM = {
  type: 'safari', category: 'Safari Package', title: '', vendor: '', vendorOffice: '',
  location: '', mapLink: '', description: '', includes: '', priceValue: '', currency: 'USD',
  priceLabel: '', offPeakValue: '', offPeakLabel: '', season: '', image: '', keywords: ''
}

function Admin() {
  const [listings, setListings] = useState([])
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [seeding, setSeeding] = useState(false)

  const load = async () => {
    const data = await fetch('/api/listings').then((r) => r.json())
    setListings(Array.isArray(data) ? data : [])
  }
  useEffect(() => { load() }, [])

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }))

  const submit = async () => {
    if (!form.title) { toast.error('Title is required'); return }
    setSaving(true)
    try {
      await fetch('/api/listings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form)
      })
      toast.success('Listing added')
      setForm(EMPTY_FORM)
      load()
    } catch (e) { toast.error('Failed to add listing') }
    finally { setSaving(false) }
  }

  const remove = async (id) => {
    await fetch(`/api/listings/${id}`, { method: 'DELETE' })
    toast.success('Listing removed')
    load()
  }

  const seed = async () => {
    setSeeding(true)
    try {
      const res = await fetch('/api/seed', { method: 'POST' })
      const data = await res.json()
      toast.success(`Seeded ${data.inserted} sample listings`)
      load()
    } catch (e) { toast.error('Seed failed') }
    finally { setSeeding(false) }
  }

  const cats = form.type === 'safari' ? SAFARI_CATS.filter((c) => c !== 'All') : LOCAL_CATS.filter((c) => c !== 'All')

  return (
    <div className="mx-auto max-w-6xl px-5 py-12">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900">Admin — Manage Listings</h1>
          <p className="text-slate-500">Add vendor listings for the Safari or Local tiers.</p>
        </div>
        <Button variant="outline" onClick={seed} disabled={seeding} className="gap-2">
          {seeding ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />} Reset & load sample data
        </Button>
      </div>

      <div className="mt-8 grid gap-8 lg:grid-cols-5">
        {/* Form */}
        <Card className="border-slate-200 lg:col-span-2">
          <CardHeader><CardTitle className="text-base">Add a listing</CardTitle></CardHeader>
          <CardContent className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <Label className="text-xs">Tier</Label>
                <Select value={form.type} onValueChange={(v) => { set('type', v); set('category', (v === 'safari' ? SAFARI_CATS : LOCAL_CATS)[1]) }}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="safari">Safari / Tourism</SelectItem>
                    <SelectItem value="local">Local Transit</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label className="text-xs">Category</Label>
                <Select value={form.category} onValueChange={(v) => set('category', v)}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>{cats.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
                </Select>
              </div>
            </div>
            <Field label="Title" v={form.title} on={(v) => set('title', v)} />
            <Field label="Vendor" v={form.vendor} on={(v) => set('vendor', v)} />
            <Field label="Vendor office" v={form.vendorOffice} on={(v) => set('vendorOffice', v)} />
            <Field label="Location" v={form.location} on={(v) => set('location', v)} />
            <Field label="Map link" v={form.mapLink} on={(v) => set('mapLink', v)} />
            <div>
              <Label className="text-xs">Description</Label>
              <Textarea value={form.description} onChange={(e) => set('description', e.target.value)} rows={3} />
            </div>
            <Field label="Includes (comma separated)" v={form.includes} on={(v) => set('includes', v)} />
            <div className="grid grid-cols-2 gap-3">
              <Field label="Price value (number)" v={form.priceValue} on={(v) => set('priceValue', v)} />
              <div>
                <Label className="text-xs">Currency</Label>
                <Select value={form.currency} onValueChange={(v) => set('currency', v)}>
                  <SelectTrigger><SelectValue /></SelectTrigger>
                  <SelectContent>
                    <SelectItem value="USD">USD ($)</SelectItem>
                    <SelectItem value="KES">KES</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <Field label="Price label" v={form.priceLabel} on={(v) => set('priceLabel', v)} ph="$350" />
              <Field label="Off-peak label" v={form.offPeakLabel} on={(v) => set('offPeakLabel', v)} ph="$280" />
            </div>
            <Field label="Season note" v={form.season} on={(v) => set('season', v)} ph="Low season: Apr-Jun" />
            <Field label="Image URL" v={form.image} on={(v) => set('image', v)} />
            <Field label="Keywords (comma separated)" v={form.keywords} on={(v) => set('keywords', v)} />
            <Button onClick={submit} disabled={saving} className="w-full gap-2 bg-[#1e3a8a] text-white hover:bg-[#1e40af]">
              {saving ? <Loader2 className="h-4 w-4 animate-spin" /> : <Plus className="h-4 w-4" />} Add listing
            </Button>
          </CardContent>
        </Card>

        {/* Table */}
        <Card className="border-slate-200 lg:col-span-3">
          <CardHeader><CardTitle className="text-base">All listings ({listings.length})</CardTitle></CardHeader>
          <CardContent>
            <div className="max-h-[640px] overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Title</TableHead>
                    <TableHead>Tier</TableHead>
                    <TableHead>Price</TableHead>
                    <TableHead></TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {listings.map((l) => (
                    <TableRow key={l.id}>
                      <TableCell>
                        <p className="font-medium">{l.title}</p>
                        <p className="text-xs text-slate-400">{l.vendor}</p>
                      </TableCell>
                      <TableCell>
                        <Badge variant="secondary" className={l.type === 'safari' ? 'bg-orange-100 text-orange-700' : 'bg-blue-100 text-blue-700'}>{l.type}</Badge>
                      </TableCell>
                      <TableCell className="text-sm">{l.priceLabel}</TableCell>
                      <TableCell className="text-right">
                        <Button size="icon" variant="ghost" onClick={() => remove(l.id)} className="text-red-500 hover:text-red-700">
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              {listings.length === 0 && <p className="py-10 text-center text-slate-400">No listings yet. Click "Reset & load sample data".</p>}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

function Field({ label, v, on, ph }) {
  return (
    <div>
      <Label className="text-xs">{label}</Label>
      <Input value={v} onChange={(e) => on(e.target.value)} placeholder={ph} />
    </div>
  )
}

// ---------------------------------------------------------------------------
// Root App
// ---------------------------------------------------------------------------
function App() {
  const [view, setView] = useState('home')
  const [mobileOpen, setMobileOpen] = useState(false)
  const [pendingQuery, setPendingQuery] = useState('')

  // Seed on first load if empty
  useEffect(() => {
    fetch('/api/listings').then((r) => r.json()).then((data) => {
      if (!Array.isArray(data) || data.length === 0) {
        fetch('/api/seed', { method: 'POST' })
      }
    }).catch(() => {})
  }, [])

  const go = (v, query = '') => {
    setPendingQuery(query)
    setView(v)
    setMobileOpen(false)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  return (
    <div className="min-h-screen bg-white">
      <Toaster position="top-center" richColors />

      {/* Nav */}
      <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-3">
          <button onClick={() => go('home')} className="flex items-center gap-2">
            <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-[#1e3a8a] to-[#f97316] text-white"><Compass className="h-5 w-5" /></span>
            <span className="text-xl font-extrabold tracking-tight text-slate-900">OSARE</span>
          </button>

          <nav className="hidden items-center gap-1 md:flex">
            {NAV.map((n) => (
              <button
                key={n.key}
                onClick={() => go(n.key)}
                className={`rounded-lg px-3 py-2 text-sm font-medium transition ${view === n.key ? 'bg-slate-900 text-white' : 'text-slate-600 hover:bg-slate-100'}`}
              >
                {n.label}
              </button>
            ))}
          </nav>

          <div className="hidden md:block">
            <Button onClick={() => go('safari')} className="gap-2 bg-[#f97316] text-white hover:bg-[#ea6c0f]">
              Explore <ArrowRight className="h-4 w-4" />
            </Button>
          </div>

          <button className="md:hidden" onClick={() => setMobileOpen((o) => !o)}>
            {mobileOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
          </button>
        </div>
        {mobileOpen && (
          <div className="border-t border-slate-200 bg-white md:hidden">
            {NAV.map((n) => (
              <button key={n.key} onClick={() => go(n.key)} className={`block w-full px-5 py-3 text-left text-sm font-medium ${view === n.key ? 'bg-slate-100 text-slate-900' : 'text-slate-600'}`}>
                {n.label}
              </button>
            ))}
          </div>
        )}
      </header>

      {/* Views */}
      {view === 'home' && <Home go={go} />}
      {view === 'safari' && <TierExplorer type="safari" key={'safari' + pendingQuery} />}
      {view === 'local' && <TierExplorer type="local" key={'local' + pendingQuery} />}
      {view === 'about' && <About />}
      {view === 'dashboard' && <Dashboard />}
      {view === 'admin' && <Admin />}

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-slate-900 py-10 text-slate-300">
        <div className="mx-auto grid max-w-7xl gap-8 px-5 md:grid-cols-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-[#1e3a8a] to-[#f97316] text-white"><Compass className="h-4 w-4" /></span>
              <span className="text-lg font-extrabold text-white">OSARE</span>
            </div>
            <p className="mt-3 text-sm text-slate-400">East Africa Safari Routes & Transit Hub. Free information for tourists & locals.</p>
          </div>
          <div>
            <h4 className="font-semibold text-white">Platform</h4>
            <ul className="mt-3 space-y-2 text-sm">
              <li><button onClick={() => go('safari')} className="hover:text-white">Safari & Tourism</button></li>
              <li><button onClick={() => go('local')} className="hover:text-white">Local Commute</button></li>
              <li><button onClick={() => go('about')} className="hover:text-white">About</button></li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-white">Vendors</h4>
            <ul className="mt-3 space-y-2 text-sm">
              <li><button onClick={() => go('admin')} className="hover:text-white">Add a listing</button></li>
              <li><button onClick={() => go('dashboard')} className="hover:text-white">Revenue dashboard</button></li>
              <li className="text-slate-400">Only 5% on bookings</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold text-white">Contact</h4>
            <ul className="mt-3 space-y-2 text-sm text-slate-400">
              <li className="flex items-center gap-2"><Phone className="h-4 w-4 text-[#25d366]" /> +254 758 378 729</li>
              <li className="flex items-center gap-2"><MapPin className="h-4 w-4" /> Nairobi CBD, Kenya</li>
            </ul>
          </div>
        </div>
        <p className="mt-8 text-center text-xs text-slate-500">© 2025 OSARE — easafariroutes.com. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App
