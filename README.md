# 📚 EduPro Learner Analytics Dashboard

> Exploratory Data Analysis of learner demographics and course enrollment behavior on an online learning platform — built as a portfolio project during a Data Analytics Internship at Unified Mentor.

---

## 📋 Overview

EduPro is an online learning platform offering 60 courses across 12 subject categories at three difficulty levels (Beginner, Intermediate, Advanced). Despite collecting detailed user registration and transaction data, the platform lacked clear, data-driven answers about who its learners are and how they engage with course content.

This project performs a complete end-to-end Exploratory Data Analysis (EDA) on EduPro's dataset — from raw data cleaning and integration through to an interactive multi-tab Streamlit dashboard. Every insight is grounded in verified data computations with no hardcoded assumptions.

---

## ❓ Problem Statement

Despite having user and transaction data, EduPro currently lacks clear answers to:

- **Which age groups are most active** on the platform?
- **How do enrollment patterns differ by gender?**
- **What course categories are preferred** by different learner segments?
- **Are Beginner, Intermediate, or Advanced courses more popular** among specific age groups?

Without these insights, decisions related to course creation, marketing, and platform growth remain intuition-driven rather than data-driven.

---

## 📂 Dataset

| Table | Rows | Columns | Description |
|---|---|---|---|
| **Users** | 3,000 | 5 | Learner demographics — Age, Gender, UserID |
| **Courses** | 60 | 8 | Course catalog — Category, Level, Type, Price, Rating |
| **Transactions** | 10,000 | 7 | Enrollment records — UserID, CourseID, Date, Amount |
| **Teachers** | 60 | 7 | Instructor records (not used in analysis) |

**Key facts:**
- Age range: **15 – 35 years** (three bands: Teen / Young Adult / Adult)
- Gender split: **50.7% Female / 49.3% Male**
- Course types: **Free (38) / Paid (22)**
- Zero missing values, zero duplicate records, zero referential integrity violations

> **Note:** This is a fictional platform dataset used for educational portfolio purposes.

---

## 🛠️ Tools and Technologies

| Category | Tools |
|---|---|
| **Language** | Python 3.11 |
| **Data Analysis** | pandas |
| **Visualization** | Plotly Express, Plotly Graph Objects |
| **Dashboard** | Streamlit |
| **File Handling** | openpyxl |
| **Version Control** | Git / GitHub |
| **Environment** | VS Code |

---

## 🔬 Methods

### 1. Data Cleaning & Integration
- Loaded all 4 sheets from the Excel workbook using `pandas`
- Audited for duplicates, nulls, and referential integrity — all clean
- Joined **Users ↔ Transactions ↔ Courses** via inner joins on `UserID` and `CourseID`
- Created derived **Age Group** column (Teen 15–17 / Young Adult 18–25 / Adult 26–35)
- Final master dataframe: **10,000 rows × 17 columns**, zero nulls

### 2. Learner Demographic Analysis
- Age distribution across all 21 individual ages (15–35)
- Gender distribution and enrollment breakdown
- Per-user engagement metrics by age group and gender

### 3. Enrollment Distribution Analysis
- Enrollment counts by **CourseCategory**, **CourseType**, and **CourseLevel**
- Most and least popular category identification
- Free vs Paid consumption patterns
- Monthly enrollment trend analysis

### 4. Demographics × Course Preference (Cross Analysis)
- Age group vs Course Category **heatmap**
- Row-normalized Age × Level analysis (removes group-size bias)
- Gender × Course Level grouped comparison
- Gender × Course Category stacked comparison

### 5. Behavioral Insights
- Average courses per learner (overall and by segment)
- **Enrollment concentration** — Lorenz curve / Pareto-style analysis
- **Learner behavioral segmentation** — Beginner-only / Advanced-only / Mixed-level classification
- Free vs Paid preference by learner segment

---

## 💡 Key Insights

### 1. "Most Active" Has Two Valid Answers
Adults (26–35) generate the **highest total enrollment volume (4,799)** — but only because they are the largest group. Teens (15–17) have the **highest per-user engagement (3.39 courses/user)** vs 3.33 for Young Adults and 3.32 for Adults.

### 2. Near-Perfect Gender Parity
Gender split is **50.7% Female / 49.3% Male** across all age groups. No gender-specific strategy is required — the platform serves both genders equally.

### 3. Data Science Leads, but Programming Has a Retention Gap
**Data Science (916 enrollments)** is the most popular category. **Programming** is simultaneously the top entry point for Beginner-level learners (657 enrollments) yet ranks **last platform-wide (806 total)** — indicating a conversion/retention gap that warrants attention.

