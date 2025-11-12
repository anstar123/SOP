# Notebook: Line-by-line explanation (cell-by-cell)

## Cell 1 — (1 lines)

### Code preview

```python
!pip install contractions
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 2 — (27 lines)

### Code preview

```python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import contractions
from datetime import datetime, timedelta

import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA

... (truncated preview) ...
```

### Explanation

- This cell loads libraries and packages used throughout the notebook (data handling, numeric, plotting).
- This cell fits an ARIMA/ARIMAX model to the time series (possibly with exogenous sentiment features), and stores predictions.

---

## Cell 3 — (35 lines)

### Code preview

```python
def preprocess_text (text) :

  text = text.lower()

  text = re.sub(r'https?:\/V.*[\r\n]*',' ', text)
  text = re.sub(r'www.*[\r\n]*','', text)
  text = re.sub(r'https', ' ', text)
  text = re.sub(r"http\S+|www\S+|https\S+", '', text, flags=re.MULTILINE)

  text = re. sub(r'\@\w+','',text)
  text = re.sub(r'\#\w+', '', text)
  text = re.sub(r'@[a-z0-9]+', '', text)
... (truncated preview) ...
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 4 — (1 lines)

### Code preview

```python
all_tweets = pd.read_csv('stock_tweets.csv')
```

### Explanation

- This cell reads dataset(s) from CSV files into DataFrame(s).

---

## Cell 5 — (2 lines)

### Code preview

```python
print(all_tweets.shape)
all_tweets.head()
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 6 — (6 lines)

### Code preview

```python
print((all_tweets["Stock Name"].unique()))
stock_name = 'TSLA'
df = all_tweets[all_tweets['Stock Name'] == stock_name]
print('df.shape: ',df.shape)
sent_df = df.copy()
df.head()
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 7 — (1 lines)

### Code preview

```python
!pip install transformers torch
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 8 — (41 lines)

### Code preview

```python


MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"

tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
model.eval()

sentiment_pipeline = pipeline(
... (truncated preview) ...
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 9 — (1 lines)

### Code preview

```python
sent_df.head()
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 10 — (1 lines)

### Code preview

```python
sent_df.info()
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 11 — (3 lines)

### Code preview

```python
sent_df['Date'] = pd.to_datetime(sent_df['Date'], errors='coerce')

print(sent_df['Date'].dtype)
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 12 — (4 lines)

### Code preview

```python
daily_sentiment = sent_df.groupby(sent_df['Date'].dt.date).agg({

    'Sentiment_Score': 'mean'
}).reset_index()
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 13 — (9 lines)

### Code preview

```python

# Plotting the distribution of 'Sentiment_Score'
plt.figure(figsize=(10, 6))
plt.hist(daily_sentiment['Sentiment_Score'], bins=100, color='skyblue', edgecolor='black')
plt.title('Distribution of Daily Sentiment Score')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 14 — (5 lines)

### Code preview

```python

daily_sentiment['Date'] = pd.to_datetime(daily_sentiment['Date'], errors='coerce')


print(daily_sentiment['Date'].dtype)
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 15 — (3 lines)

### Code preview

```python
all_stocks = pd.read_csv('stock_yfinance_data.csv')
print(all_stocks.shape)
all_stocks.head()
```

### Explanation

- This cell reads dataset(s) from CSV files into DataFrame(s).

---

## Cell 16 — (2 lines)

### Code preview

```python
stock_df = all_stocks[all_stocks['Stock Name'] == stock_name]
stock_df['Date'] = pd.to_datetime(stock_df['Date'])
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 17 — (3 lines)

### Code preview

```python
print(stock_df.info())
final_df = pd.merge(stock_df, daily_sentiment, left_on='Date', right_on='Date', how='inner')
print(final_df.head())
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 18 — (1 lines)

### Code preview

```python
final_df.to_csv('my_file.csv', index=False)
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 19 — (3 lines)

### Code preview

```python
loaded_df = pd.read_csv('my_file.csv')
data = loaded_df.copy()
data.head()
```

### Explanation

- This cell reads dataset(s) from CSV files into DataFrame(s).

---

## Cell 20 — (10 lines)

### Code preview

```python
df = data.copy()
df['Date'] = pd.to_datetime(df['Date'])
plt.figure(figsize=(14, 7))
plt.plot(df['Date'], df['Close'], label="Close Price", color='blue')
plt.title("Tesla Stock Prices Over Time")
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.legend()
plt.grid()
plt.show()
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 21 — (0 lines)

### Code preview

```python

```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 22 — (16 lines)

### Code preview

```python
plt.figure(figsize=(14, 7))
plt.plot(df['Date'], df['Sentiment_Score'], label="Sentiment Score", color='green')
plt.axhline(y=0, color='red', linestyle='--', label="Neutral Sentiment")
plt.title("Sentiment Scores Over Time")
plt.xlabel("Date")
plt.ylabel("Sentiment Score")
plt.legend()
plt.grid()
plt.show()

# Distribution of sentiment scores
sns.histplot(df['Sentiment_Score'], bins=50, kde=True, color='purple')
... (truncated preview) ...
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 23 — (1 lines)

### Code preview

```python
df.describe
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 24 — (1 lines)

### Code preview

```python
df1=df.copy()
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 25 — (18 lines)

### Code preview

```python
df1['Sentiment_Score'] = df1['Sentiment_Score'].fillna(0)
endog_data = df1['Close']
scaler = MinMaxScaler()
exog_data = pd.DataFrame(scaler.fit_transform(df1[['Sentiment_Score']]),
                         index=df1.index,
                         columns=['Sentiment_Score_Scaled'])

p, d, q = 1, 1, 1

print("Fitting ARIMAX model...")
arimax_model = ARIMA(endog=endog_data, exog=exog_data, order=(p, d, q))
model_fit = arimax_model.fit()
... (truncated preview) ...
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).
- This cell fits an ARIMA/ARIMAX model to the time series (possibly with exogenous sentiment features), and stores predictions.

