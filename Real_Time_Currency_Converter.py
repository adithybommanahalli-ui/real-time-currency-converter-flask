from flask import Flask, render_template, request, session, redirect, url_for, send_file
import requests, csv, io

#Create Flask Application
app = Flask(__name__)
app.secret_key = 'your_secret_key' #Used for storing session data securely

API_KEY = "9811d61fe134d22905215755" #Your API key for exchangerate-api.com

#List of supported currencies (code, name, country)
currencies = [
    ('AED','UAE Dirham','United Arab Emirates'),('AUD','Australian Dollar','Australia'),
    ('BDT','Bangladeshi Taka','Bangladesh'),('BRL','Brazilian Real','Brazil'),
    ('CAD','Canadian Dollar','Canada'),('CHF','Swiss Franc','Switzerland'),
    ('CNY','Chinese Renminbi','China'),('DKK','Danish Krone','Denmark'),
    ('EGP','Egyptian Pound','Egypt'),('EUR','Euro','European Union'),
    ('GBP','Pound Sterling','United Kingdom'),('HKD','Hong Kong Dollar','Hong Kong'),
    ('IDR','Indonesian Rupiah','Indonesia'),('INR','Indian Rupee','India'),
    ('JPY','Japanese Yen','Japan'),('KRW','South Korean Won','South Korea'),
    ('MXN','Mexican Peso','Mexico'),('MYR','Malaysian Ringgit','Malaysia'),
    ('NOK','Norwegian Krone','Norway'),('NZD','New Zealand Dollar','New Zealand'),
    ('PKR','Pakistani Rupee','Pakistan'),('PLN','Polish Złoty','Poland'),
    ('RUB','Russian Ruble','Russia'),('SAR','Saudi Riyal','Saudi Arabia'),
    ('SEK','Swedish Krona','Sweden'),('SGD','Singapore Dollar','Singapore'),
    ('THB','Thai Baht','Thailand'),('TRY','Turkish Lira','Turkey'),
    ('USD','United States Dollar','United States'),('VND','Vietnamese Đồng','Vietnam'),
    ('ZAR','South African Rand','South Africa')
]

#Available languages and their names
languages = {
    "kn":"Kannada","en":"English","hi":"Hindi","es":"Spanish","fr":"French","de":"German",
    "zh-cn":"Chinese (Simplified)","ar":"Arabic","ja":"Japanese","ru":"Russian",
    "pt":"Portuguese"
}

