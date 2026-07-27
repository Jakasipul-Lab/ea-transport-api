"use client"

import { useState } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Search, Bus, MapPin, Clock } from "lucide-react"

export default function JakasipulPage() {
  const [query, setQuery] = useState("")
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState(false)
  const [hasSearched, setHasSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()

    const searchUrl = query.trim() 
      ? `http://127.0.0.1:10000/api/search?q=${encodeURIComponent(query.trim())}&category=local`
      : `http://127.0.0.1:10000/api/search?category=local`

    setLoading(true)
    setHasSearched(true)

    try {
      const res = await fetch(searchUrl)
      if (!res.ok) throw new Error("Server error")
      const data = await res.json()
      setRoutes(data)
    } catch (error) {
      console.error("Failed to fetch local routes:", error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="container mx-auto px-4 py-12 max-w-4xl">
      <Link href="/" className="flex items-center gap-2 text-sm mb-6 hover:underline text-muted-foreground">
        <ArrowLeft className="w-4 h-4"/> Back to Home
      </Link>
      
      <h1 className="text-4xl font-bold mb-2 text-blue-800">🚌 Jakasipul: Local Commuter Hub</h1>
      <p className="text-muted-foreground mb-6">City matatu routes, local town shuttles, and daily metropolitan stages.</p>

      {/* Local Commuter Search Form */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 w-5 h-5 text-blue-600" />
          <input
            type="text"
            placeholder="Search Local Commuter Stage (e.g. Rongai, Ngong, Kasarani, Likoni, Kondele)..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-600 bg-background"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 cursor-pointer"
        >
          {loading ? "Searching..." : "Search Local Routes"}
        </button>
      </form>

      {/* Results Section */}
      {hasSearched && (
        <div className="mb-8 space-y-4">
          <h2 className="text-xl font-semibold text-blue-900">Local Commuter Results</h2>
          {routes.length === 0 ? (
            <p className="text-muted-foreground">No local commuter routes found for "{query}".</p>
          ) : (
            routes.map((route) => (
              <Card key={route.id} className="border-l-4 border-l-blue-600">
                <CardContent className="pt-6 flex justify-between items-center">
                  <div>
                    <span className="text-xs font-semibold uppercase px-2 py-1 bg-blue-100 text-blue-800 rounded">
                      {route.operator}
                    </span>
                    <h3 className="text-lg font-bold mt-1 flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-blue-600" />
                      {route.origin} → {route.destination}
                    </h3>
                    <p className="text-sm text-muted-foreground flex items-center gap-1 mt-1">
                      <Clock className="w-3.5 h-3.5" /> Frequency: {route.time}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-bold text-blue-700">{route.price}</span>
                    {route.info && <p className="text-xs text-muted-foreground mt-1">{route.info}</p>}
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      )}

      {/* Local Terminals */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-blue-800">
            <Bus className="w-5 h-5 text-blue-600" /> Major Local City Terminals
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3 text-sm">
          <p>• <strong>Nairobi:</strong> Githurai, Dandora, Rongai, Ngong Road, Kasarani, Westlands</p>
          <p>• <strong>Mombasa:</strong> Likoni Ferry, Nyali, Bamburi, Changamwe, Mtongwe</p>
          <p>• <strong>Kisumu:</strong> Kibuye, Nyanza, Kondele, Mamboleo</p>
          <p>• <strong>Eldoret:</strong> Langas, Huruma, Pioneer, Maili Tisa</p>
        </CardContent>
      </Card>
    </main>
  )
}
