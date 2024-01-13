from flask import Flask, redirect, render_template,request, url_for
import sqlite3

app = Flask(__name__,static_url_path='/static')
app.secret_key = 'your_secret_key' 

DATABASE = 'database.db'

def connect_db():
    return sqlite3.connect(DATABASE)


@app.route('/')
def index():
    db = connect_db()
    
    db.execute('''

       CREATE TABLE IF NOT EXISTS hotel (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_name TEXT NOT NULL,
    hotel_price REAL NOT NULL,
    hotel_amenities TEXT NOT NULL,
    hotel_comments REAL,
    hotel_location TEXT NOT NULL,
    hotel_rating REAL NOT NULL,
    hotel_memberPrice REAL,
    hotel_country TEXT NOT NULL,
    hotel_city TEXT NOT NULL,
    hotel_discount REAL,
    ImageURL TEXT
);

    ''')

    db.execute('DELETE FROM hotel')

    db.execute('''

        INSERT INTO hotel (hotel_name, hotel_price, hotel_amenities, hotel_comments,hotel_location,hotel_rating,hotel_memberPrice,hotel_country,hotel_city,hotel_discount,ImageURL) VALUES
            ('Lara Barut Collection - Ultra All Inclusive','7739','restoran,havuz,Wi-Fi,bar,Spa','11','Güzeloba Mah. Yaşar Sobutay Mah. No.: 30, Lara, Antalya, Antalya, 07235','8.2 Çok İyi','7000','Turkey','Antalya','','https://images.trvl-media.com/lodging/2000000/1210000/1207100/1207007/f5aaac97.jpg?impolicy=resizecrop&rw=1200&ra=fit'),
            ('Pearly Hotel','2274','restoran,havuz,Wi-Fi,bar,Spa','9','Akdeniz Bulvarı No.: 104, Konyaaltı, Antalya, 0707','7.9 İyi','2500','Turkey','Antalya','','https://images.trvl-media.com/lodging/77000000/76580000/76577500/76577472/d1b74eb8.jpg?impolicy=resizecrop&rw=1200&ra=fit'),
            ('Conrad Istanbul Bosphorus','11653','restoran,havuz,Wi-Fi,bar,Spa','5','Cihannüma Mah. Saray Cad. No: 5, Beşiktaş, İstanbul, İstanbul, 34353','8.9 Çok İyi','10000','Turkey','Istanbul','','https://images.trvl-media.com/lodging/1000000/20000/15300/15234/f7fddb72.jpg?impolicy=resizecrop&rw=1200&ra=fit')
        ''')

    db.commit()

    cursor = db.execute('SELECT * FROM hotel ORDER BY hotel_price DESC')

    hotels = cursor.fetchall()

    db.close()

    return render_template('index.html', hotels=hotels)

@app.route('/detail/<int:hotel_id>')
def detail(hotel_id):
    db = connect_db()
    cursor = db.execute('SELECT * FROM hotel WHERE id = ?', (hotel_id,))
    hotel = cursor.fetchone()
    db.close()

    return render_template('detail.html', hotel=hotel)

@app.route('/login')
def login():
    return render_template('login.html')



def connect_db():
    connection = sqlite3.connect(DATABASE)
    connection.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            country TEXT NOT NULL,
            city TEXT NOT NULL
        )
    ''')
    return connection


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['inputFirstName']
        surname = request.form['inputLastName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        country = request.form['inputDropdown1']
        city = request.form['inputDropdown2']
        if not name or not surname or not email or not password or not country or not city:
            return render_template('signup.html', error="Please fill in all fields")
        
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO users (name, surname, email, password, country, city)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, surname, email, password, country, city))

        db.commit()
        db.close()

        return redirect(url_for('index'))

    return render_template('signup.html')


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        city_query = request.form.get('city_query')

        if not city_query:
            return render_template('index.html', hotels=[], error="Please enter a city for the search")

        db = connect_db()
        cursor = db.execute('SELECT * FROM hotel WHERE hotel_city LIKE ? ORDER BY hotel_price DESC', ('%' + city_query + '%',))
        search_results = cursor.fetchall()
        db.close()

        return render_template('searchresult.html', search_results=search_results)
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5001)

