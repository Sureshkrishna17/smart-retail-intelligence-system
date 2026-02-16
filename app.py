import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Page Configuration
st.set_page_config(
    page_title="Smart Retail Intelligence System",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, vibrant UI - Orange/Teal/Pink Theme
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        padding: 20px;
    }
    .stApp {
        background: linear-gradient(135deg, #FFF5E6 0%, #FFE4B5 100%);
    }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(255, 107, 53, 0.4);
        margin: 10px 0;
    }
    .alert-card {
        background: linear-gradient(135deg, #FF1744 0%, #FF5252 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 8px 20px rgba(255, 23, 68, 0.4);
    }
    .success-card {
        background: linear-gradient(135deg, #00CED1 0%, #20B2AA 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 8px 20px rgba(0, 206, 209, 0.4);
    }
    .cart-card {
        background: linear-gradient(135deg, #FFB6C1 0%, #FF69B4 100%);
        padding: 15px;
        border-radius: 12px;
        color: white;
        margin: 8px 0;
        box-shadow: 0 6px 15px rgba(255, 105, 180, 0.3);
    }
    h1 {
        color: #FF6B35;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    h2, h3 {
        color: #F7931E;
        font-weight: 700;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 53, 0.6);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'inventory' not in st.session_state:
    st.session_state.inventory = {}
if 'billing_cart' not in st.session_state:
    st.session_state.billing_cart = []
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None

# Product prices (in INR)
PRODUCT_PRICES = {
    'Rice': 50,
    'Wheat': 45,
    'Sugar': 40,
    'Tea': 200,
    'Oil': 150,
    'Biscuits': 30,
    'Soap': 35,
    'Shampoo': 120
}

# Festival dates (for 1.5x boost logic)
FESTIVAL_DATES = {
    'Diwali': [(10, 24), (11, 12)],  # Oct 24 - Nov 12
    'Pongal': [(1, 14), (1, 17)],     # Jan 14-17
    'New Year': [(12, 25), (1, 5)]    # Dec 25 - Jan 5
}

def is_festival_period(date):
    """Check if date is within ±7 days of festival dates"""
    try:
        month = date.month
        day = date.day
        
        for festival, date_ranges in FESTIVAL_DATES.items():
            for start_date, end_date in [date_ranges]:
                start_month, start_day = start_date
                end_month, end_day = end_date
                
                # Handle year transitions
                if start_month <= month <= end_month or \
                   (start_month > end_month and (month >= start_month or month <= end_month)):
                    if start_month == end_month:
                        if start_day - 7 <= day <= end_day + 7:
                            return True
                    else:
                        # Year transition case
                        if month == start_month and day >= start_day - 7:
                            return True
                        elif month == end_month and day <= end_day + 7:
                            return True
                        elif start_month < month < end_month:
                            return True
        return False
    except:
        return False

def load_demo_data():
    """Load demo dataset"""
    try:
        df = pd.read_csv('demo_sales_data.csv')
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading demo data: {e}")
        return None

def load_data(uploaded_file=None):
    """Load data from uploaded file or demo dataset"""
    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            df['Date'] = pd.to_datetime(df['Date'])
            st.success("✅ File uploaded successfully!")
        else:
            df = load_demo_data()
            if df is not None:
                st.info("📊 Using Demo Dataset (Upload your own CSV to override)")
        
        if df is not None:
            # Initialize inventory from latest stock data
            latest_stock = df.groupby('Product')['Stock_Qty'].last().to_dict()
            st.session_state.inventory = latest_stock
            st.session_state.df = df
            st.session_state.data_loaded = True
            return df
        return None
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return None

def train_ai_model(df):
    """Train RandomForest model for sales prediction"""
    try:
        # Feature engineering
        df_model = df.copy()
        df_model['Year'] = df_model['Date'].dt.year
        df_model['Month'] = df_model['Date'].dt.month
        df_model['Day'] = df_model['Date'].dt.day
        df_model['DayOfWeek'] = df_model['Date'].dt.dayofweek
        
        models = {}
        for product in df['Product'].unique():
            product_data = df_model[df_model['Product'] == product].copy()
            
            if len(product_data) < 10:
                continue
            
            X = product_data[['Year', 'Month', 'Day', 'DayOfWeek']]
            y = product_data['Sales_Qty']
            
            if len(X) > 0:
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X, y)
                models[product] = model
        
        return models
    except Exception as e:
        st.error(f"❌ Error training model: {e}")
        return {}

def predict_sales(models, product, date):
    """Predict sales for a product on a specific date with festival boost"""
    try:
        if product not in models:
            return 50  # Default prediction
        
        model = models[product]
        features = [[date.year, date.month, date.day, date.weekday()]]
        prediction = model.predict(features)[0]
        
        # Apply festival boost (1.5x multiplier)
        if is_festival_period(date):
            prediction *= 1.5
            
        return max(0, int(prediction))
    except Exception as e:
        return 50

def get_stock_alerts(inventory, models):
    """Get low stock alerts by comparing current stock vs predicted sales"""
    alerts = []
    
    try:
        # Predict for next 7 days
        future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 8)]
        
        for product, current_stock in inventory.items():
            total_predicted = 0
            for date in future_dates:
                total_predicted += predict_sales(models, product, date)
            
            if current_stock < total_predicted:
                shortage = total_predicted - current_stock
                alerts.append({
                    'product': product,
                    'current_stock': current_stock,
                    'predicted_demand': total_predicted,
                    'shortage': shortage
                })
    except Exception as e:
        st.error(f"Error calculating alerts: {e}")
    
    return alerts

