@app.get("/health/local")
def health_local():
    return {"status": "local ok"}

"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ArrowLeft, Search, Compass, MapPin, Bus, Tag } from "lucide-react"

const API_URL = "https://ea-transport-api.onrender.com/api/search" // <-- YOUR REAL BACKEND

export default function SafarioutesPage() {
  const [query, setQuery] = useState("")
  const [routes, setRoutes] = useState([])
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState("local") // local or safari

  // Load routes on page load
  useEffect(() => {
    fetchRoutes("", "local")
  }, [])

  const fetchRoutes = async (searchTerm, category) => {
    setLoading(true)
    setActiveTab(category)
    
    const url = searchTerm
      ? `${API_URL}?q=${encodeURIComponent(searchTerm)}&category=${category}`
      : `${API_URL}?category=${category}`

    try {
      const res = await fetch(url)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setRoutes(Array.isArray(data) ? data : [])
    } catch (error) {
      console.error("Failed to fetch routes:", error)
      setRoutes([])
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    fetchRoutes(query, activeTab)
  }

  return (
    <main className="container mx-auto px-4 py-12 max-w-4xl">
      <Link href="/" className="flex items-center gap-2 text-sm mb-6 hover:underline text-muted-foreground">
        <ArrowLeft className="w-4 h-4" />
        Back to Home
      </Link>

      <h1 className="text-4xl font-bold mb-2 text-emerald-800">
        🚌 OSARE Routes Hub
      </h1>
      <p className="text-muted-foreground mb-6">
        Local matatus, long-distance, and safari routes across Kenya.
      </p>

      {/* Tabs for Local vs Safari */}
      <div className="flex gap-2 mb-4">
        <button 
          onClick={() => fetchRoutes("", "local")} 
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${activeTab === "local" ? "bg-blue-600 text-white" : "bg-gray-200"}`}
        >
          <Bus className="w-4 h-4"/> Local Routes
        </button>
        <button 
          onClick={() => fetchRoutes("", "safari")} 
          className={`px-4 py-2 rounded-lg flex items-center gap-2 ${activeTab === "safari" ? "bg-emerald-600 text-white" : "bg-gray-200"}`}
        >
          <Compass className="w-4 h-4"/> Safari Routes
        </button>
      </div>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-3 w-5 h-5 text-emerald-600" />
          <input
            type="text"
            placeholder="Search Routes: Githurai, Mara, Mombasa..."
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

      {/* Results */}
      <div className="mb-8 space-y-4">
        <h2 className="text-xl font-semibold">
          {activeTab === "local" ? "Local" : "Safari"} Results
        </h2>

        {loading && <p>Loading...</p>}
        
        {!loading && routes.length === 0 && (
          <p className="text-muted-foreground">No routes found. Try searching "Jakasipul" or "Mara".</p>
        )}

        {!loading && routes.map((route) => (
          <Card key={route.id} className="border-l-4 border-l-emerald-600 hover:shadow-md transition">
            <CardContent className="pt-6 flex justify-between items-center">
              <div>
                <span className="text-xs font-semibold uppercase px-2 py-1 bg-emerald-100 text-emerald-800 rounded flex items-center gap-1 w-fit">
                  <Tag className="w-3 h-3"/> {route.category}
                </span>
                <h3 className="text-lg font-bold mt-2 flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-emerald-600" />
                  {route.name} {/* MATCHES YOUR BACKEND */}
                </h3>
              </div>
              <div className="text-right">
                <span className="text-2xl font-bold text-emerald-700">
                  {route.price} KES {/* MATCHES YOUR BACKEND */}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* ADDED: Local Information */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-blue-800">
            <Bus className="w-5 h-5 text-blue-600" />
            Popular Nairobi Local Routes
          </CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-2 text-sm">
          <p>• <strong>CBD ↔ Githurai:</strong> 50 KES</p>
          <p>• <strong>CBD ↔ Rongai:</strong> 80 KES</p>
          <p>• <strong>CBD ↔ Kangemi:</strong> 60 KES</p>
          <p>• <strong>CBD ↔ Embakasi:</strong> 70 KES</p>
          <p>• <strong>CBD ↔ Kawangware:</strong> 50 KES</p>
          <p>• <strong>CBD ↔ Kayole:</strong> 60 KES</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-emerald-800">
            <Compass className="w-5 h-5 text-emerald-600" />
            Safari & Tourism Corridors
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-sm">
          <p>• <strong>Masai Mara:</strong> Daily shuttles from Nairobi</p>
          <p>• <strong>Amboseli & Tsavo:</strong> Lodge transfers</p>
          <p>• <strong>Coastal:</strong> SGR to Mombasa + Diani connections</p>
          <p>• <strong>Cross-Border:</strong> To Arusha, Kampala, Kigali</p>
        </CardContent>
      </Card>
    </main>
  )
}
