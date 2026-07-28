const handleSearch = async (e) => {
  e.preventDefault()

  const searchUrl = query.trim()
    ? `/api/search?q=${encodeURIComponent(query.trim())}&category=local`
    : `/api/search?category=local`

  setLoading(true)
  setHasSearched(true)

  try {
    const res = await fetch(searchUrl)

    if (!res.ok) {
      throw new Error(`Server error: ${res.status}`)
    }

    const data = await res.json()
    setRoutes(data || [])
  } catch (error) {
    console.error("Failed to fetch local routes:", error)
    setRoutes([])
  } finally {
    setLoading(false)
  }
}
