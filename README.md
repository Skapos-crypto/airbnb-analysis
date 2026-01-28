# 🏠 Airbnb Pricing Analysis Dashboard

An interactive web dashboard analyzing pricing patterns across 52,810 Airbnb listings in 10 major European cities.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Dash](https://img.shields.io/badge/Dash-3.4.0-green)
![Plotly](https://img.shields.io/badge/Plotly-6.5.2-orange)

## 📊 Features

- **Real-time Analytics**: Comprehensive analysis of pricing trends
- **Tourism Impact**: Correlation between tourism pressure and pricing
- **Location Intelligence**: Distance-based pricing analysis (city center, metro, airport)
- **Interactive Visualizations**: 9 dynamic charts and graphs
- **Multi-city Comparison**: Compare pricing across 10 European destinations

## 🌍 Cities Covered

Amsterdam, Athens, Barcelona, Berlin, Budapest, Lisbon, Paris, Rome, Vienna, and more!

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/airbnb-dashboard.git
   cd airbnb-dashboard
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   python dashboard.py
   ```

4. **Open your browser**
   Navigate to: http://127.0.0.1:8050

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to:
- Render
- Heroku
- Railway
- Docker
- PythonAnywhere

## 📦 Project Structure

```
orange_hackthon/
├── dashboard.py          # Main dashboard application
├── build_dataset.py      # Data preprocessing script
├── dataset.csv           # Main dataset (52,810 listings)
├── merged_dataset.csv    # Merged dataset with additional features
├── requirements.txt      # Python dependencies
├── Procfile             # For Heroku/Render deployment
├── render.yaml          # Render configuration
├── DEPLOYMENT.md        # Deployment guide
└── README.md            # This file
```

## 📈 Dashboard Sections

1. **Key Metrics Dashboard**
   - Total listings, cities, average prices, features

2. **Tourism Demand Analysis**
   - Tourism pressure ratio vs pricing correlation
   - Scatter plot with city comparisons

3. **Location & Accessibility**
   - Distance from city center analysis
   - Metro station proximity impact
   - Airport distance effects

4. **Price Distribution**
   - City-by-city comparisons
   - Box plots with statistical distributions
   - Price per person by room type

5. **Correlation Analysis**
   - Heatmap of feature correlations
   - Key pricing drivers

## 🛠️ Technologies Used

- **Python 3.12**: Core programming language
- **Dash 3.4**: Web framework
- **Plotly 6.5**: Interactive visualizations
- **Pandas 3.0**: Data manipulation
- **NumPy 2.4**: Numerical computing

## 📊 Dataset Information

- **Total Listings**: 52,810
- **Cities**: 10 European destinations
- **Features**: 30 variables including:
  - Price metrics
  - Location data
  - Tourism statistics
  - Guest satisfaction scores
  - Accessibility metrics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

Created for the Orange Hackathon

## 🙏 Acknowledgments

- Airport data from OpenFlights.org
- Tourism statistics from official city databases
- Airbnb public dataset

---

**Ready to deploy?** Check out [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions!
