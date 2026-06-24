@app.get("/search")
def search(q: str):
    query_words = q.lower().split()

    @app.get("/edit/{tour_id}")
def edit_page(tour_id: int):
    cursor.execute("SELECT * FROM tours WHERE id = ?", (tour_id,))
    row = cursor.fetchone()

    from fastapi import Form

from fastapi import Form

@app.post("/update/{tour_id}")
def update_tour(
    tour_id: int,
    name: str = Form(...),
    price: int = Form(...)
):
    cursor.execute(
        "UPDATE tours SET name=?, price=? WHERE id=?",
        (name, price, tour_id)
    )
    conn.commit()

    return {"message": "Tour updated successfully"}

@app.get("/edit/{tour_id}")
def edit_page(tour_id: int):
    cursor.execute("SELECT * FROM tours WHERE id=?", (tour_id,))
    row = cursor.fetchone()

    if not row:
        return "Tour not found"

    id, name, desc, keywords, region, price, link = row

    return f"""
    <html>
    <body>

        <h2>Edit Tour</h2>

        <form action="/update/{id}" method="post">
            Name:<br>
            <input name="name" value="{name}"><br><br>

            Price:<br>
            <input name="price" value="{price}"><br><br>

            <button type="submit">Update</button>
        </form>

        <br>
        <a href="/dashboard">← Back to Dashboard</a>

    </body>
    </html>
    """

@app.post("/update/{tour_id}")
def update_tour(
    tour_id: int,
    name: str = Form(...),
    desc: str = Form(...),
    keywords: str = Form(...),
    region: str = Form(...),
    price: int = Form(...),
    link: str = Form(...)
):
    cursor.execute("""
    UPDATE tours
    SET name = ?, desc = ?, keywords = ?, region = ?, price = ?, link = ?
    WHERE id = ?
    """, (name, desc, keywords, region, price, link, tour_id))

    conn.commit()

    return {"message": "Tour updated successfully"}
    
    if not row:
        return {"error": "Tour not found"}

    id, name, desc, keywords, region, price, link = row

    return f"""
    <html>
    <body>
        <h2>Edit Tour</h2>

        <form action="/update/{id}" method="post">
            Name: <input name="name" value="{name}"><br><br>
            Description: <input name="desc" value="{desc}"><br><br>
            Keywords: <input name="keywords" value="{keywords}"><br><br>
            Region: <input name="region" value="{region}"><br><br>
            Price: <input name="price" value="{price}"><br><br>
            Link: <input name="link" value="{link}"><br><br>

            <button type="submit">Update Tour</button>
        </form>

        <br><a href="/dashboard">← Back</a>
    </body>
    </html>
    """
``

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

@app.get("/dashboard")
def dashboard():
    cursor.execute("SELECT * FROM tours")
    rows = cursor.fetchall()

    content = ""

    for row in rows:
        id, name, desc, keywords, region, price, link = row

        content += f"""
        <div class="card">
            <h3>{name}</h3>
            <p>{desc}</p>
            <p>Region: {region}</p>
            <p>Price: ${price}</p>
            <a href="{link}" target="_blank">View Link</a><br><br>
            <a href="/delete/{id}">❌ Delete</a>
        </div>
        """

    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial; text-align:center; background:#f4f7f6; }}
            .card {{ background:white; padding:20px; margin:20px auto; max-width:400px; border-radius:10px; }}
        </style>
    </head>

    <body>
        <h1>Admin Dashboard</h1>
        <a href="/admin">➕ Add New Tour</a>
        {content}
    </body>
    </html>
    """
