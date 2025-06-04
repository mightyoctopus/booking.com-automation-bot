# Booking.com Hotel Search Automation

This Python-based automation tool allows you to search hotels on **Booking.com** with custom filters and automatically extract the results into a structured **CSV file** within seconds.

It supports filtering by:

- **Location** (city or region)
- **Travel dates** (check-in and check-out)
- **Number of visitors**
- **Minimum hotel rating**

Built with **Selenium** for web interaction and **Pandas** for data handling, this tool is ideal for travel planning, data analysis, or automation testing.

---

## Features
(You can add anything on top of these on your own way!)

- Customizable search filters
- Hotel results saved to `results.csv`
- Fast execution with dynamic data scraping
- Clean setup using `Selenium` and `Pandas`

---

## ⚠Note for Developers

> 💡 Please read this before running the tool!

1. **WebDriver Initialization Bug**  
   On the **first run**, the app might throw a **WebDriver error** due to initialization issues.  
   **No worries!** Just re-run the script — it should work perfectly on the second attempt.

2. **Dynamic Website Behavior**  
   Booking.com uses a complex, dynamic layout with **lazy loading**, **changing DOMs**, and **UI overlays**.  
   ✅ For best results:
   - Keep the automation browser **wide enough** to show the **left-side filtering panel**.
   - This ensures the script’s element selectors work properly without UI interference.

---

## Requirements

- Python 3.8+
- Selenium
- Pandas
- Chrome WebDriver (version matching your Chrome browser)

Install the required libraries:

```bash
pip install -r requirements.txt
