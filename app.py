from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
import logging

app = Flask(__name__)
app.secret_key = 'yg-auto-secret-key-2024'

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# База данных автомобилей
cars_db = [
    {
        'id': 1,
        'brand': 'BMW',
        'model': 'X5',
        'year': 2023,
        'price': 8500000,
        'image': 'bmw_x5.png',
        'specs': {
            'engine': '3.0L',
            'power': '249 л.с.',
            'acceleration': '6.5с',
            'fuel': '8.1л/100км'
        },
        'badge': 'Новинка',
        'description': 'Премиальный внедорожник с полным комплектом опций'
    },
    {
        'id': 2,
        'brand': 'Audi',
        'model': 'A6',
        'year': 2022,
        'price': 5200000,
        'image': 'audi_a6.png',
        'specs': {
            'engine': '2.0L',
            'power': '245 л.с.',
            'acceleration': '7.1с',
            'fuel': '7.8л/100км'
        },
        'badge': 'Хит',
        'description': 'Бизнес-седан с инновационными технологиями'
    },
    {
        'id': 3,
        'brand': 'Mercedes',
        'model': 'E-Class',
        'year': 2023,
        'price': 7200000,
        'image': 'mercedes_eclass.png',
        'specs': {
            'engine': '2.0L',
            'power': '258 л.с.',
            'acceleration': '6.8с',
            'fuel': '8.2л/100км'
        },
        'badge': 'Премиум',
        'description': 'Роскошный седан премиум-класса'
    },
    {
        'id': 4,
        'brand': 'Toyota',
        'model': 'Camry',
        'year': 2024,
        'price': 3200000,
        'image': 'toyota_camry.png',
        'specs': {
            'engine': '2.5L',
            'power': '181 л.с.',
            'acceleration': '8.9с',
            'fuel': '7.1л/100км'
        },
        'badge': 'Надежный',
        'description': 'Комфортабельный седан с отличной экономичностью'
    },
    {
        'id': 5,
        'brand': 'Lada',
        'model': 'Vesta',
        'year': 2024,
        'price': 1500000,
        'image': 'lada_vesta.png',
        'specs': {
            'engine': '1.6L',
            'power': '106 л.с.',
            'acceleration': '11.5с',
            'fuel': '6.9л/100км'
        },
        'badge': 'Выгодно',
        'description': 'Популярный отечественный седан'
    }
]


@app.route('/')
def home():
    """Главная страница"""
    return render_template('index.html')


@app.route('/cars')
def cars():
    """Страница каталога автомобилей"""
    brand_filter = request.args.get('brand', 'all')
    price_filter = request.args.get('price', 'all')
    year_filter = request.args.get('year', 'all')
    type_filter = request.args.get('type', 'all')

    filtered_cars = cars_db.copy()

    # Фильтрация по марке
    if brand_filter != 'all':
        filtered_cars = [car for car in filtered_cars if car['brand'].lower() == brand_filter.lower()]

    # Фильтрация по цене
    if price_filter != 'all':
        if price_filter == '1-2':
            filtered_cars = [car for car in filtered_cars if 1000000 <= car['price'] <= 2000000]
        elif price_filter == '2-5':
            filtered_cars = [car for car in filtered_cars if 2000000 <= car['price'] <= 5000000]
        elif price_filter == '5+':
            filtered_cars = [car for car in filtered_cars if car['price'] > 5000000]

    # Фильтрация по году
    if year_filter != 'all':
        if year_filter == '2023-2024':
            filtered_cars = [car for car in filtered_cars if car['year'] >= 2023]
        elif year_filter == '2020-2022':
            filtered_cars = [car for car in filtered_cars if 2020 <= car['year'] <= 2022]
        elif year_filter == '2017-2019':
            filtered_cars = [car for car in filtered_cars if 2017 <= car['year'] <= 2019]

    return render_template('cars.html',
                           cars=filtered_cars,
                           current_filters={
                               'brand': brand_filter,
                               'price': price_filter,
                               'year': year_filter,
                               'type': type_filter
                           })


