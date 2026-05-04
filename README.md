# Kenya Maternal & Child Health Analysis
## A County-Level Data Series | KDHS 2022

This repository contains a two-part data analysis project examining 
maternal and child health indicators across all 47 Kenyan counties 
using data from the Kenya Demographic and Health Survey (KDHS) 2022.

## Project 1 — Skilled Antenatal Care Coverage

## Key Finding
Kenya's national skilled ANC coverage average is 97.1%, but this figure 
masks a serious regional divide.

- 🔴 **Lowest coverage:** Mandera, Garissa and Wajir
- 🟢 **Highest coverage:** Nairobi City, Nyamira and Migori
- ⚠️ Counties in North Eastern Kenya fall significantly below the 
  national average, indicating that geography and infrastructure 
  remain critical barriers for women accessing maternal care.

## Visualization
![ANC Coverage by County](kenya_anc_coverage_final.png)


## Project 2 — Under-5 Mortality Rate

### Key Finding
Kenya's national under-5 mortality rate stands at 42 deaths per 
1,000 live births. However, the data reveals a surprising pattern 
that challenges assumptions about poverty and child survival.

- 🔴 **Highest mortality:** Migori, Siaya and Homa Bay
- 🟢 **Lowest mortality:** Nairobi City, Mandera and Marsabit
- ⚠️ The Nyanza region shows elevated mortality rates likely driven 
  by malaria and HIV burden — despite having better infrastructure 
  than North Eastern counties.

# Key Insight
Comparing both projects reveals a striking analytical tension —
counties like Mandera have **low ANC coverage** but **relatively low 
under-5 mortality**, while counties like Migori have **decent ANC 
coverage** but **high child mortality**. This suggests that child 
survival in Kenya is shaped not just by poverty or remoteness, 
but by disease ecology and healthcare quality.

# Visualization
![Under-5 Mortality by County](kenya_under5_mortality.png)

# Tools Used
- Excel
- Python
- Pandas
- Matplotlib
- Google Colab

# Data Source
- Kenya Demographic and Health Survey (KDHS) 2022
- Published by Kenya National Bureau of Statistics (KNBS)
- Table 9.1C — Antenatal care by county
- Table 8.1 — Under-5 mortality by county

---

# Project 3 — ANC Quality: Beyond the 97% Coverage Figure
# Background
Following engagement on the first analysis, a health professional challenged 
the 97.1% ANC coverage figure — noting that timeliness and number of contacts 
tell a more honest story. This project responds to that feedback with data.

# Key Finding
When you look beyond attendance numbers, a deeper quality gap emerges across 
Kenyan counties across three indicators:

- **National 4+ visits coverage:** Only 62.3% of women complete the WHO 
  recommended minimum of 4 ANC visits
- **First trimester initiation:** Only 27.6% of women begin ANC in the 
  first trimester nationally
-  **No ANC at all:** Mandera, Garissa and Wajir have the highest proportions 
  of women receiving zero antenatal care

# Pattern Found
Mandera appears as a consistently underperforming county across all three 
quality indicators — low 4+ visits, highest no-ANC rate, and fewest first 
trimester visits. This points to a systemic access barrier beyond simple 
coverage statistics.

Counties like Meru, Vihiga and Machakos show strong early initiation despite 
not topping overall coverage charts — suggesting quality of engagement matters 
as much as attendance.

# Insight
> *Kenya's maternal health challenge is no longer just about getting women to 
attend ANC — it's about getting them there early enough and often enough to 
make a difference.*

# Visualization
![ANC Quality Indicators](kenya_anc_quality.png)

# Data Source
- Kenya Demographic and Health Survey (KDHS) 2022
- Table 9.2C — Number of ANC visits and timing of first visit by county
## Author
**Felix Beru**
Data Analyst | Nairobi, Kenya

📊 Passionate about using data to improve health outcomes in Kenya

[www.linkedin.com/in/felix-beru-04b905280]