# ========== SIDEBAR NAVIGATION ==========
st.sidebar.title("🏪 Smart Retail System")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigate:",
    ["🏠 Dashboard", "🧮 Billing Calculator", "📦 Inventory Manager", "🤖 AI Predictions"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📤 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=['csv'])

# Load data
if uploaded_file is not None or not st.session_state.data_loaded:
    df = load_data(uploaded_file)
else:
    df = st.session_state.df

# ========== DASHBOARD ==========
if menu == "🏠 Dashboard":
    st.title("🏠 Sales Dashboard")
    
    if df is not None and st.session_state.data_loaded:
        # Train AI models
        models = train_ai_model(df)
        
        # Metrics Row
        col1, col2, col3 = st.columns(3)
        
        total_revenue = (df['Sales_Qty'] * df['Product'].map(PRODUCT_PRICES)).sum()
        total_products = len(st.session_state.inventory)
        alerts = get_stock_alerts(st.session_state.inventory, models)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h2>₹{total_revenue:,.0f}</h2>
                    <p>Total Revenue</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h2>{total_products}</h2>
                    <p>Total Products</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="alert-card">
                    <h2>{len(alerts)}</h2>
                    <p>Low Stock Alerts</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Low Stock Alerts
        if alerts:
            st.subheader("⚠️ Critical Stock Alerts")
            for alert in alerts:
                st.markdown(f"""
                    <div class="alert-card">
                        <h3>🚨 {alert['product']} - LOW STOCK WARNING</h3>
                        <p><strong>Current Stock:</strong> {alert['current_stock']} units</p>
                        <p><strong>Predicted Demand (Next 7 Days):</strong> {alert['predicted_demand']} units</p>
                        <p><strong>Shortage:</strong> {alert['shortage']} units</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"⚠️ Restock {alert['product']} Now", key=f"restock_{alert['product']}"):
                    st.success(f"✅ Restock order placed for {alert['product']}!")
        
        st.markdown("---")
        
        # Sales Trend Chart
        st.subheader("📈 Sales Trends")
        daily_sales = df.groupby('Date')['Sales_Qty'].sum().reset_index()
        fig_trend = px.line(
            daily_sales,
            x='Date',
            y='Sales_Qty',
            title='Daily Sales Trend',
            labels={'Sales_Qty': 'Total Sales Quantity', 'Date': 'Date'},
            template='plotly_white'
        )
        fig_trend.update_traces(line_color='#FF6B35', line_width=3)
        fig_trend.update_layout(
            title_font_size=20,
            title_font_color='#F7931E',
            hovermode='x unified'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Stock vs Demand Chart
        st.subheader("📊 Stock vs Predicted Demand")
        products = list(st.session_state.inventory.keys())
        current_stocks = [st.session_state.inventory[p] for p in products]
        predicted_demands = [sum([predict_sales(models, p, datetime.now() + timedelta(days=i)) 
                                  for i in range(1, 8)]) for p in products]
        
        fig_comparison = go.Figure()
        fig_comparison.add_trace(go.Bar(
            x=products,
            y=current_stocks,
            name='Current Stock',
            marker_color='#00CED1'
        ))
        fig_comparison.add_trace(go.Bar(
            x=products,
            y=predicted_demands,
            name='Predicted Demand (7 Days)',
            marker_color='#FF6B35'
        ))
        
        fig_comparison.update_layout(
            title='Stock vs Demand Comparison',
            xaxis_title='Product',
            yaxis_title='Quantity',
            barmode='group',
            template='plotly_white',
            title_font_size=20,
            title_font_color='#F7931E'
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    else:
        st.warning("⚠️ Please upload a CSV file or wait for demo data to load.")

# ========== BILLING CALCULATOR ==========
elif menu == "🧮 Billing Calculator":
    st.title("🧮 Smart Billing Calculator")
    
    if st.session_state.data_loaded and st.session_state.inventory:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("🛒 Add Products to Cart")
            
            products = list(st.session_state.inventory.keys())
            selected_product = st.selectbox("Select Product", products, key="product_select")
            
            max_qty = st.session_state.inventory.get(selected_product, 0)
            st.info(f"📦 Available Stock: {max_qty} units")
            
            quantity = st.number_input(
                "Enter Quantity",
                min_value=1,
                max_value=max_qty if max_qty > 0 else 1,
                value=1,
                step=1,
                key="qty_input"
            )
            
            price_per_unit = PRODUCT_PRICES.get(selected_product, 0)
            item_total = quantity * price_per_unit
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("➕ Add to Cart", use_container_width=True):
                    if quantity > max_qty:
                        st.error(f"❌ Insufficient stock! Only {max_qty} units available.")
                    elif quantity <= 0:
                        st.error("❌ Quantity must be greater than 0!")
                    else:
                        # Add to cart
                        st.session_state.billing_cart.append({
                            'product': selected_product,
                            'quantity': quantity,
                            'price_per_unit': price_per_unit,
                            'total': item_total
                        })
                        st.success(f"✅ Added {quantity}x {selected_product} to cart!")
                        st.rerun()
            
            with col_b:
                if st.button("🗑️ Clear Cart", use_container_width=True):
                    st.session_state.billing_cart = []
                    st.success("🗑️ Cart cleared!")
                    st.rerun()
            
            st.markdown("---")
            
            # Shopping Cart Display
            st.subheader("🛒 Shopping Cart")
            
            if st.session_state.billing_cart:
                for idx, item in enumerate(st.session_state.billing_cart):
                    col_item, col_remove = st.columns([4, 1])
                    
                    with col_item:
                        st.markdown(f"""
                            <div class="cart-card">
                                <h4>{item['product']}</h4>
                                <p>Quantity: {item['quantity']} × ₹{item['price_per_unit']} = ₹{item['total']}</p>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col_remove:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if st.button("❌", key=f"remove_{idx}"):
                            st.session_state.billing_cart.pop(idx)
                            st.rerun()
                
                # Calculate Grand Total
                grand_total = sum([item['total'] for item in st.session_state.billing_cart])
                
                st.markdown(f"""
                    <div class="success-card">
                        <h3>Final Bill</h3>
                        <h2>Grand Total: ₹{grand_total}</h2>
                        <p>Items in Cart: {len(st.session_state.billing_cart)}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("💰 Generate Bill & Checkout", use_container_width=True, type="primary"):
                    # Auto-deduct stock for all items
                    bill_details = []
                    for item in st.session_state.billing_cart:
                        product = item['product']
                        qty = item['quantity']
                        
                        # Deduct from inventory
                        if product in st.session_state.inventory:
                            old_stock = st.session_state.inventory[product]
                            st.session_state.inventory[product] -= qty
                            bill_details.append(f"- {product}: {qty} units (Stock: {old_stock} → {st.session_state.inventory[product]})")
                    
                    # Show success message
                    st.success(f"""
                        ✅ **Bill Generated Successfully!**
                        
                        📝 **Bill Details:**
                        - Total Items: {len(st.session_state.billing_cart)}
                        - Grand Total: ₹{grand_total}
                        
                        📦 **Stock Updated:**
                        \n"""+"\n".join(bill_details))
                    
                    # Clear cart after checkout
                    st.session_state.billing_cart = []
                    
                    # Show confetti effect
                    st.balloons()
                    st.rerun()
            else:
                st.info("🛒 Your cart is empty. Add products to get started!")
        
        with col2:
            st.subheader("📋 Price List")
            price_df = pd.DataFrame(list(PRODUCT_PRICES.items()), columns=['Product', 'Price (₹)'])
            st.dataframe(price_df, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ Please load data first from the sidebar.")

# ========== INVENTORY MANAGER ==========
elif menu == "📦 Inventory Manager":
    st.title("📦 Inventory Manager")
    
    if st.session_state.data_loaded and st.session_state.inventory:
        st.subheader("Current Stock Levels")
        
        inventory_df = pd.DataFrame(
            list(st.session_state.inventory.items()),
            columns=['Product', 'Current Stock']
        )
        
        # Add color coding
        def highlight_low_stock(row):
            if row['Current Stock'] < 50:
                return ['background-color: #FF1744; color: white'] * len(row)
            elif row['Current Stock'] < 100:
                return ['background-color: #FFA500; color: black'] * len(row)
            else:
                return ['background-color: #00CED1; color: white'] * len(row)
        
        styled_df = inventory_df.style.apply(highlight_low_stock, axis=1)
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Update Stock
        st.subheader("🔄 Update Stock")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            product_to_update = st.selectbox("Select Product", list(st.session_state.inventory.keys()))
        
        with col2:
            new_stock = st.number_input(
                "New Stock Quantity",
                min_value=0,
                value=st.session_state.inventory[product_to_update],
                step=1
            )
        
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Update Stock", use_container_width=True):
                old_stock = st.session_state.inventory[product_to_update]
                st.session_state.inventory[product_to_update] = new_stock
                st.success(f"✅ Stock updated for {product_to_update}: {old_stock} → {new_stock} units")
                st.rerun()
    else:
        st.warning("⚠️ Please load data first from the sidebar.")

# ========== AI PREDICTIONS ==========
elif menu == "🤖 AI Predictions":
    st.title("🤖 AI Sales Predictions")
    
    if st.session_state.data_loaded and df is not None:
        # Train models
        models = train_ai_model(df)
        
        st.subheader("📅 Predict Future Sales")
        
        col1, col2 = st.columns(2)
        
        with col1:
            predict_product = st.selectbox("Select Product", df['Product'].unique())
        
        with col2:
            predict_date = st.date_input(
                "Select Date",
                value=datetime.now() + timedelta(days=7),
                min_value=datetime.now(),
                max_value=datetime.now() + timedelta(days=90)
            )
        
        if st.button("🔮 Predict Sales", use_container_width=True):
            prediction = predict_sales(models, predict_product, predict_date)
            is_festival = is_festival_period(predict_date)
            
            if is_festival:
                st.markdown(f"""
                    <div class="alert-card">
                        <h2>🎉 FESTIVAL BOOST APPLIED! 🎉</h2>
                        <h3>Predicted Sales for {predict_product}</h3>
                        <h1>{prediction} units</h1>
                        <p>Date: {predict_date.strftime('%Y-%m-%d')}</p>
                        <p><strong>Festival period detected! Prediction boosted by 1.5x</strong></p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="success-card">
                        <h3>Predicted Sales for {predict_product}</h3>
                        <h1>{prediction} units</h1>
                        <p>Date: {predict_date.strftime('%Y-%m-%d')}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 7-Day Forecast
        st.subheader("📊 7-Day Sales Forecast")
        forecast_product = st.selectbox("Select Product for Forecast", df['Product'].unique(), key='forecast')
        
        future_dates = [datetime.now() + timedelta(days=i) for i in range(1, 8)]
        forecasts = [predict_sales(models, forecast_product, date) for date in future_dates]
        
        forecast_df = pd.DataFrame({
            'Date': [d.strftime('%Y-%m-%d') for d in future_dates],
            'Predicted Sales': forecasts,
            'Festival Boost': [is_festival_period(d) for d in future_dates]
        })
        
        # Highlight festival dates
        def highlight_festivals(row):
            if row['Festival Boost']:
                return ['background-color: #FFB6C1; color: white'] * len(row)
            return [''] * len(row)
        
        styled_forecast = forecast_df.style.apply(highlight_festivals, axis=1)
        st.dataframe(styled_forecast, use_container_width=True, hide_index=True)
        
        # Forecast Chart
        fig_forecast = px.line(
            forecast_df,
            x='Date',
            y='Predicted Sales',
            title=f'7-Day Sales Forecast for {forecast_product}',
            markers=True,
            template='plotly_white'
        )
        fig_forecast.update_traces(line_color='#FF6B35', line_width=3, marker_size=10)
        fig_forecast.update_layout(
            title_font_size=20,
            title_font_color='#F7931E',
            hovermode='x unified'
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
    else:
        st.warning("⚠️ Please load data first from the sidebar.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='text-align: center; color: #F7931E;'>
        <h4>🏪 Smart Retail Intelligence</h4>
        <p>Powered by AI 🤖</p>
    </div>
""", unsafe_allow_html=True)