@app.route('/about')
def about():
    """Страница о компании"""
    team_members = [
        {
            'name': 'Александр Петров',
            'role': 'Генеральный директор',
            'experience': '10 лет в автомобильном бизнесе',
            'avatar': '👨‍💼'
        },
        {
            'name': 'Мария Иванова',
            'role': 'Финансовый директор',
            'experience': 'MBA, 8 лет опыта',
            'avatar': '👩‍💼'
        },
        {
            'name': 'Дмитрий Сидоров',
            'role': 'Технический директор',
            'experience': '15 лет экспертизы',
            'avatar': '👨‍🔧'
        }
    ]

    certificates = [
        {'name': 'Лучший автосалон 2023', 'description': 'Награда от Ассоциации автодилеров'},
        {'name': 'Сертификат качества', 'description': 'ISO 9001:2015'},
        {'name': 'Партнер года', 'description': 'Официальный дилер BMW'},
        {'name': 'Выбор покупателей', 'description': 'По версии Auto.Ru 2023'}
    ]

    return render_template('about.html',
                           team_members=team_members,
                           certificates=certificates)


@app.route('/evaluate', methods=['GET', 'POST'])
def evaluate_car():
    """Форма оценки автомобиля"""
    if request.method == 'POST':
        brand = request.form.get('brand', '').strip()
        model = request.form.get('model', '').strip()
        year = request.form.get('year', '').strip()
        mileage = request.form.get('mileage', '').strip()
        condition = request.form.get('condition', '').strip()
        phone = request.form.get('phone', '').strip()
        additional_info = request.form.get('additional_info', '').strip()

        if not all([brand, model, year, phone]):
            flash('Пожалуйста, заполните все обязательные поля', 'error')
            return redirect(url_for('evaluate_car'))

        logger.info(f"Новая заявка на оценку: {brand} {model} {year}, тел: {phone}")

        message = f"""
📋 НОВАЯ ЗАЯВКА НА ОЦЕНКУ АВТО

🚗 Марка: {brand}
🔧 Модель: {model}
📅 Год: {year}
🛣️ Пробег: {mileage if mileage else 'Не указан'}
⭐ Состояние: {get_condition_text(condition)}
📞 Телефон: {phone}

💬 Доп. информация: {additional_info if additional_info else 'Не указана'}

🕒 Время заявки: {datetime.now().strftime('%d.%m.%Y %H:%M')}
        """

        send_notification(message)
        flash('Спасибо! Мы свяжемся с вами в течение 15 минут для оценки автомобиля.', 'success')
        return redirect(url_for('evaluate_car'))

    return render_template('evaluate.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Форма обратной связи"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, phone, message]):
            flash('Пожалуйста, заполните все поля', 'error')
            return redirect(url_for('contact'))

        logger.info(f"Новое сообщение от {name}: {phone} - {message}")

        notification_message = f"""
📩 НОВОЕ СООБЩЕНИЕ С САЙТА

👤 Имя: {name}
📞 Телефон: {phone}

💬 Сообщение:
{message}

🕒 Время: {datetime.now().strftime('%d.%m.%Y %H:%M')}
        """

        send_notification(notification_message)
        flash('Сообщение отправлено! Мы ответим вам в ближайшее время.', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


def get_condition_text(condition):
    conditions = {
        'excellent': 'Отличное',
        'good': 'Хорошее',
        'satisfactory': 'Удовлетворительное',
        'needs_repair': 'Требует ремонта'
    }
    return conditions.get(condition, 'Не указано')


def send_notification(message):
    try:
        print("=" * 50)
        print("УВЕДОМЛЕНИЕ ДЛЯ АДМИНИСТРАТОРА:")
        print(message)
        print("=" * 50)

        with open('notifications.log', 'a', encoding='utf-8') as f:
            f.write(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(message)
            f.write("\n" + "=" * 50 + "\n")

    except Exception as e:
        logger.error(f"Ошибка отправки уведомления: {e}")


@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    os.makedirs('static/images', exist_ok=True)

    print("🚀 YG Auto запускается...")
    print("📍 Сайт доступен по адресу: http://localhost:5000")
    print("📞 Телефон для связи: +7 (903) 948-35-80")

    app.run(debug=True, host='0.0.0.0', port=5000)