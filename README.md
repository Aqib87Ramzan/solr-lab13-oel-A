# Lab 13 — Indexing, Importing and Searching Data in Apache Solr

**Course:** CS-347 Parallel & Distributed Computing  
**Class:** BSCS-13A  
**Instructor:** Dr. Khurram Shahzad  
**Student:** Aqib Ramzan (459729)
**Date:** 8th May 2026

---

## 📌 Overview

This project demonstrates the use of **Apache Solr** as a full-text search engine. It includes:
- Indexing a real-world student dataset (100 records) into Solr
- Executing advanced search queries with filtering, sorting, faceting, and highlighting
- A **Flask-based web application** integrated with Solr for real-time search

---

## 🗂️ Project Structure

```
solr-lab13-oel-A/
│
├── app.py                  # Flask backend — connects to Solr API
├── students.csv            # Dataset — 100 student records
├── templates/
│   └── index.html          # Frontend — search UI, contains HTML + CSS + JS
└── README.md               # Project documentation
```

---

## 📊 Dataset

The dataset (`students.csv`) contains **100 student records** with the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Unique student ID |
| `name` | Text | Full name of the student |
| `age` | Integer | Age of the student |
| `department` | Text | Academic department |
| `cgpa` | Float | Cumulative GPA (0.0 – 4.0) |
| `city` | Text | City of residence |

### Departments covered:
- Computer Science (21 students)
- Software Engineering (17 students)
- Artificial Intelligence (16 students)
- Data Science (16 students)
- Cyber Security (15 students)
- Networking (15 students)

### Cities covered:
Lahore, Karachi, Islamabad, Peshawar, Quetta, Rawalpindi, Faisalabad, Multan, Sialkot

---

## ⚙️ Setup & Installation

### Prerequisites
- Java JDK 21+ (tested with JDK 25.0.2)
- Apache Solr 10.0.0
- Python 3.x
- pip

### Step 1: Start Apache Solr
```bash
cd C:\solr-10.0.0\bin
solr start
```
Solr runs at: `http://localhost:8983/solr`

### Step 2: Create Solr Core
```bash
solr create -c student_records
```

### Step 3: Index the Dataset
```bash
curl "http://localhost:8983/solr/student_records/update?commit=true" \
  -H "Content-Type: application/csv" \
  --data-binary @students.csv
```

### Step 4: Install Python Dependencies
```bash
pip install flask requests
```

### Step 5: Run the Web Application
```bash
python app.py
```

Open your browser at: `http://127.0.0.1:5000`

---

## 🔍 Task 1 — Solr Queries

All queries were executed via the Solr Admin UI (`http://localhost:8983/solr`) and browser URLs.

| # | Query | Description |
|---|---|---|
| 1 | `q=*:*` | Retrieve all 100 records |
| 2 | `q=department:"Computer Science"` | Filter by department |
| 3 | `q=*:*&fq=city:Lahore` | Filter by city using `fq` parameter |
| 4 | `q=*:*&sort=cgpa desc` | Sort by CGPA high to low |
| 5 | `q=*:*&start=0&rows=5` | Pagination — first 5 results |
| 6 | `q=cgpa:[3.5 TO 4.0]` | Range query — CGPA between 3.5 and 4.0 |
| 7 | `q=*:*&facet=true&facet.field=department_str` | Faceted search grouped by department |
| 8 | `q=name:Ali&hl=true&hl.fl=name` | Highlighted search results |

---

## 🌐 Task 2 — Web Application Features

The Flask web app (`app.py`) connects to Solr's REST API and provides:

### Features Implemented:
| Feature | Description |
|---|---|
| **Search bar** | Search by name, department, or city |
| **Real-time results** | Results update instantly on search |
| **Autocomplete** | Suggestions appear while typing |
| **Faceted navigation** | Browse by department with counts |
| **Filters** | Filter results by department dropdown |
| **Sorting** | Sort by CGPA (high/low) or Age |
| **Pagination** | 5 results per page, 20 pages total |
| **Responsive UI** | Clean, mobile-friendly design |
| **CGPA color coding** | Green for CGPA ≥ 3.5, red for below |

### How it works:
1. User enters a search query in the browser
2. Flask receives the query and sends it to Solr's `/select` endpoint
3. Solr returns matching documents as JSON
4. Flask passes results to the HTML template
5. Jinja2 renders the results dynamically in the browser

---

## 🔧 Key Technical Details

### Solr Configuration:
- **Core name:** `student_records`
- **Port:** 8983
- **Schema:** Managed schema (auto field detection)
- **Facet field:** `department_str` (string type for exact faceting)

### Why `department_str` instead of `department`?
Solr automatically creates a `_str` copy field for string fields that supports exact-value faceting. The regular `department` field is tokenized (text type) and cannot be used for faceting. Using `department_str` returns correct grouped counts.

### Flask Route:
- `GET /` — loads homepage with all records
- `POST /` — processes search query and filters

---

## 📈 Observations

- Query 1: All 100 records retrieved in **1ms** (QTime: 1)
- Query 2: **21** Computer Science students found
- Query 3: Lahore filter returned students using Solr `fq` parameter
- Query 4: Maha Zafar (CGPA: 3.96) ranked first in descending sort
- Query 5: Pagination working — 5 results per page, 20 pages total
- Query 6: **70 out of 100** students have CGPA between 3.5 and 4.0
- Query 7: Faceted search correctly grouped all 6 departments with counts
- Query 8: Highlighting successfully marked "Ali" in search results

---

## 🚧 Challenges & Solutions

| Challenge | Solution |
|---|---|
| `JAVA_HOME` not set | Manually set `JAVA_HOME=C:\Program Files\Java\jdk-25.0.2` in System Environment Variables |
| CSV file not found by curl | Used full OneDrive path in curl command |
| Department facets returning empty `[]` | Switched from `department` (text) to `department_str` (string) field |
| Search not finding "Ali Hassan" | Changed query to use wildcard: `name:*Ali*` |

---

## 🔗 Links

- **GitHub Repository:** https://github.com/Aqib87Ramzan/solr-lab13-oel-A.git
- **Solr Admin UI:** http://localhost:8983/solr
- **Web App:** http://127.0.0.1:5000
- **Apache Solr Docs:** https://solr.apache.org/guide/

---

## ✅ Conclusion

This lab successfully demonstrated Apache Solr's powerful search capabilities. By indexing 100 student records and executing 8 different query types, the performance and flexibility of Solr was clearly observed. The Flask web application provides a clean, intuitive interface that integrates seamlessly with Solr's REST API, enabling real-time full-text search with advanced filtering, sorting, faceted navigation, and pagination.