---

## Cell 26 — (3 lines)

### Code preview

```python
# # Calculate moving averages
# df1['ma_20'] = df1['Close'].rolling(window=20,min_periods=1).mean()
# df1['z_score'] = (df1['Close'] - df1['ma_20']) / df1['Close'].rolling(window=7, min_periods=1).std()
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 27 — (11 lines)

### Code preview

```python
# Plot z-scores
plt.figure(figsize=(14, 10))
plt.plot(df1['Date'], df1['z_score'], label="Z-Score", color='orange')
plt.axhline(y=1, color='red', linestyle='--', label="Overbought (Sell)")
plt.axhline(y=-1, color='green', linestyle='--', label="Oversold (Buy)")
plt.title("Z-Scores of Tesla Prices")
plt.xlabel("Date")
plt.ylabel("Z-Score")
plt.legend()
plt.grid()
plt.show()
```

### Explanation

- This cell simulates a trading strategy using model predictions to compute profit/loss, final balance, etc.

---

## Cell 28 — (23 lines)

### Code preview

```python
fig, ax1 = plt.subplots(figsize=(14, 7))


ax1.plot(df1['Date'], df1['Close'], label="Stock Price", color='blue')
ax1.set_xlabel("Date")
ax1.set_ylabel("Stock Price ($)", color='blue')
ax1.tick_params(axis='y', labelcolor='blue')


ax2 = ax1.twinx()
ax2.plot(df1['Date'], df1['Sentiment_Score'], label="Sentiment Score", color='green', alpha=0.7)
ax2.axhline(y=0, color='red', linestyle='--', label="Neutral Sentiment")
... (truncated preview) ...
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 29 — (27 lines)

### Code preview

```python
df1['lagged_sentiment'] = df1.groupby('Stock Name')['Sentiment_Score'].shift(1)
df1['sentiment_volatility'] = df1.groupby('Stock Name')['Sentiment_Score'].rolling(window=3).std().reset_index(0, drop=True)

for lag in [1, 3, 7, 14]:
    df1[f'future_returns_lag_{lag}'] = df1.groupby('Stock Name')['Close'].shift(-lag) / df1['Close'] - 1

features_to_correlate = [
    'Sentiment_Score',
    'sentiment_volatility',
    'lagged_sentiment',
    'future_returns_lag_1',
    'future_returns_lag_3',
... (truncated preview) ...
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 30 — (4 lines)

### Code preview

```python
# Check for skewness before applying log-transformation of scores

skew_value = skew(df1['Sentiment_Score'].dropna())
print(f"Skewness: {skew_value}")
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 31 — (106 lines)

### Code preview

```python

# Convert 'Date' column to datetime format
df1['Date'] = pd.to_datetime(df1['Date'])

def plot_dashboard(start_date, end_date):
    """Plot the stock price and sentiment dashboard"""
    # Filter data
    filtered_df = df1[(df1['Date'] >= pd.to_datetime(start_date)) &
                      (df1['Date'] <= pd.to_datetime(end_date))]

    # Create figure with dual y-axes
    fig = go.Figure()
... (truncated preview) ...
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).

---

## Cell 32 — (39 lines)

### Code preview

```python


def preprocess_data_zscore(df, feature_columns, target_column, sequence_length, exclude_columns=[]):
    feature_scaler = StandardScaler()
    target_scaler = StandardScaler()

    columns_to_scale = [col for col in feature_columns if col not in exclude_columns]
    df[columns_to_scale] = feature_scaler.fit_transform(df[columns_to_scale])
    df[target_column] = target_scaler.fit_transform(df[[target_column]])


    # Create sequences for LSTM
... (truncated preview) ...
```

### Explanation

- This cell processes tweet text and computes sentiment scores (e.g., using VADER or a custom pipeline).
- This cell defines or trains the LSTM/BiLSTM model; look for model architecture, input shapes, and training loop.

---

## Cell 33 — (2 lines)

### Code preview

```python
train_dataset = torch.utils.data.TensorDataset(X_train, y_train)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64, shuffle=True)
```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---

## Cell 34 — (123 lines)

### Code preview

```python
# --- 1. Define Bidirectional LSTM Model ---
class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(
            input_dim,
            hidden_dim,
            num_layers,
            batch_first=True,
            dropout=dropout,
            bidirectional=True  # <-- Set to True
        )
... (truncated preview) ...
```

### Explanation

- This cell defines or trains the LSTM/BiLSTM model; look for model architecture, input shapes, and training loop.
- This cell computes evaluation metrics like RMSE or directional accuracy to assess forecast quality.

---

## Cell 35 — (69 lines)

### Code preview

```python
import numpy as np
import matplotlib.pyplot as plt

# Parameters
threshold = 0.02
initial_balance = 10000
stop_loss_pct = 0.03
take_profit_pct = 2
position = 0
balance = initial_balance
portfolio = []

... (truncated preview) ...
```

### Explanation

- This cell loads libraries and packages used throughout the notebook (data handling, numeric, plotting).
- This cell simulates a trading strategy using model predictions to compute profit/loss, final balance, etc.

---

## Cell 36 — (2 lines)

### Code preview

```python
Profits = final_balance - initial_balance
print(f"Profits: {Profits:.2f}")
```

### Explanation

- This cell simulates a trading strategy using model predictions to compute profit/loss, final balance, etc.

---

## Cell 37 — (0 lines)

### Code preview

```python

```

### Explanation

- This cell performs data transformation, plotting, or utility operations. Read exact code for details.

---
