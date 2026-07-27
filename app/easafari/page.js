"use client"

import { useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Search, Compass, MapPin, Clock } from "lucide-react"

export default function EAsafariPage() {
  const [query, setQuery] = useState("")
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    
    // Fetch all safari routes if query is empty, or filter if typed
    const searchUrl = query.trim() 
      ? `http://localhost:10000/api/search?q=${encodeURIComponent(query.trim())}&category=safari`
      : `http://localhost:10000/api/search?category=safari`

    setLoading(true)
    setHasSearched(true)

    try {
      const res = await fetch(searchUrl)
      if (!res.ok) throw new Error("Server error")
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
      
      <h1 className="text-4xl font-bold mb-2">🦁 EAsafari Routes</h1>
      <p className="text-muted-foreground mb-6">Regional tourism, wildlife safaris, SGR rail, and long-distance travel.</p>

      {/* Interactive Search Form */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 w-5 h-5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search tourism routes (e.g. Masai Mara, Amboseli, Diani, SGR, Kampala)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-600 bg-background"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-emerald-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-emerald-700 disabled:opacity-50 cursor-pointer"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {/* Results Section */}
      {hasSearched && (
        <div className="mb-8 space-y-4">
          <h2 className="text-xl font-semibold">Tourism & Safari Results</h2>
          {routes.length === 0 ? (
            <p className="text-muted-foreground">No safari routes found for "{query}".</p>
          ) : (
            routes.map((route) => (
              <Card key={route.id} className="border-l-4 border-l-emerald-600">
                <CardContent className="pt-6 flex justify-between items-center">
                  <div>
                    <span className="text-xs font-semibold uppercase px-2 py-1 bg-emerald-100 text-emerald-800 rounded">
                      {route.operator}
                    </span>
                    <h3 className="text-lg font-bold mt-1 flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-emerald-600" />
                      {route.origin} → {route.destination}
                    </h3>
                    <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                      <Clock className="w-3.5 h-3.5" /> Schedule: {route.time}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-bold text-emerald-700">{route.price}</span>
                    {route.info && <p className="text-xs text-muted-foreground mt-1">{route.info}</p>}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}

      {/* Major Regional Tourism Corridors Overview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Compass className="w-5 h-5 text-emerald-600" /> Major Regional Tourism Corridors
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <p>• <strong>Masai Mara Circuit:</strong> 4x4 Tour Land Cruisers & Air Charters from Nairobi/JKIA</p>
          <p>• <strong>Amboseli & Tsavo:</strong> Overland Wildlife Shuttles & Game Park Transfers</p>
          <p>• <strong>Coastal Tourist Hubs:</strong> SGR Madaraka Express to Mombasa, Diani & Watamu Transfers</p>
          <p>• <strong>Cross-Border Transit:</strong> Luxury Executive Coaches to Arusha, Namanga & Kampala</p>
        </CardContent>
      </Card>
    </main>
  )
}
