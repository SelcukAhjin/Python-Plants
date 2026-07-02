# 🌿 Flower Power At Your Hour

A Python-based mobile application built with the Flet framework. This smart botanical assistant helps users look up specific care requirements for common house plants and cross-references them with live, location-based weather data to provide actionable care alerts.

## 🌟 Key Features

*   **Smart Botanical Search:** Search for everyday house plants (e.g., Monstera, Ficus, Aloe Vera) to retrieve their botanical names, sun requirements, and temperature tolerances.
*   **Live Weather Integration:** Fetches real-time weather data and a 5-day forecast for any global city.
*   **Dynamic Alert System:** Automatically compares the current local temperature with the optimal temperature range of the selected plant. It triggers visual warnings and actionable care tips if conditions are too hot or too cold.
*   **Asynchronous Architecture:** Utilizes native Flet threading (`page.run_thread()`) for non-blocking API calls, ensuring a fluid mobile user interface with smooth loading animations.
*   **My Garden (Upcoming):** A dedicated tab to save and manage favorite plants in a personal digital garden.

## 🛠️ Tech Stack & Architecture

*   **Language:** Python 3.x
*   **Frontend UI:** Flet (Flutter-based cross-platform UI framework)
*   **Backend:** `requests` library for RESTful API communication
*   **Concurrency:** Native Flet thread handling to prevent UI freezing during network requests.

## 🔑 API Keys & Prerequisites

To run this application locally, you will need **two separate API keys**:

1.  **Weather Data (OpenWeatherMap):**
    *   Used for real-time temperature and forecast data.
    *   Get your key at: [OpenWeatherMap](https://openweathermap.org/api)
2.  **Plant Database (RapidAPI - House Plants API):**
    *   Used to fetch botanical information and temperature tolerances.
    *   This project uses the Pro version of the API.
    *   Get your key at: [House Plants API on RapidAPI](https://rapidapi.com/mnai01/api/house-plants2)

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SelcukAhjin/Python-Plants