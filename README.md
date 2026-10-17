# Personal Finance Dashboard

A simple and interactive web application to track daily expenses, manage spending records and visualize personal finances.

## Features

- **Add Expenses:** Record descriptions, amounts, categories and dates.
- **Expense History:** View saved expenses in an organized table.
- **Total Spending:** Calculate the total amount of recorded expenses.
- **Category Analysis:** Visualize spending by category using charts.
- **Spending Trends:** Track expenses over time with interactive charts.
- **Database Storage:** Store expense records using SQLite.

## Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite, Flask-SQLAlchemy
- **Frontend:** HTML, Tailwind CSS
- **Data Visualization:** Chart.js

## Project Structure

```text
personal-finance-dashboard/
├── app.py
├── templates/
│   └── index.html
└── instance/
    └── expenses.db
```

*Note: The database file is created automatically when the application runs.*

## Installation and Setup

**1. Clone the repository**

```bash
git clone <your-repository-url>
cd personal-finance-dashboard
```

**2. Install dependencies**

```bash
python -m pip install flask flask-sqlalchemy
```

**3. Run the application**

```bash
python app.py
```

**4. Open in your browser**

Visit [http://127.0.0.1:4848](http://127.0.0.1:4848).

## How to Use

1. Launch the application.
2. Enter the expense description and amount.
3. Select a category and date.
4. Click **Add Expense** to save the record.
5. Review your expense history, total spending and charts.

## Future Improvements

- Date and category filters
- Expense editing and deletion
- CSV export
- Monthly budgets and spending reports
- User authentication

## Author

**Abhronil Jash**
