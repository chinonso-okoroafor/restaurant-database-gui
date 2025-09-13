
---

# Restaurant Analytics System — End-to-End Database + GUI Application  

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)  
![SQLite](https://img.shields.io/badge/SQLite-Relational%20DB-orange)  
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)  
![Matplotlib](https://img.shields.io/badge/Visualization-Matplotlib-purple)  
![Pandas](https://img.shields.io/badge/Data%20Cleaning-Pandas-red)

## Project Scope & Business Requirements

A local food delivery service needed to:
1. **Replace error-prone CSV files** with a **structured relational database**.
2. **Clean and standardize messy data** (missing values, inconsistent formats).
3. Build a **non-technical user interface (GUI)** to:
   - Update restaurant manager details (email, tenure, name)
   - Calculate and display **mean Customer Rating-Food per restaurant**
   - Generate a **histogram of Delivery Time Taken (mins)** for performance analysis

---

## Technical Implementation

### 1. Data Cleaning & Preprocessing (Pandas)
Handled real-world data quality issues:
```python
# Examples from cleaning logic
df['QuantityOfItems'].fillna(df['QuantityOfItems'].median(), inplace=True)
df['PaymentMode'] = np.where(df['CreditCard'].notna(), 'Credit Card',
                   np.where(df['DebitCard'].notna(), 'Debit Card', 'Cash on Delivery'))
df['Manager'].fillna('Unknown', inplace=True)
df['Email'].fillna('noemail@example.com', inplace=True)
```
---

### 2. Database Design (SQLite, 3NF)

Designed and implemented a **9-table normalized schema** following Third Normal Form to eliminate redundancy and ensure data integrity.

**Core Tables**:
- `Restaurant` ←→ `Manager`, `Cuisine`, `Category`, `Zone`, `Location`
- `Orders` ←→ `Customer`, `Restaurant`
- Later extended → `DeliveryStaff`

**ERD Snapshot**:  
![ERD Diagram](https://github.com/chinonso-okoroafor/restaurant-database-gui/blob/main/screenshots/erd-diagram.png)
---

### 3. GUI Application (Tkinter + Matplotlib)

Built a desktop application with 3 core business functions:

#### Feature 1: Update Restaurant Manager
- Form-based interface with validation
- Real-time database updates
- Error handling for invalid inputs (e.g., malformed email)

![Manager Update GUI](https://github.com/chinonso-okoroafor/restaurant-database-gui/blob/main/screenshots/manager_update.png)  
*Fig: GUI preventing invalid email submission with messagebox alert*

---

#### Feature 2: Calculate Mean Food Rating per Restaurant
- Dropdown selector for restaurant name
- Executes `JOIN` between `Orders` and `Restaurant`
- Displays result rounded to 2 decimal places

```sql
SELECT AVG(CustomerRatingFood) 
FROM Orders 
JOIN Restaurant ON Orders.RestaurantID = Restaurant.RestaurantID 
WHERE Restaurant.RestaurantName = ?
```

![Food Rating GUI](https://github.com/chinonso-okoroafor/restaurant-database-gui/blob/main/screenshots/food_rating.png)  
*Fig: Mean food rating calculated for "The Golden Dragon"*

---

#### Feature 3: Histogram of Delivery Times
- Queries all `DeliveryTimeTaken` values
- Plots distribution using `matplotlib`
- Reveals operational bottlenecks or efficiencies

```python
plt.hist(delivery_times, bins=30, edgecolor='black')
plt.title("Histogram of Delivery Time Taken for All Orders")
```

![Delivery Time Histogram](https://github.com/chinonso-okoroafor/restaurant-database-gui/blob/main/screenshots/delivery_histogram.png)  
*Fig: Visualizing delivery performance across all orders*

---

## Key Technical Skills Demonstrated

| Skill Area             | Tools & Techniques Used                          | Business Relevance                            |
|------------------------|--------------------------------------------------|-----------------------------------------------|
| **Database Design**    | ERD, 3NF, SQLite, PK/FK, Schema Evolution        | Foundation for scalable, reliable data systems |
| **Data Cleaning**      | Pandas, Imputation, Conditional Logic, Validation | Prepares data for accurate analysis & reporting |
| **Backend Development**| Python, SQLite3, SQL Queries (JOIN, AVG, SELECT)  | Extracts KPIs from structured data             |
| **Frontend (GUI)**     | Tkinter, Event Handling, Dropdowns, Messagebox   | Empowers non-technical users to interact with data |
| **Data Visualization** | Matplotlib, Histograms, Axis Labeling            | Communicates insights visually to stakeholders |
| **Software Engineering**| OOP, Try-Except, Modular Functions, Documentation | Ensures maintainable, production-ready code   |

---

## Business Impact & Analytical Value

This system enables the food delivery service to:
- **Improve Manager Accountability**: Track tenure and contact info dynamically.
- **Monitor Restaurant Performance**: Identify high/low-rated restaurants by food quality.
- **Optimize Logistics**: Spot delivery time outliers and improve SLA compliance.
- **Scale Operations**: Schema supports adding delivery staff, payment providers, etc.
---

## Testing & Validation

- All GUI functions include **error handling** (e.g., database connection failures, empty inputs).
- **Screenshots provided** in report validate successful execution of all features.
- Schema redesigned to include `DeliveryStaff` — proving ability to **iterate based on new requirements**.

---

## Repository Structure

```
├── Coursework.py               # Main DB logic
├── gui.py                      # Main GUI logic
├── data/
│   ├── restaurant_info.csv     # Raw input data
│   └── Orders.csv
├── Coursework.db              # Generated SQLite database
├── screenshots/               # Validation images (add your PNGs here)
│   ├── erd-diagram.png
|   ├── manager_update.png
│   ├── food_rating.png
│   └── delivery_histogram.png
└── README.md                   # You are here!
```

---

## How to Run

1. Clone this repo:
   ```bash
   git clone https://github.com/yourusername/restaurant-analytics-system.git
   cd restaurant-analytics-system
   ```

2. Install dependencies:
   ```bash
   pip install pandas matplotlib
   ```

3. Run the application:
   ```bash
   python Coursework.py
   python gui.py
   ```

> Ensure `restaurant_info.csv` and `Orders.csv` are in the `/data` folder before running.

## References

- Dasu, T., & Johnson, T. (2003). *Exploratory Data Mining and Data Cleaning*. Wiley.  
- Dennis, A., Wixom, B.H., & Tegarden, D. (2012). *Systems Analysis & Design*. Wiley.

---