#Translations for different languages
translations = {
    "en":{
        "title":"Currency Converter","heading":"Convert Currency",
        "from_currency":"From Currency","to_currency":"To Currency",
        "amount":"Amount","convert_button":"Convert",
        "history":"Conversion History","download":"Download CSV","back":"← Back",
        "error":"An error occurred"
    },
    "hi":{
        "title":"मुद्रा परिवर्तक","heading":"मुद्रा बदलें",
        "from_currency":"से मुद्रा","to_currency":"मुद्रा में",
        "amount":"राशि","convert_button":"बदलें",
        "history":"परिवर्तन इतिहास","download":"CSV डाउनलोड करें","back":"← वापिस",
        "error":"त्रुटि हुई"
    },
    "es":{
        "title":"Convertidor de Moneda","heading":"Convertir Moneda",
        "from_currency":"De","to_currency":"A",
        "amount":"Cantidad","convert_button":"Convertir",
        "history":"Historial de Conversión","download":"Descargar CSV","back":"← Atrás",
        "error":"Ocurrió un error"
    },
    "fr":{
        "title":"Convertisseur de Devises","heading":"Convertir une Devise",
        "from_currency":"De","to_currency":"À",
        "amount":"Montant","convert_button":"Convertir",
        "history":"Historique des Conversions","download":"Télécharger CSV","back":"← Retour",
        "error":"Une erreur s'est produite"
    },
    "de":{
        "title":"Währungsrechner","heading":"Währung umrechnen",
        "from_currency":"Von","to_currency":"Zu",
        "amount":"Betrag","convert_button":"Umrechnen",
        "history":"Konvertierungshistorie","download":"CSV herunterladen","back":"← Zurück",
        "error":"Ein Fehler ist aufgetreten"
    },
    "zh-cn":{
        "title":"货币转换器","heading":"转换货币",
        "from_currency":"从","to_currency":"到",
        "amount":"金额","convert_button":"转换",
        "history":"转换历史","download":"下载 CSV","back":"← 返回",
        "error":"发生错误"
    },
    "ar":{
        "title":"محول العملات","heading":"تحويل العملة",
        "from_currency":"من","to_currency":"إلى",
        "amount":"المبلغ","convert_button":"تحويل",
        "history":"تاريخ التحويل","download":"تنزيل CSV","back":"← رجوع",
        "error":"حدث خطأ"
    },
    "ja":{
        "title":"通貨コンバーター","heading":"通貨を変換",
        "from_currency":"から","to_currency":"へ",
        "amount":"金額","convert_button":"変換",
        "history":"変換履歴","download":"CSVをダウンロード","back":"← 戻る",
        "error":"エラーが発生しました"
    },
    "ru":{
        "title":"Конвертер валют","heading":"Преобразовать валюту",
        "from_currency":"Из","to_currency":"В",
        "amount":"Сумма","convert_button":"Конвертировать",
        "history":"История конверсии","download":"Скачать CSV","back":"← Назад",
        "error":"Произошла ошибка"
    },
    "pt":{
        "title":"Conversor de Moedas","heading":"Converter Moeda",
        "from_currency":"De","to_currency":"Para",
        "amount":"Quantia","convert_button":"Converter",
        "history":"Histórico de Conversões","download":"Baixar CSV","back":"← Voltar",
        "error":"Ocorreu um erro"
    },
    "kn":{
        "title":"ಕರೆನ್ಸಿ ಪರಿವರ್ತಕ","heading":"ಕರೆನ್ಸಿ ಪರಿವರ್ತಿಸಿ",
        "from_currency":"ಇಂದ","to_currency":"ಗೆ",
        "amount":"ಮೊತ್ತ","convert_button":"ಪರಿವರ್ತನೆ",
        "history":"ಪರಿವರ್ತನೆ ಇತಿಹಾಸ","download":"CSV ಡೌನ್‌ಲೋಡ್","back":"← ಹಿಂತೆಗೆದುಕೊಳ್ಳಿ",
        "error":"ದೋಷವಾಗಾಯಿತು"
    }
}

# Home route: language selection page
@app.route('/')
def language_selection():
    return render_template("language.html", languages=languages)

# Converter form route
@app.route('/converter')
def converter_page():
    lang = request.args.get('lang', 'en')  # Default to English
    session['lang'] = lang  # Save selected language in session
    texts = translations[lang]  # Load translated text
    return render_template("index.html", currencies=currencies, texts=texts, lang=lang)

# Main conversion logic
@app.route('/convert', methods=['POST'])
def convert():
    lang = session.get('lang', 'en')
    texts = translations[lang]

    # Get form input values
    frm = request.form['from_currency']
    to = request.form['to_currency']
    amt_input = request.form['amount']

# Validation: ensure amount is a positive number
    try:
        amt = float(amt_input)
        if amt <= 0:
            raise ValueError("Amount must be positive.")
    except ValueError:
        return render_template(
            "error.html",
            error=f"{texts['error']}: Invalid or negative amount.",
            texts=texts,
            lang=lang
        )
# Call the exchange rate API
    r = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{frm}").json()

    # Check if data is valid
    if r.get('result') != 'success' or to not in r['conversion_rates']:
        return render_template("error.html", error=texts['error'], texts=texts, lang=lang)

    rate = r['conversion_rates'][to]
    conv = round(rate * amt, 2)  # Calculate converted value
    res_str = f"{amt} {frm} = {conv} {to}"  # Display format

    # Save to session history
    hist = session.get('history', [])
    hist.append({'from': frm, 'to': to, 'amount': amt, 'converted': conv})
    session['history'] = hist

    # Render result template with result and history
    return render_template("result.html", result=res_str, history=hist, texts=texts, lang=lang)

# Download conversion history as CSV
@app.route('/download')
def download():
    lang = session.get('lang', 'en')
    hist = session.get('history', [])

    if not hist:
        return redirect(url_for('converter_page', lang=lang))

    # Create in-memory CSV
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(['From', 'To', 'Amount', 'Converted'])
    for e in hist:
        w.writerow([e['from'], e['to'], e['amount'], e['converted']])
    buf.seek(0)

    # Send the file as downloadable response
    return send_file(io.BytesIO(buf.read().encode()),
                     download_name='history.csv',
                     as_attachment=True,
                     mimetype='text/csv')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

#682