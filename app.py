from flask import Flask, render_template, request
import requests

app = Flask(__name__)
SOLR_URL = "http://localhost:8983/solr/student_records/select"

def get_facets():
    params = {
        "q": "*:*",
        "rows": 0,
        "wt": "json",
        "facet": "true",
        "facet.field": "department_str"
    }
    response = requests.get(SOLR_URL, params=params)
    data = response.json()
    raw = data.get("facet_counts", {}).get("facet_fields", {}).get("department_str", [])
    return [(raw[i], raw[i+1]) for i in range(0, len(raw), 2)]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    query = "*:*"
    total = 0
    sort = ""
    department_filter = ""
    page = int(request.args.get("page", 1))
    rows = 5
    start = (page - 1) * rows

    if request.method == "POST":
        user_input = request.form.get("query", "").strip()
        sort = request.form.get("sort", "")
        department_filter = request.form.get("department", "")

        if user_input:
            query = f'name:*{user_input}* OR department:*{user_input}* OR city:*{user_input}*'
        else:
            query = "*:*"

    params = {
        "q": query,
        "rows": rows,
        "start": start,
        "wt": "json",
        "hl": "true",
        "hl.fl": "name,department",
        "facet": "true",
        "facet.field": "department_str"
    }

    if sort:
        params["sort"] = sort
    if department_filter:
        params["fq"] = f'department_str:"{department_filter}"'

    response = requests.get(SOLR_URL, params=params)
    data = response.json()
    results = data["response"]["docs"]
    total = data["response"]["numFound"]
    total_pages = max((total + rows - 1) // rows, 1)
    facets = get_facets()

    return render_template("index.html",
        results=results,
        query=query,
        total=total,
        facets=facets,
        page=page,
        total_pages=total_pages,
        sort=sort,
        department_filter=department_filter
    )

if __name__ == "__main__":
    app.run(debug=True)
