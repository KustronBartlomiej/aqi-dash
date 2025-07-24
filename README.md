# 🌍 Global Air Quality Index (AQI) Dashboard

An interactive dashboard built using **Dash** and **Plotly** to visualize global air quality data from a CSV dataset.

## 🚀 Features

- Interactive world map with AQI (Air Quality Index) levels by city
- AQI category color-coded visualization
- Click on a city to view the breakdown of AQI components:
  - PM2.5
  - Ozone
  - NO₂
  - CO
- Summary statistics including:
  - Global average AQI
  - Number of cities in the dataset

## 🗂 Dataset

The dataset used must be in CSV format and contain the following columns:

- `City`
- `AQI Value`
- `AQI Category`
- `lat` (latitude)
- `lng` (longitude)
- `PM2.5 AQI Value`
- `Ozone AQI Value`
- `NO2 AQI Value`
- `CO AQI Value`

## 📦 Requirements

Install dependencies using pip:

```bash
pip install dash pandas plotly
