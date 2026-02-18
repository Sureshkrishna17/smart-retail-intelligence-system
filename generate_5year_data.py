import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuration
products = ['Rice', 'Wheat', 'Sugar', 'Tea', 'Oil', 'Biscuits', 'Soap', 'Shampoo']
base_demand = {
    'Rice': 50, 'Wheat': 45, 'Sugar': 40, 'Tea': 15, 
    'Oil': 20, 'Biscuits': 60, 'Soap': 30, 'Shampoo': 25
}
start_date = datetime.now() - timedelta(days=365*5)
end_date = datetime.now()

# Festival Definitions (Month, Day)
festivals = [
    (10, 24), (11, 12), # Diwali (approx)
    (1, 14), (1, 15),   # Pongal
    (12, 25), (1, 1)    # Christmas/New Year
]

def get_festival_boost(date):
    for month, day in festivals:
        # Check ±7 days window
        fest_date = datetime(date.year, month, day)
        if abs((date - fest_date).days) <= 7:
            return 1.5
    return 1.0

def get_weekend_boost(date):
    return 1.2 if date.weekday() >= 5 else 1.0

# Generate Data
data = []
current_date = start_date

print("Generating 5 years of data...")

while current_date <= end_date:
    for product in products:
        # Calculate demand
        base = base_demand[product]
        noise = np.random.normal(0, base * 0.1) # 10% variance
        trend = 1 + (current_date - start_date).days / (365*5) * 0.2 # 20% growth over 5 years
        
        # Apply boosts
        fest_boost = get_festival_boost(current_date)
        weekend_boost = get_weekend_boost(current_date)
        
        sales_qty = int(max(0, (base + noise) * trend * fest_boost * weekend_boost))
        
        # Simulate stock (usually higher than sales, but sometimes dips)
        stock_qty = int(sales_qty * random.uniform(1.2, 3.0))
        
        data.append({
            'Date': current_date.strftime('%Y-%m-%d'),
            'Product': product,
            'Sales_Qty': sales_qty,
            'Stock_Qty': stock_qty
        })
    
    current_date += timedelta(days=1)

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
filename = 'retail_sales_5years.csv'
df.to_csv(filename, index=False)
print(f"✅ Successfully generated {len(df)} rows in '{filename}'")
