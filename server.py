# 4. Search API Endpoints - 2 TIER VERSION
@app.get("/api/search")
@app.get("/api/routes")
def get_routes(
    category: str = Query(None),  # "safari" or "local"
    from_: str = Query(None, alias="from"),
    to: str = Query(None),
    q: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Route)
    
    # TIER FILTER: safari = EAsafari, local = Jakasipul
    if category:
        query = query.filter(Route.category == category)
        
    # SEARCH FILTER: From + To
    if from_:
        query = query.filter(Route.origin.ilike(f"%{from_}%"))
    if to:
        query = query.filter(Route.destination.ilike(f"%{to}%"))
        
    # GENERAL SEARCH
    if q:
        search_term = f"%{q}%"
        query = query.filter(
            or_(
                Route.origin.ilike(search_term),
                Route.destination.ilike(search_term),
                Route.operator.ilike(search_term),
                Route.info.ilike(search_term)
            )
        )
        
    results = query.all()
    
    # Add commission info to response
    return {
        "tier": category,
        "commission": "5%",
        "count": len(results),
        "results": results
    }

# 5. Public Search Route for Frontend
@app.get("/public/search")
def public_search(
    from_: str = Query(None, alias="from"), 
    to: str = Query(None), 
    tier: str = Query("safari")  # safari or local
):
    """
    Maps frontend 'tier' to DB 'category'
    tier=easafari -> category=safari
    tier=jakasipul -> category=local
    """
    db = SessionLocal()
    try:
        category = "safari" if tier == "easafari" else "local"
        return get_routes(category=category, from_=from_, to=to, db=db)
    finally:
        db.close()
