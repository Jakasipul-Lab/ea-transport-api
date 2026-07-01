<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Search Results</title>
<style>
body{font-family:Arial;background:#f5f5f5;margin:0;padding:20px}
h1{text-align:center}
.card{background:white;padding:16px;margin:12px auto;border-radius:10px;max-width:600px;box-shadow:0 2px 6px #ccc}
.price{color:#0a7;font-weight:bold}
a{color:#06c;text-decoration:none}
</style>
</head>
<body>
<h1 id="title">Results</h1>
<div id="results">Loading...</div>
<script>
const DB = {
  bus: [
    {name:"Nairobi to Mombasa Bus", price:"KES 1,200", link:"#"},
    {name:"Nairobi to Kisumu Matatu", price:"KES 1,500", link:"#"}
  ],
  electronics: [
    {name:"iPhone 14 Used", price:"KES 85,000", link:"#"},
    {name:"Samsung TV 43inch", price:"KES 42,000", link:"#"}
  ],
  safari: [
    {name:"3-Day Masai Mara", price:"KES 28,000", link:"#"},
    {name:"Amboseli Weekend", price:"KES 18,000", link:"#"}
  ]
};
const params = new URLSearchParams(location.search);
const cat = params.get("cat");
document.getElementById("title").innerText = cat? cat.toUpperCase() + " Results" : "All Results";
const items = DB[cat] || [];
document.getElementById("results").innerHTML = items.length
 ? items.map(i=>`<div class="card"><h3>${i.name}</h3><p class="price">${i.price}</p><a href="${i.link}">View Details →</a></div>`).join("")
  : "<p>No items found.</p>";
</script>
</body>
</html>
'@
