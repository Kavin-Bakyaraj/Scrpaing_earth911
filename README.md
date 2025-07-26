````markdown
# 🌎 Earth911 Recycling Facility Scraper

A Python script that scrapes recycling facility information from [Earth911](https://search.earth911.com/) based on user-defined material types, ZIP codes, and search radius. It extracts names, addresses, and accepted materials from each listing — all neatly outputted into a clean CSV file.

---

## 📌 Project Overview

This tool automates the discovery of recycling facilities for a given material and location. It handles pagination, performs robust data cleaning, and includes error handling to ensure consistent results even with occasional HTML or network hiccups.

---

## 🔁 Scraping Workflow

### 1. Search Initialization
- Builds a URL based on parameters:
  - **Material type** (e.g., `"Electronics"`)
  - **ZIP code** (e.g., `10001`)
  - **Search radius** (e.g., `100 miles`)
- **Default behavior**: Finds electronics recycling centers within 100 miles of ZIP code 10001.

### 2. Pagination Handling
- Scrapes the first results page and checks for a "next page" link.
- Loops through up to **20 pages** to prevent infinite scraping.
- Adds a **2-second delay** between requests.

### 3. Data Extraction
Each facility entry includes:
- ✅ Business Name
- ✅ Address Details
- ✅ Accepted Materials

### 4. Data Cleaning
- Removes BOM characters (`ï»¿`)
- Trims whitespace and newlines
- Converts material tags to comma-separated strings
- Inserts `"N/A"` for missing data

---

## ⚠️ Error Handling

- Up to **3 retries** for failed requests (with exponential backoff)
- Logs scraping issues and skips broken listings
- Catches missing or broken HTML elements gracefully
- Debug-friendly logging to file and console

---

## 📤 Output

- `earth911_data_clean.csv` — CSV file with structured facility data
- `earth911_scraper.log` — Log file tracking execution details, errors, and retry attempts

---

## 🧰 Dependencies

| Library        | Purpose                        |
|----------------|--------------------------------|
| `requests`     | HTTP requests with headers     |
| `BeautifulSoup4` | HTML parsing                |
| `pandas`       | DataFrame + CSV export         |
| `time`         | Request delay                  |
| `logging`      | Console + file logging         |
| `re`           | (Future use) Regex parsing     |

Install them with:

```bash
pip install requests beautifulsoup4 pandas
````

---

## ⚙️ Implementation Highlights

### 🕵️‍♂️ User Agent Spoofing

* Mimics a real browser using a custom `User-Agent` header

### 🌐 Request Logic

* Timeout setup to avoid hanging
* Retry mechanism for flaky connections

### 📝 Logging System

* Console + `earth911_scraper.log` file
* Timestamped logs with severity levels
* Tracks scraping progress + errors

---

## ▶️ Usage

### 1. Set Parameters

Inside the `main()` function:

```python
material = "Electronics"
zipcode = "10001"
radius = 100
```

### 2. Run the Script

```bash
python earth911_scraper.py
```

### 3. Get Output

* `earth911_data_clean.csv`
* `earth911_scraper.log`

---

## ❗ Limitations

* Scraper depends on the current Earth911 site structure (subject to change).
* May be blocked if Earth911 enforces strict anti-scraping measures.
* Pagination is limited to 20 pages per search.
* Designed to be respectful: includes 2-second delay per page request.

---

## 🚀 Future Enhancements

* ✅ Add CLI support for input parameters
* ✅ Integrate proxy rotation for bot bypassing
* ✅ Push data into MongoDB/PostgreSQL instead of CSV
* ✅ Add headless browser fallback for dynamic content

---

## 👨‍💻 Author

Built by [Kavin](https://github.com/your-github-profile) — intern @ SNS iHub, building automation tools and AI agents with Python.

