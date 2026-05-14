"""
Egyptian Drug Price Updater
--------------------------
يقوم هذا السكربت بـ:
1- تحميل صفحة البحث من DrugEye.
2- استخراج اسم الدواء وسعره.
3- تحديث ملف JSON محلي.
4- إنشاء ملف CSV وExcel جديدين بتاريخ اليوم.

المتطلبات:
pip install requests beautifulsoup4 pandas openpyxl
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime

# رابط البحث في DrugEye
BASE_URL = "https://drugeye.pharorg.com/drugeyeapp/android-search/drugeye-android-live-go.aspx"

# قائمة بالأدوية المطلوب تحديثها
DRUGS_TO_SEARCH = [
    "Panadol",
    "Augmentin",
    "Cataflam",
    "Brufen",
    "Congestal",
    "Voltaren"
]

def search_drug(drug_name):
    """
    البحث عن دواء واستخراج النتائج.
    """
    params = {"search": drug_name}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(BASE_URL, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    # استخراج جميع صفوف النتائج
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 3:
            name = cols[0].get_text(strip=True)
            company = cols[1].get_text(strip=True)
            price = cols[2].get_text(strip=True)

            if name:
                results.append({
                    "name": name,
                    "company": company,
                    "price": price,
                    "searched_term": drug_name
                })

    return results

def update_database():
    all_results = []

    for drug in DRUGS_TO_SEARCH:
        print(f"Searching for {drug}...")
        try:
            results = search_drug(drug)
            all_results.extend(results)
        except Exception as e:
            print(f"Error searching {drug}: {e}")

    if not all_results:
        print("No results found.")
        return

    # DataFrame
    df = pd.DataFrame(all_results)

    # اسم الملف بالتاريخ
    today = datetime.now().strftime("%Y-%m-%d")

    # حفظ JSON
    json_file = f"egypt_drugs_{today}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    # حفظ CSV
    csv_file = f"egypt_drugs_{today}.csv"
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")

    # حفظ Excel
    excel_file = f"egypt_drugs_{today}.xlsx"
    df.to_excel(excel_file, index=False)

    print("Files created successfully:")
    print(json_file)
    print(csv_file)
    print(excel_file)

if __name__ == "__main__":
    update_database()
