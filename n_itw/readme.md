# ⏱ Time Series Forecasting of Frequency Data using ARIMA

This project demonstrates a time series forecasting solution using the ARIMA model to predict frequency variations over time. It involves data preprocessing, visualization, stationarity testing, and model evaluation.

---

## 📁 Dataset

- A realistic dataset with Date, Time, and Frequency_Hz columns.
- Combined date and time into a single Datetime index.
- Example source: realistic_time_date_frequency_dataset.csv

---

## 📊 Project Workflow

### ✅ 1. Data Preprocessing
- Combined Date and Time into a single Datetime column.
- Parsed datetime formats using a custom parser.
- Set Datetime as the index for time series modeling.

### ✅ 2. Exploratory Data Analysis (EDA)
- Used matplotlib and seaborn to visualize frequency trends over time.
- Grouped data by month to study frequency patterns.

### ✅ 3. Stationarity Testing
- Applied the Augmented Dickey-Fuller (ADF) test.
- Determined differencing order d for the ARIMA model.

### ✅ 4. ACF and PACF Plots
- Generated plots to help choose optimal ARIMA parameters p and q.

### ✅ 5. ARIMA Modeling
- Built the ARIMA model using the statsmodels library.
- Trained on 80% of the dataset and tested on the remaining 20%.
- Forecasted future frequency values and evaluated results.

---

## 🛠 Technologies Used

- Python 3.x  
- Pandas  
- Matplotlib & Seaborn  
- Statsmodels (ARIMA, ADF Test, ACF/PACF)
