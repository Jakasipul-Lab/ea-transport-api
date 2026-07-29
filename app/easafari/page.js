"use client"

import { useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Search, Compass, MapPin, Clock } from "lucide-react"

export default function SafarioutesPage() {
  const [query, setQuery] = useState("")
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()

  const searchUrl = query.trim()
  ? `http://172.31.234.106:8000/search?q=${encodeURIComponent(query.trim())}&category=safari`
  : `http://172.31.234.106:8000/search?category=safari`

    setLoading(true)
    setHasSearched(true)

    try {
      const res = await fetch(searchUrl)

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`)
      }

      const data = await res.json()
      setRoutes(data || [])
    } catch (error) {
      console.error("Failed to fetch safari routes:", error)
      setRoutes([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-12 max-w-4xl">
      / className="flex items-center gap-2 text-sm mb-6 hover:underline text-muted-foreground"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Home
      </Link>

      <h1 className="text-4xl font-bold mb-2 text-emerald-800">
        🦁 Safari Routes: Regional & Tourism Hub
      </h1>

      <p className="text-muted-foreground mb-6">
        Long-distance travel, wildlife safaris, SGR express rail, and cross-border coaches.
      </p>

      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 w-5 h-5 text-emerald-600" />

          <input
            type="text"
            placeholder="Search Safari Routes (Masai Mara, Amboseli, Mombasa, Kampala...)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border rounded-lg bg-background"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="bg-emerald-600 text-white px-6 py-2 rounded-lg hover:bg-emerald-700 disabled:opacity-50"
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </form>

      {hasSearched && (
        <div className="mb-8 space-y-4">
          <h2 className="text-xl font-semibold text-emerald-900">
            Safari Results
          </h2>

          {routes.length === 0 ? (
            <p className="text-muted-foreground">
              No routes found.
            </p>
          ) : (
            routes.map((route) => (
              <Card
                key={route.id}
                className="border-l-4 border-l-emerald-600"
              >
                <CardContent className="pt-6 flex justify-between items-center">
                  <div>
                    <span className="text-xs font-semibold uppercase px-2 py-1 bg-emerald-100 text-emerald-800 rounded">
                      {route.operator}
                    </span>

                    <h3 className="text-lg font-bold mt-2 flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-emerald-600" />
                      {route.origin} → {route.destination}
                    </h3>

                    <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                      <Clock className="w-3 h-3" />
                      Departure: {route.time}
                    </p>
                  </div>

                  <div className="text-right">
                    <span className="text-lg font-bold text-emerald-700">
                      {route.price}
                    </span>

                    {route.info && (
                      <p className="text-xs text-muted-foreground mt-1">
                        {route.info}
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-emerald-800">
            <Compass className="w-5 h-5 text-emerald-600" />
            Major Tourism Corridors
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-3 text-sm">
          <p>
            • <strong>Masai Mara Circuit:</strong> 4x4 safari transfers and air charters from Nairobi.
          </p>

          <p>
            • <strong>Amboseli & Tsavo:</strong> Wildlife safari and lodge transfers.
          </p>

          <p>
            • <strong>Coastal Tourism:</strong> SGR services to Mombasa with Diani and Watamu connections.
          </p>

          <p>
            • <strong>Cross-Border Travel:</strong> Coaches to Arusha, Namanga, Kigali and Kampala.
          </p>
        </CardContent>
      </Card>
    
