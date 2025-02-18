# 🚀 LinkedIn Scraper

## 📌 Overview

LinkedIn Scraper is a web-based tool that allows users to extract data from LinkedIn:

1. **Company Followers Scraper** – Extract followers of a LinkedIn company page.
2. **Post Likers Scraper** – Get a list of users who liked a specific LinkedIn post.

This tool enables users to scrape LinkedIn data with a simple UI and download the results as a CSV file.  
Built with:

- **Frontend:** HTML, CSS, JavaScript (No jQuery, pure JS)
- **Backend:** Flask (Python)
- **Data Output:** CSV file download

---

## 🔧 Features

✅ **Scrape Company Followers**  
✅ **Scrape Post Likers**  
✅ **Validate LinkedIn URLs** (Company & Post)  
✅ **Download CSV Files Directly**

---

## ⚠️ **Using LinkedIn's Hidden APIs**

This scraper uses **LinkedIn's private (undocumented) APIs** to fetch follower and post-like data.  
Since these APIs are not officially supported by LinkedIn:

- **They may stop working at any time** if LinkedIn changes its internal API structure.
- **Scraping LinkedIn data may violate LinkedIn's Terms of Service** – Use responsibly.
- **You may need to update cookies/session headers periodically** to maintain access.

---

## 🛠️ Installation & Setup

### **🔹 1️⃣ Install Dependencies**

> **Backend (Flask & Python)**

```bash
pip install -r requirements.txt
```

### **🔹 2️⃣ Run the Backend**

> **Start the Flask server:**

```bash
python main.py
```

## 🚀 How to Use

### **🔹 1️⃣ Open index.html in a browser**

- Simply open the index.html file in your browser.

### **🔹 2️⃣ Select Scraper Type**

- **Company Followers Scraper** - Scrapes followers from a LinkedIn company page.
- **Post Likers Scraper** - Scrapes users who liked a specific LinkedIn post.

### 🔹 3️⃣ Enter the LinkedIn URL\*\*

- **Company URL Format:**

```bash
https://www.linkedin.com/company/12345678/admin/dashboard/
```

- **POST URL Format:**

```bash
https://www.linkedin.com/feed/update/urn:li:activity:1234567890/
```

### **🔹 4️⃣ Click Start Scraping**

- The scraper starts, and a loading animation appears on the button.
- Once completed, the CSV file automatically downloads.

### **🔹 5️⃣ Open Your CSV File**

- The scraped data is saved in a CSV file, ready for analysis

Website Url: https://linkedin-scraper-qcwi.onrender.com/
