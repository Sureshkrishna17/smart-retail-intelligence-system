# 🏪 Smart Retail Intelligence System

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> An AI-powered retail management system designed for small shopkeepers in India with sales prediction, inventory tracking, and intelligent stock alerts.

---

## ✨ Features

### 🧮 Smart Billing Calculator
- **Multi-Product Shopping Cart** - Add multiple items before checkout
- **Auto-Deduct Stock** - Inventory automatically updates after billing
- **Real-time Stock Validation** - Prevents overselling
- **Beautiful UI** - Pink gradient cart cards with easy-to-use interface

### 🤖 AI Sales Prediction
- **RandomForest ML Model** - Accurate sales forecasting
- **Festival Boost Logic** - Automatic 1.5x multiplier for Indian festivals (Diwali, Pongal, New Year)
- **7-Day Forecast** - View predictions for the week ahead
- **Product-Specific Predictions** - Tailored forecasts for each item

### 📊 Interactive Dashboard
- **Sales Trends Visualization** - Interactive Plotly line charts
- **Stock vs Demand Analysis** - Compare inventory with predicted needs
- **Key Metrics Display** - Total revenue, product count, and alerts
- **Real-time Updates** - Live data synchronization

### ⚠️ Intelligent Stock Alerts
- **Low Stock Warnings** - Bright RED alerts when stock < predicted demand
- **7-Day Prediction Comparison** - Proactive restocking notifications
- **Visual Indicators** - Color-coded stock levels (Red/Orange/Teal)

### 📦 Inventory Manager
- **Color-Coded Stock Levels** - Instant visual stock status
- **Easy Stock Updates** - Simple interface for restocking
- **Live Inventory Tracking** - Real-time stock synchronization

---

## 🎨 UI Design

**Vibrant Color Scheme:**
- 🧡 **Primary:** Orange Gradient (#FF6B35 → #F7931E)
- 💚 **Secondary:** Teal/Turquoise (#00CED1)
- ❤️ **Alerts:** Bright Red (#FF1744)
- 💗 **Cart:** Pink Gradient (#FFB6C1 → #FF69B4)

**Design Philosophy:**
- Clean, modern interface
- Simple language (no technical jargon)
- Large touch targets for easy use
- Responsive design

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Sureshkrishna17/smart-retail-intelligence-system.git
cd smart-retail-intelligence-system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
- The app will automatically open at `http://localhost:8501`
- Or manually navigate to the URL shown in terminal

---

## 📖 Usage Guide

### Quick Start

1. **Dashboard** - View sales trends and stock alerts
2. **Billing Calculator** - Add products to cart and generate bills
3. **Inventory Manager** - Monitor and update stock levels
4. **AI Predictions** - Forecast future sales

### Billing Workflow

1. Navigate to **"🧮 Billing Calculator"**
2. Select product from dropdown
3. Enter quantity
4. Click **"➕ Add to Cart"**
5. Repeat for more products
6. Review cart
7. Click **"💰 Generate Bill & Checkout"**
8. Stock automatically updates! ✅

### AI Prediction Workflow

1. Navigate to **"🤖 AI Predictions"**
2. Select product
3. Choose future date
4. Click **"🔮 Predict Sales"**
5. View prediction with festival boost indicator
6. Check 7-day forecast below

---

## 📁 Project Structure

```
smart-retail-intelligence-system/
│
├── app.py                    # Main Streamlit application
├── demo_sales_data.csv       # Demo dataset (2 months of sales data)
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── .gitignore               # Git ignore rules
```

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.8+
- **ML Model:** Scikit-learn (RandomForestRegressor)
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly
- **Deployment:** Streamlit Cloud compatible

---

## 📊 Dataset

The demo dataset includes:
- **Duration:** 2 months (Nov-Dec 2025)
- **Products:** 8 common retail items
  - Rice, Wheat, Sugar, Tea, Oil, Biscuits, Soap, Shampoo
- **Records:** 336 daily sales entries
- **Columns:** Date, Product, Sales_Qty, Stock_Qty

---

## 🎯 Business Value

- ✅ **Prevents Stock-Outs** - Proactive alerts before running out
- ✅ **Maximizes Festival Revenue** - 1.5x boost predictions for peak seasons
- ✅ **Saves Time** - Auto-deduct stock reduces manual work
- ✅ **Easy to Use** - Designed for non-technical shopkeepers
- ✅ **Data-Driven Decisions** - AI-powered forecasting

---

## 🎓 Academic Project

This is a **Final Year Project** demonstrating:
- Machine Learning integration
- Real-time data processing
- Interactive web applications
- Business problem solving
- User-centered design

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Sureshkrishna**
- GitHub: [@Sureshkrishna17](https://github.com/Sureshkrishna17)
- Repository: [smart-retail-intelligence-system](https://github.com/Sureshkrishna17/smart-retail-intelligence-system)

---

## 🙏 Acknowledgments

- Built with ❤️ for small shopkeepers in India
- Powered by AI and modern web technologies
- Designed for simplicity and ease of use

---

## 📸 Screenshots

*Add screenshots of your application here after uploading*

---

## 🔮 Future Enhancements

- [ ] SMS/WhatsApp alerts for low stock
- [ ] Multi-language support (Hindi, Tamil, etc.)
- [ ] Barcode scanner integration
- [ ] Cloud database integration
- [ ] Mobile app version
- [ ] Customer loyalty program
- [ ] Expense tracking

---

**⭐ If you find this project useful, please give it a star!**

---

Made with ❤️ by Sureshkrishna for making retail smarter in India 🇮🇳
