fetch("http://127.0.0.1:5000/risk", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "Emma Johnson",
    product_category: "beauty"
  })
})
.then(res => res.json())
.then(data => console.log(data));