### 4. Teens Uniquely Prefer Advanced Courses (Counter-Intuitive Finding)
When measured as a **within-group percentage** (removing group-size bias):
- **Teen (15–17):** Advanced is top preference at **36.4%** — the only group where Advanced outranks Beginner
- **Young Adult (18–25):** Beginner leads at **36.0%**
- **Adult (26–35):** Beginner leads at **36.0%**

Intermediate is the least preferred level across **every** age group (~29–30%).

### 5. Small Group of Power Users Drives Most Activity
The **top 10% of users generate 42.3%** of all enrollments. The top 20% generate **66.5%**. Retention campaigns targeting this group can protect a disproportionate share of platform activity.

### 6. Mixed-Level Learners Are 4.3× More Engaged
Learners who explore multiple difficulty levels average **5.03 courses per user** — compared to 1.16 for Beginner-only and 1.18 for Advanced-only learners. Converting single-level learners into multi-level explorers is the clearest lever for increasing overall platform engagement.

### 7. Beginners Strongly Prefer Free Content
Beginner-level enrollments are **67.0% Free** vs 62.4% for Intermediate/Advanced — consistent with cautious, exploratory behavior among new learners before committing financially.

---

## 📊 Dashboard / Output

### Interactive Streamlit Dashboard
A **7-tab interactive dashboard** with real-time sidebar filters (Age Group, Gender, Course Category, Course Level, Course Type):

| Tab | Content |
|---|---|
| 🏠 Overview | 5 KPI cards + 4 summary charts |
| 👥 Demographics | Age distribution, gender split, age group analysis |
| 📊 Enrollments | Category ranking, level/type distribution, Beginner preferences, monthly trend |
| 🔥 Cross Analysis | Age × Category heatmap, normalized Age × Level, Gender × Level/Category |
| 💡 Behavior | Engagement distribution, Lorenz curve, learner segment analysis |
| 📈 KPIs | 15 platform KPIs + downloadable CSV |
| 🎯 Problem, Solution & Insights | Direct data-backed answers to all 4 business questions |

---

## 🚀 How to Run This Project

### Prerequisites
```
Python 3.9 or above
```

### Step 1 — Clone the repository
```bash
git clone https://github.com/your-username/edupro-analytics.git
cd edupro-analytics
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Place the dataset
Place `EduPro Online Platform.xlsx` in the **same folder** as `app.py`.

### Step 4 — Run the dashboard
```bash
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`

### requirements.txt
```
streamlit>=1.35.0
pandas>=2.0.0
plotly>=5.18.0
openpyxl>=3.1.0
```

---

## 📈 Results & Conclusion

| KPI | Value |
|---|---|
| Total Users | 3,000 |
| Total Enrollments | 10,000 |
| Platform Activity Rate | 100% (every user enrolled ≥1 time) |
| Avg Courses per User | 3.33 |
| Top Course Category | Data Science (916 enrollments) |
| Least Popular Category | Marketing / Programming (806 each) |
| Free Course Share | 64.0% |
| Top 10% Users → Enrollment Share | 42.3% |
| Mixed-Level Avg Courses | 5.03 |
| Single-Level Avg Courses | ~1.17 |

This project successfully converted EduPro's raw transactional data into clear, actionable answers to four business questions that previously had no data-backed response. The analysis revealed that "most active" is a two-dimensional concept (volume vs engagement), that a teen-specific course-level preference pattern exists and contradicts common assumptions, and that the strongest available lever for growing platform engagement is converting single-level learners into multi-level explorers.

---

## 🔭 Future Work

- **Predictive analytics** — Build a model to predict which users are at risk of disengaging (churn prediction)
- **Course recommendation system** — Recommend courses based on a learner's age group, past enrollment level, and category preference
- **Revenue analysis** — Extend the analysis to track revenue per category and estimate the revenue uplift from converting Free learners to Paid
- **Time-series analysis** — Analyze enrollment trends across months/seasons to identify peak learning periods
- **Cohort analysis** — Track how learner behavior evolves over time (e.g., do Beginner-only learners eventually expand to other levels?)
- **A/B testing framework** — Design experiments to test whether Advanced-content promotion to Teen users increases engagement
- **NLP on course descriptions** — Analyze course content to understand why certain categories attract higher engagement

---

## 👤 Author & Contact

**Mohammed Ashif Maniyar**
Data Analytics Intern — Unified Mentor

| Platform | Link |
|---|---|
| 📧 Email | mailto:mdasifmaniyar73@gmail.com |
| 💼 LinkedIn | https://www.linkedin.com/in/mohammed-ashif-maniyar-95b347152 |
| 🐙 GitHub | github.com/your-username |

> **Internship Program:** Unified Mentor — Data Analytics Track
> **Project Type:** Portfolio / Internship Deliverable
> **Year:** 2026

---

*This project was completed as part of a Data Analytics Internship at Unified Mentor. The dataset is fictional and used purely for educational and portfolio demonstration purposes.*
