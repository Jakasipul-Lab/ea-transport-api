"use client"

import { useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Search, Train, MapPin, Clock } from "lucide-react"

export default function EAsafariPage() {
  const [query, setQuery] = useState("")
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    setHasSearched(true)
    try {
      // Connects directly to your Python FastAPI backend on port 10000
      const res = await fetch(`http://localhost:10000/api/search?q=${encodeURIComponent(query)}&category=safari`)
      const data = await res.json()
      setRoutes(data)
    } catch (error) {
      console.error("Failed to fetch safari routes:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-12 max-w-4xl">
      <Link href="/" className="flex items-center gap-2 text-sm mb-6 hover:underline text-muted-foreground">
        <ArrowLeft className="w-4 h-4"/> Back to Home
      </Link>
      
      <h1 className="text-4xl font-bold mb-2">🚄 EAsafari Routes</h1>
      <p className="text-muted-foreground mb-6">Your gateway to comfortable long-distance travel across East Africa.</p>

      <p className="mb-8 text-sm">
        We’re here to serve you better. Find schedules, operators, and route information all in one place.{" "}
        Need assistance? <Link href="/help" className="underline font-medium text-primary">Visit our Help Page</Link>
      </p>

      {/* Interactive Search Bar connected to transport.db */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search regional route (e.g. Mombasa, Kisumu, Kampala)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-background"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-primary text-primary-foreground px-6 py-2 rounded-lg font-medium hover:opacity-90 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {/* Search Results */}
      {hasSearched && (
        <div className="mb-8 space-y-4">
          <h2 className="text-xl font-semibold">Safari & Long-Distance Results</h2>
          {routes.length === 0 ? (
            <p className="text-muted-foreground">No regional routes found for "{query}".</p>
          ) : (
            routes.map((route) => (
              <Card key={route.id} className="border-l-4 border-l-emerald-600">
                <CardContent className="pt-6 flex justify-between items-center">
                  <div>
                    <span className="text-xs font-semibold uppercase px-2 py-1 bg-emerald-100 text-emerald-800 rounded">
                      {route.operator}
                    </span>
                    <h3 className="text-lg font-bold mt-1 flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-muted-foreground" />
                      {route.origin} → {route.destination}
                    </h3>
                    <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                      <Clock className="w-3.5 h-3.5" /> Departure: {route.time}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-bold text-green-600">{route.price}</span>
                    {route.info && <p className="text-xs text-muted-foreground mt-1">{route.info}</p>}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}

      {/* Popular Routes Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Train className="w-5 h-5" /> Popular Long-Distance Routes
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <p>• <strong>Nairobi ↔ Mombasa:</strong> SGR Express/Inter-County & Highway Buses</p>
          <p>• <strong>Nairobi ↔ Kisumu:</strong> VIP Executive Buses & Express Shuttles</p>
          <p>• <strong>Nairobi ↔ Eldoret:</strong> Multi-daily Shuttles & Intercity Coaches</p>
          <p>• <strong>Nairobi ↔ Kampala:</strong> Cross-border Overnight Coaches</p>
        </CardContent>
      </Card>
    </main>
  )
}
