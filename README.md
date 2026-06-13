# 💱 Real-Time Currency Converter

A multilingual web application built with **Flask** that converts currencies in real time using the [ExchangeRate-API](https://www.exchangerate-api.com/), supporting 30+ currencies and 11 languages.

## ✨ Features

- 🌐 **Multilingual UI** — English, Hindi, Kannada, Spanish, French, German, Chinese, Arabic, Japanese, Russian, and Portuguese
- 💱 **Real-time conversion** for 30+ currencies using live exchange rates
- 📜 **Conversion history** tracked per session
- 📥 **CSV export** of conversion history
- 🎨 Clean, responsive UI with GMU-branded styling

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, Jinja2 templates, CSS
- **API:** [ExchangeRate-API v6](https://www.exchangerate-api.com/)
- **Deployment:** Gunicorn (Procfile included for platforms like Heroku/Render)

## 📂 Project Structure

```
.
├── Real_Time_Currency_Converter.py   # Main Flask application
├── requirements.txt                  # Python dependencies
├── Procfile                          # Deployment entry point
├── static/
│   └── style.css                     # App styling
└── templates/
    ├── language.html                 # Language selection page
    ├── index.html                    # Currency converter form
    ├── result.html                   # Conversion result + history
    └── error.html                    # Error page
```

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key**

   Get a free API key from [ExchangeRate-API](https://www.exchangerate-api.com/) and replace the `API_KEY` value in `Real_Time_Currency_Converter.py`:
   ```python
   API_KEY = "your_api_key_here"
   ```

5. **Run the app**
   ```bash
   python Real_Time_Currency_Converter.py
   ```

   The app will be available at `http://127.0.0.1:5000/`

## 🚀 Deployment

This project includes a `Procfile` for deployment with Gunicorn:
```
web: gunicorn Real_Time_Currency_Converter:app
```

It can be deployed directly to platforms like **Render**, **Heroku**, or **Railway**.

## 🔄 How It Works

1. User selects a preferred language on the home page.
2. User selects "From" and "To" currencies along with an amount.
3. The app fetches live exchange rates from ExchangeRate-API.
4. The converted value is displayed, and the conversion is added to the session history.
5. Users can download their conversion history as a CSV file.

## 📚 Project Information

This project is part of a **Project-Based Learning (PBL)** initiative by a student of [GM University, Davangere](https://gmu.ac.in).

- 📽️ **Demo Video:** [Watch on YouTube](https://youtu.be/dujdUix0awc?si=M9-dPmXrLbyQuzER)
- 📁 **Project Files:** [Google Drive](https://drive.google.com/drive/folders/1okWNH4Lq5AuxkBoUjLjdnAESTdRSKkp6)

## 📄 License

This project is for educational purposes as part of academic coursework.

Aditya Basavaraj, CSE DEPARTMENT, GM UNIVERSITY, DAVANGERE
