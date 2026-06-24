@app.get("/search")
def search(q: str):
    query_words = q.lower().split()

    cursor.execute("SELECT * FROM tours")
    rows = cursor.fetchall()

    results = []

    for row in rows:
        id, name, desc, keywords, region, price, link = row

        keyword_list = keywords.split(",")

        score = 0

        for word in query_words:
            if word in keyword_list:
                score += 3

        if region == "africa":
            score += 2

        if score > 0:
            results.append({
                "name": name,
                "desc": desc,
                "price": price,
                "link": link,
                "score": score
            })

    # ✅ sort by best match
    results.sort(key=lambda x: x["score"], reverse=True)

    # ✅ build UI
    cards = ""

    for r in results:
        cards += f"""
        <div class="card">
            <h3>{r['name']}</h3>
            <p>{r['desc']}</p>
            <p><b>From ${r['price']}</b></p>
            <a href="{r['link']}" class="btn">Book Now</a>
        </div>
        """

    if not cards:
        cards = "<p>No results found</p>"

    return HTMLResponse(f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; text-align:center; background:#f4f7f6; }}
            .card {{ background:white; padding:20px; margin:20px auto; max-width:400px; border-radius:10px; }}
            .btn {{ display:block; padding:10px; margin-top:10px; background:#16a34a; color:white; text-decoration:none; }}
        </style>
    </head>
    <body>
        <h2>Results for: {q}</h2>
        {cards}
    </body>
    </html>
    """)
