# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import time
import datetime
import random
from dateutil.relativedelta import relativedelta

# Initialize the app from Flask
app = Flask(__name__)

# Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='ticket',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor,
                       )


# ----------------------------------------------  Aux. Functions for Simplicity ----------------------------------------
# Load all phones
def load_phone():
    cursor = conn.cursor()
    pl = []
    query = 'SELECT phone_number AS num FROM staff_phone'
    cursor.execute(query)
    data = cursor.fetchall()
    for e in data:
        pl.append(e['num'])
    cursor.close()
    return pl


# Load all existing airports
def load_airport():
    cursor = conn.cursor()
    ap = []
    query = 'SELECT name FROM airport'
    cursor.execute(query)
    data = cursor.fetchall()
    for e in data:
        ap.append(e['name'])
    cursor.close()
    return ap


# Load all existing emails
def load_email():
    cursor = conn.cursor()
    query = 'SELECT email FROM customer'
    cursor.execute(query)
    data = cursor.fetchall()
    all_email = [i['email'] for i in data]
    cursor.close()
    return all_email


# Return 'XX-XX-XX' format of time
def currdate():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def currym():
    return time.strftime('%Y-%m', time.localtime(time.time()))


def curry():
    return time.strftime('%Y', time.localtime(time.time())), time.strftime('%m', time.localtime(time.time()))


def currtime():
    return time.strftime('%H:%M:%S', time.localtime(time.time()))


# ---------------------------------------------- Public Use Case -------------------------------------------------------
# Welcome page
@app.route('/')
def hello():
    try:
        u_type = session['type']
        if u_type == 'staff':
            name = session['name']
            airline = session['airline']
            return redirect(url_for('staffHomepage', name=name, airline=airline))
        else:
            name = session['name']
            return redirect(url_for('custHomepage', username=name))
    except:
        pass
    cursor = conn.cursor()

    query = "SELECT city FROM airport"
    cursor.execute(query)
    data = cursor.fetchall()
    city_list = []
    for e in data:
        city_list.append(e['city'])
    cursor.close()
    flight_list = []
    cursor = conn.cursor()
    cursor.execute('SELECT flight_number FROM flight')
    data = cursor.fetchall()
    for f in data:
        flight_list.append(f['flight_number'])
    airport_list = []
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM airline')
    data = cursor.fetchall()
    for g in data:
        airport_list.append(g['name'])
    cursor.close()
    return render_template('index.html', city_airport_list=city_list, flight_list=flight_list,
                           airline_list=airport_list)


# Public search with departure and arrival information
@app.route('/publicsearch', methods=['GET', 'POST'])
def publicsearch():
    dp = request.form['departure_airport']
    ap = request.form['arrival_airport']
    date = request.form['flight_date']
    fn = request.form['flight_number']
    airports = load_airport()
    future = '9999-12-31'
    if_cust = False
    if_staff = False
    try:
        a = session['email']
        if_cust = True
    except:
        pass
    try:
        a = session['airline']
        if_staff = True
    except:
        pass

    if dp in airports and ap in airports:
        if not fn:
            query = 'SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight, airport as S, airport as T WHERE departure_airport_name = %s' \
                    ' AND arrival_airport_name = %s AND departure_date BETWEEN %s AND %s'
            cursor = conn.cursor()
            if not date:
                date = currdate()
                cursor.execute(query, (dp, ap, date, future))
            else:
                cursor.execute(query, (dp, ap, date, date))
        else:
            query = 'SELECT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight, airport as S, airport as T WHERE departure_airport_name = S.name AND' \
                    ' arrival_airport_name = T.name AND flight_number = %s AND departure_date BETWEEN %s AND %s'
            cursor = conn.cursor()
            if not date:
                date = currdate()
                cursor.execute(query, (fn, date, future))
            else:
                cursor.execute(query, (fn, date, date))
    elif dp in airports and ap not in airports:
        if not fn:
            query = 'SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight, airport as S, airport as T WHERE departure_airport_name = %s' \
                    ' AND arrival_airport_name in (SELECT name FROM airport WHERE city=%s) AND departure_date BETWEEN %s AND %s'
            cursor = conn.cursor()
            if not date:
                date = currdate()
                cursor.execute(query, (dp, ap, date, future))
            else:
                cursor.execute(query, (dp, ap, date, date))
        else:
            query = 'SELECT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight, airport as S, airport as T WHERE departure_airport_name = S.name AND' \
                    ' arrival_airport_name = T.name AND flight_number = %s AND departure_date BETWEEN %s AND %s'
            cursor = conn.cursor()
            if not date:
                date = currdate()
                cursor.execute(query, (fn, date, future))
            else:
                cursor.execute(query, (fn, date, date))
    elif dp not in airports and ap in airports:
        if not fn:
            query = 'SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight, airport as S, airport as T WHERE arrival_airport_name = %s' \
                    ' AND departure_airport_name in (SELECT name FROM airport WHERE city=%s) AND departure_date BETWEEN %s AND %s'
            cursor = conn.cursor()
            if not date:
                date = currdate()
                cursor.execute(query, (ap, dp, date, future))
            else:
                cursor.execute(query, (ap, dp, date, date))
        else:
            query = 'SELECT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight, airport as S, airport as T WHERE departure_airport_name = S.name AND' \
                    ' arrival_airport_name = T.name AND flight_number = %s AND departure_date BETWEEN %s AND %s'
            cursor = conn.cursor()
            if not date:
                date = currdate()
                cursor.execute(query, (fn, date, future))
            else:
                cursor.execute(query, (fn, date, date))
    else:
        if not fn:
            query = 'SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight, airport as S, airport as T WHERE arrival_airport_name in (SELECT name FROM airport WHERE city=%s)' \
                    ' AND departure_airport_name in (SELECT name FROM airport WHERE city=%s) AND departure_date BETWEEN %s AND %s'
            cursor = conn.cursor()
            if not date:
                date = currdate()
                cursor.execute(query, (ap, dp, date, future))
            else:
                cursor.execute(query, (ap, dp, date, date))
        else:
            query = 'SELECT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight, airport as S, airport as T WHERE departure_airport_name = S.name AND' \
                    ' arrival_airport_name = T.name AND flight_number = %s AND departure_date BETWEEN %s AND %s'
            cursor = conn.cursor()
            if not date:
                date = currdate()
                cursor.execute(query, (fn, date, future))
            else:
                cursor.execute(query, (fn, date, date))
    data = cursor.fetchall()
    cursor.close()
    if data:
        if if_cust:
            return render_template('custPublicSearch.html', flight_data=data)
        elif if_staff:
            return render_template('staffPublicSearch.html', flight_data=data)
        else:
            return render_template('publicsearch.html', flight_data=data)
    else:
        error = 'No flights found for the conditions'
        if if_cust:
            return render_template('custPublicSearch.html', error=error)
        elif if_staff:
            return render_template('staffPublicSearch.html', error=error)
        else:
            return render_template('publicsearch.html', error=error)


# Public Search based on airlines and departure dates
@app.route('/publicSearchV2', methods=['GET', 'POST'])
def publicSearchV2():
    airline = request.form['airline_name']
    date = request.form['flight_date']
    num = request.form['flight_number']
    cursor = conn.cursor()
    if num:
        query = 'SELECT airline_name, flight_number, departure_airport_name, ' \
                'departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight WHERE' \
                ' airline_name=%s AND flight_number = %s AND departure_date = %s'
        cursor.execute(query, (airline, num, date))
    else:
        query = 'SELECT airline_name, flight_number, departure_airport_name, ' \
                'departure_time, arrival_airport_name, arrival_time, base_price, status FROM flight WHERE' \
                ' airline_name=%s AND departure_date = %s'
        cursor.execute(query, (airline, date))
    data = cursor.fetchall()
    cursor.close()
    if data:
        return render_template('publicsearch.html', flight_data=data)
    else:
        error = 'No flights found for the conditions'
        return render_template('publicsearch.html', error=error)


# ---------------------------------------------- Customer Use Case -----------------------------------------------------
# Customer Register Pages
@app.route('/customersignup')
def customer_su():
    return render_template('customersignup.html')


# Customer Sign-up Verification
@app.route('/customerregister', methods=['GET', 'POST'])
def customerregister():
    psw = request.form['password']
    cfpsw = request.form['confirm_pwd']
    email = request.form["email"]
    username = request.form["username"]
    building_number = request.form["building_number"]
    street = request.form["street"]
    city = request.form["city"]
    state = request.form["state"]
    phone_number = int(request.form["phone_number"])
    passport_number = request.form["passport_number"]
    passport_expiration = request.form["passport_expiration"]
    passport_country = request.form["passport_country"]
    date_of_birth = request.form["date_of_birth"]
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    for e in data:
        if email == e["email"]:
            error = "Email Duplicate. Please use another email for signing up!"
            return render_template("customersignup.html", error=error)
    if psw != cfpsw:
        error = "Two entries of password do not conform."
        return render_template('customersignup.html', error=error)
    elif date_of_birth > passport_expiration or currdate() < date_of_birth:
        error = "Time is not valid. Please double check the time you are entering"
        return render_template('customersignup.html', error=error)
    elif passport_expiration < currdate():
        error = 'Your passport is expiring. Please update!'
        return render_template('customersignup.html', error=error)
    else:
        query = "INSERT INTO customer VALUES(%s,%s,md5(%s),%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(query, (email, username, psw, building_number, street, city,
                               state, phone_number, passport_number, passport_expiration,
                               passport_country, date_of_birth))
        conn.commit()
        cursor.close()
        return render_template('customersignin.html')


# Customer Sign-in Page
@app.route('/customersignin')
def customersignin():
    return render_template('customersignin.html')


# Customer Sign-in Verification
@app.route('/customerlogin', methods=['GET', 'POST'])
def customerlogin():
    email = request.form['email']
    password = request.form['password']
    query = 'SELECT email FROM customer'
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    exists = False
    for e in data:
        if e['email'] == email:
            exists = True
            break
    if not exists:
        error = "User does not exist. Click the link above to register."
        return render_template('customersignin.html', error=error)
    else:
        query = 'SELECT * FROM customer WHERE email = %s and password = md5(%s)'
        cursor.execute(query, (email, password))
        data = cursor.fetchone()
        if not data:
            cursor.close()
            error = "Email and password do not match. Please try again."
            return render_template('customersignin.html', error=error)
        else:
            query = 'SELECT name FROM customer WHERE email = %s'
            cursor.execute(query, email)
            data = cursor.fetchone()
            name = data['name']
            session['type'] = 'customer'
            session['name'] = name
            session['email'] = email
            return redirect(url_for('custHomepage', name=name))


# Customer's Homepage
@app.route('/custHomepage')
def custHomepage():
    name = session['name']
    return render_template('custHomepage.html', username=name, city_airport_list=load_airport())


# Customer's view flights page
@app.route('/custViewFlight')
def custviewflight():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    ap = load_airport()
    query = "SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, " \
            "arrival_airport_name, arrival_date, sold_price, status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases " \
            "WHERE customer_email = %s AND CONCAT(departure_date, ' ', departure_time) > SYSDATE()"
    email = session['email']
    cursor = conn.cursor()
    cursor.execute(query, email)
    data = cursor.fetchall()
    cursor.close()
    return render_template('custViewFlight.html', airport=ap, booked_flight_data=data)


# Customer's view flights verification page
@app.route('/custViewFlightAuth', methods=['GET', 'POST'])
def customer_view_flight():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    try:
        sa, da = request.form['source_airport'], request.form['dest_airport']
        if not sa:
            sa = 'any'
        if not da:
            da = 'any'
        sd = request.form['sd']
        ed = request.form['ed']
    except:
        sa = da = 'any'
        ed = sd = ''
    if not sd:
        sd = '0000-01-01'
    if not ed:
        ed = '9999-12-31'
    if not sa:
        sa = 'any'
    if not da:
        da = 'any'
    email = session['email']
    cursor = conn.cursor()
    if sa == 'any' and da == 'any':  # The default case, showing future flights
        query = "SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, " \
                "arrival_airport_name, arrival_date, sold_price, status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases " \
                "WHERE customer_email = %s AND departure_date BETWEEN %s AND %s"
        cursor.execute(query, (email, sd, ed))
        data = cursor.fetchall()
    elif sa == 'any' and da != 'any':
        query = "SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, " \
                "arrival_airport_name, arrival_date, sold_price, status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases " \
                "WHERE customer_email = %s AND arrival_airport_name = %s AND departure_date BETWEEN  %s AND %s"
        cursor.execute(query, (email, da, sd, ed))
        data = cursor.fetchall()
    elif sa != 'any' and da == 'any':
        query = "SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, " \
                "arrival_airport_name, arrival_date, sold_price, status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases " \
                "WHERE customer_email = %s AND departure_airport_name = %s AND departure_date BETWEEN  %s AND %s"
        cursor.execute(query, (email, sa, sd, ed))
        data = cursor.fetchall()
    else:
        query = "SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, " \
                "arrival_airport_name, arrival_date, sold_price, status FROM flight NATURAL JOIN ticket NATURAL JOIN purchases " \
                "WHERE customer_email = %s AND departure_airport_name = %s AND" \
                " arrival_airport_name = %s AND departure_date BETWEEN  %s AND %s"
        cursor.execute(query, (email, sa, da, sd, ed))
        data = cursor.fetchall()
    if not data:
        return render_template('custViewFlight.html', airport=load_airport(), error='Information not found!')
    return render_template('custViewFlight.html', booked_flight_data=data, airport=load_airport())


# Customer's purchase page
@app.route('/custPurchasepage', methods=['GET', 'POST'])
def customerPurchasepage():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    cursor = conn.cursor()
    query = "SELECT DISTINCT city FROM airport"
    cursor.execute(query)
    data = cursor.fetchall()
    city_list = []
    for e in data:
        city_list.append(e['city'])
    cursor.close()
    return render_template('custPurchasepage.html', city_airport_list=city_list)


# Customer's purchase confirmation page
@app.route('/custPurchaseMiddle', methods=['GET', 'POST'])
def custPurchaseMiddle():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    dp = request.form['source_airport']
    ar = request.form['destination_airport']
    dt = request.form['date']
    cursor = conn.cursor()
    query = 'SELECT DISTINCT flight.flight_number,flight.airline_name, departure_airport_name, departure_date, arrival_airport_name, arrival_date, base_price, status from flight, airplane, airport as S, airport as T where flight.airplane_id = airplane.ID ' \
            'AND S.name = flight.departure_airport_name' \
            ' AND T.name = flight.arrival_airport_name AND S.city = %s AND T.city = %s AND CONCAT(departure_date, " ", departure_time) > SYSDATE() AND departure_date=%s'
    cursor.execute(query, (dp, ar, dt))
    all_data = cursor.fetchall()
    cursor.close()
    fl = []
    if not all_data:
        return render_template('Purchasenotgood.html', error='No such flights available.')
    for data in all_data:
        fl.append(data['flight_number'])
    session['date'] = dt
    return render_template('custPurchaseMiddle.html', flight_data=all_data, flights=fl)


# Customer's purchase detail page
@app.route('/custPurchaseDetail', methods=['GET', 'POST'])
def custPurchaseDetail():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    try:
        date = session['date']
        flight = request.form['flight']
        session.pop('date')
        query = 'SELECT * FROM flight ,airplane WHERE airplane_id = airplane.ID AND flight_number=%s AND departure_date=%s'
        cursor = conn.cursor()
        cursor.execute(query, (flight, date))
        session.pop('date', None)
        data = cursor.fetchone()
        price, seat, fl = data['base_price'], data['seat_amount'], data['flight_number']
        threshold = seat * 0.3
        query = "SELECT (seat_amount - COUNT(ticket.ticket_id)) AS remain FROM airplane , purchases NATURAL JOIN ticket natural right outer join flight " \
                "WHERE airplane.ID = airplane_id AND flight.flight_number = %s GROUP BY flight.flight_number"
        cursor = conn.cursor()
        cursor.execute(query, fl)
        new_data = cursor.fetchone()
        remain = new_data['remain']
        if remain <= 0:
            return render_template('Purchasenotgood.html', error='The flight you searched for has no more seats.')
        if remain < threshold:
            price = 1.2 * float(price)
        data['base_price'] = price
        query = 'SELECT ticket_id FROM ticket NATURAL JOIN flight ' \
                'WHERE departure_date = %s AND flight_number=%s AND avail = "1"'
        cursor.execute(query, (date, flight))
        temp_data = cursor.fetchall()
        if not temp_data:
            return render_template('custnotbuy.html', info='The flight is in a wrong status: invalidly added.')
        tl = []
        for e in temp_data:
            tl.append(int(e['ticket_id']))
        final_choice = random.choice(tl)
        session['choice'] = int(final_choice)
        session['price'] = float(price)
        cursor.close()
        return render_template('custPurchaseDetail.html', flight_info=data, available_ticket_num=remain,
                               card=['Credit Card', 'Debt Card'])
    except:
        return render_template('custnotbuy.html')


# Customer's purchase with fillings of payment information
@app.route('/custPurchaseProcessCont', methods=['GET', 'POST'])
def purchase_process():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        session.pop('price', None)
        session.pop('choice', None)
        session.pop('card', None)
        return render_template('loginError.html')
    card_number = request.form['card_num']
    card_name = request.form['card_name']
    card_type = request.form['card_type']
    exp = request.form['exp']
    if exp < currdate():
        return render_template('custnotbuy.html', info='The card has already expired.')
    session['card'] = card_name + " " + card_number + " " + card_type + " " + exp
    return redirect(url_for('custPurchaseSuccessPage'))


# Customer's successful payment after submissions of the required information; generating a purchase record.
@app.route('/custPurchaseSuccessPage')
def custPurchaseSuccessPage():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    price = session['price']
    email = session['email']
    choice = session['choice']
    card = session['card'].split()
    name = card[0]
    number = card[1]
    c_type = card[2]
    exp = card[-1]
    query = 'INSERT INTO purchases VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    cursor = conn.cursor()
    cursor.execute(query, (email, choice, c_type, number, exp, name, currdate(), currtime()))
    conn.commit()
    query = 'SELECT base_price FROM ticket NATURAL JOIN flight WHERE ticket.ticket_id = %s'
    cursor.execute(query, choice)
    bp = cursor.fetchone()['base_price']
    change = False
    if price != bp:
        change = True
    query = "UPDATE ticket SET avail = '0' WHERE ticket_id = %s"
    cursor.execute(query, choice)
    conn.commit()
    if change:
        query = "UPDATE ticket SET sold_price = %s WHERE ticket_id = %s"
        cursor.execute(query, (price, choice))
        conn.commit()

    cursor.close()
    session.pop('price', None)
    session.pop('choice', None)
    session.pop('card', None)
    return render_template('custFinalPurchaseSuccessPage.html')


# Message After Customer's Successful Payment
@app.route('/custFinalPurchaseSuccessPage')
def byebyebye():
    return render_template('custFinalPurchaseSuccessPage.html')


# Customer's Rate & Comment Page
@app.route('/custRateComment')
def custRateComment():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    email = session['email']
    cursor = conn.cursor()
    query = 'SELECT DISTINCT name FROM airline'
    airline_list = []
    cursor.execute(query)
    data = cursor.fetchall()
    for e in data:
        airline_list.append(e['name'])
    query = 'SELECT DISTINCT flight_number FROM ticket NATURAL JOIN purchases WHERE customer_email = %s'
    cursor.execute(query, email)
    data = cursor.fetchall()
    if not data:
        return render_template('customererror.html', name=session['name'], error='You have not taken any flights yet!')
    fl = []
    for f in data:
        fl.append(f['flight_number'])
    cursor.close()
    return render_template('custRateComment.html', airline=airline_list, nums=[1, 2, 3, 4, 5], flights=fl)


# Customer's posting rate and view form
@app.route('/custRateandReview', methods=['GET', 'POST'])
def custRateandReview():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    comment = request.form['comment']
    name = request.form['name']
    email = session['email']
    rating = request.form['rating']
    cursor = conn.cursor()
    flight = request.form['flight']
    query = 'SELECT DISTINCT flight_number FROM ticket NATURAL JOIN purchases WHERE customer_email = %s'
    cursor.execute(query, email)
    data = cursor.fetchall()
    fl = []
    for f in data:
        fl.append(f['flight_number'])
    query = 'SELECT flight_number FROM flight WHERE airline_name = %s'
    cursor.execute(query, name)
    flight_list = []
    for e in cursor.fetchall():
        flight_list.append(e['flight_number'])
    cursor.close()
    if not flight_list or flight not in flight_list:
        return render_template('customererror.html', name=session['name'], error='Flights and airline do not match.')
    query = 'INSERT INTO comments(blog_post, airline_name,flight_num, email, rating) VALUES (%s,%s,%s,%s,%s)'
    try:
        cursor = conn.cursor()
        cursor.execute(query, (comment, name, flight, email, rating))
        conn.commit()
        cursor.close()
        return render_template('thanksforfeedback.html', name=session['name'], flights=fl)
    except:
        return render_template('customererror.html', name=session['name'], error='Wrong information for flights')


# Customer's page showing default spending trackings
@app.route('/custTrackSpending')
def custTrackspending():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    # Show the default components:

    year = datetime.datetime.now().year
    name = session['name']
    email = session['email']
    query = '''SELECT SUM(sold_price) AS yeartot
                         FROM ticket NATURAL JOIN purchases WHERE customer_email = %s AND YEAR(purchased_date) = %s'''
    cursor = conn.cursor()
    cursor.execute(query, (email, year))
    yearly = cursor.fetchone()["yeartot"]
    query = '''SELECT SUM(sold_price) AS tot_price FROM ticket NATURAL JOIN purchases
                    WHERE customer_email = %s AND YEAR(purchased_date) = %s AND MONTH(purchased_date) = %s'''
    xAxis_categories = []
    six_month = []
    current_month = datetime.datetime.now().month
    cursor = conn.cursor()

    for i in range(1, 7):
        if current_month - 6 + i <= 0:
            cursor.execute(query, (email, year - 1, 6 + i + current_month))
            xAxis_categories.append("%s.%s" % (year - 1, 6 + i + current_month))
        else:
            cursor.execute(query, (email, year, i + current_month - 6))
            xAxis_categories.append("%s.%s" % (year, i + current_month - 6))
        price = cursor.fetchone()["tot_price"]
        if not price:
            price = 0
        six_month.append(float(price))
    return render_template('custTrackSpending.html', user=name, xAxis_categories=xAxis_categories,
                           annual_spending=yearly,
                           total_spending_in_month=sum(six_month), monthly=six_month,
                           interval='last 6 months')


# Customer's posting form to show specific flight records within time range
@app.route('/custTrackerAuth', methods=['GET', 'POST'])
def custTracker():
    try:
        a = session['type']
        if a == 'staff':
            return render_template('staffNotAuthorized.html')
    except:
        return render_template('loginError.html')
    name = session['name']
    email = session['email']
    try:
        start = request.form['start_date']
        end = request.form['end_date']
    except:
        start = end = ""
    query = '''SELECT SUM(sold_price) AS yeartot
               FROM ticket NATURAL JOIN purchases WHERE customer_email = %s AND YEAR(purchased_date) = %s'''
    cursor = conn.cursor()
    year = datetime.datetime.now().year
    cursor.execute(query, (email, year))
    yearly = cursor.fetchone()["yeartot"]
    if not yearly:
        yearly = 0
    query = '''SELECT SUM(sold_price) AS tot_price FROM ticket NATURAL JOIN purchases
                WHERE customer_email = %s AND YEAR(purchased_date) = %s AND MONTH(purchased_date) = %s'''
    xAxis_categories = []
    six_month = []
    current_month = datetime.datetime.now().month
    cursor = conn.cursor()
    for i in range(1, 7):
        if current_month - 6 + i <= 0:
            cursor.execute(query, (email, year - 1, 6 + i + current_month))
            xAxis_categories.append("%s.%s" % (year - 1, 6 + i + current_month))
        else:
            cursor.execute(query, (email, year, i + current_month - 6))
            xAxis_categories.append("%s.%s" % (year, i + current_month - 6))
        price = cursor.fetchone()["tot_price"]
        if not price:
            price = 0
        six_month.append(float(price))
    if (not start) or (not end) or (
            end < start):  # Invalid input; Only when they're all not None, it will not be set to default.
        interval = 'six months (default)'
        range_spending = six_month
        range_specific = sum(six_month)
    else:
        xAxis_categories = []
        range_spending = []
        ey, em = int(end[:4]), int(end[5:7])
        sy, sm = int(start[:4]), int(start[5:7])
        span = 12 * (ey - sy) + (em - sm)
        for i in range(span + 1):
            month = (sm + i) % 12
            yp = (sm + i) // 12 + sy
            cursor.execute(query, (email, yp, month))
            xAxis_categories.append("%s.%s" % (yp, month))
            price = cursor.fetchone()["tot_price"]
            if not price:
                price = 0
            range_spending.append(float(price))
        interval = start + ' to ' + end
        # Now asking for the specific one:
        query = '''SELECT SUM(sold_price) AS tot_price FROM ticket NATURAL JOIN purchases
                WHERE customer_email = %s AND purchased_date BETWEEN %s AND %s'''
        cursor.execute(query, (email, start, end))
        data = cursor.fetchall()
        range_specific = 0
        for e in data:
            temp = e['tot_price']
            if not temp:
                temp = 0
            range_specific += temp

    return render_template('custTrackSpending.html', user=name, xAxis_categories=xAxis_categories,
                           annual_spending=yearly,
                           total_spending_in_month=range_specific, monthly=range_spending,
                           interval=interval)


# ---------------------------------------------- Staff Use Case --------------------------------------------------------
# Staff's sign-up page
@app.route('/staffsignup')
def staffsignup():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airline")
    data = cursor.fetchall()
    airline_list = []
    for e in data:
        airline_list.append(e["name"])
    cursor.close()
    return render_template("staffsignup.html", airlines=airline_list)


# Staff's sign-up verification
@app.route('/staffregister', methods=['GET', 'POST'])
def staffregister():
    cursor = conn.cursor()
    username = request.form['username']
    psw = request.form['password']
    cfpsw = request.form['confirm_pwd']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    airline_name = request.form['airline_name']
    phone_list = load_phone()
    phone0 = request.form['phone']
    phone1 = request.form['phone1']
    phone2 = request.form['phone2']
    cursor.execute("SELECT * FROM airline")
    data = cursor.fetchall()
    airline_list = []
    for e in data:
        airline_list.append(e["name"])
    if not phone1:
        phone1 = '000'
    if not phone2:
        phone2 = '000'
    phone = [phone0, phone1, phone2]
    while '000' in phone:
        del phone[-1]
    for f in phone:
        if f in phone_list:
            return render_template('staffsignup.html', error='Duplicate phone number, already registered.',
                                   airlines=airline_list)
    cursor.execute("SELECT username FROM airline_staff")
    data = cursor.fetchall()
    cursor.close()
    for e in data:
        if e['username'] == username:
            error = 'Username exists. Please log in or select another name.'
            return render_template('staffsignup.html', error=error, airlines=airline_list)
    if psw != cfpsw:
        error = "Two entries of password do not conform."
        return render_template('staffsignup.html', error=error, airlines=airline_list)
    elif currdate() < date_of_birth:
        error = "Time is not valid. Please double check the time you are entering"
        return render_template('staffsignup.html', error=error, airlines=airline_list)
    else:
        cursor = conn.cursor()
        query = "INSERT INTO airline_staff VALUES(%s,%s, md5(%s),%s,%s,%s)"
        cursor.execute(query, (username, airline_name, psw, first_name, last_name, date_of_birth))
        conn.commit()
        query = 'INSERT INTO staff_phone VALUES(%s, %s)'
        for item in phone:
            cursor.execute(query, (username, item))
            conn.commit()
        conn.commit()
        cursor.close()
        return render_template('staffsignin.html')


# Staff sign-in page
@app.route('/staffsignin')
def staffsignin():
    return render_template('staffsignin.html')


# Staff sign-in verification
@app.route('/stafflogin', methods=['GET', 'POST'])
def stafflogin():
    username = request.form['username']
    psw = request.form['password']
    query = 'SELECT username FROM airline_staff'
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    exists = False
    for e in data:
        if e['username'] == username:
            exists = True
            break
    if not exists:
        error = "User does not exist. Click the link above to register."
        return render_template('staffsignin.html', error=error)
    else:
        query = 'SELECT * FROM airline_staff WHERE username = %s and password = md5(%s)'
        cursor = conn.cursor()
        cursor.execute(query, (username, psw))
        data = cursor.fetchone()
        cursor.close()
        if not data:
            error = "Username and password do not match. Please try again."
            return render_template('staffsignin.html', error=error)
        else:
            cursor = conn.cursor()
            query = 'SELECT first_name, last_name, airline_name FROM airline_staff WHERE username = %s'
            cursor.execute(query, username)
            data = cursor.fetchone()
            airline = data['airline_name']
            session['type'] = 'staff'
            session['name'] = username
            session['airline'] = airline
            return redirect(
                url_for('staffHomepage', username=username, airline=airline, city_airport_list=load_airport()))


# Staff's homepage
@app.route('/staffHomepage')
def staffHomepage():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline = session['airline']
    name = session['name']
    return render_template('staffHomepage.html', username=name, airline=airline, city_airport_list=load_airport())


# Staff's creating flight page
@app.route('/staffCreateFlight')
def staffCreateFlight():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline_name = session['airline']
    cursor = conn.cursor()
    ap = []
    fp = []
    query = 'SELECT name FROM airport'
    cursor.execute(query)
    data = cursor.fetchall()
    for e in data:
        ap.append(e['name'])
    cursor.execute('SELECT ID FROM airplane WHERE airline_name = %s', airline_name)
    data = cursor.fetchall()
    if not data:
        return render_template('staffnotfound.html', error="No planes available")
    for e in data:
        fp.append(e['ID'])
    return render_template('staffCreateFlight.html', airline_name=airline_name, airports=ap, airplanes=fp)


# Staff's creating flight verification page
@app.route('/flightCreation', methods=['GET', 'POST'])
def flightCreation():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    name = session['name']
    airline = session['airline']
    num = request.form['flight_num']
    da = request.form['departure_airport']
    dd = request.form['departure_date']
    dt = request.form['departure_time']
    aa = request.form['arrival_airport']
    ad = request.form['arrival_date']
    at = request.form['arrival_time']
    price = request.form['price']
    status = request.form['status']
    plane_id = request.form['airplane_id']
    checker = 'SELECT * FROM flight WHERE flight_number = %s AND airline_name = %s AND departure_date = %s'
    cursor = conn.cursor()
    cursor.execute(checker, (num, airline, dd))
    data = cursor.fetchall()
    if data:
        return render_template('staffnotadd.html', name=name, error='Duplicated flight in a same day!')

    if da == aa:
        return render_template('staffnotadd.html', name=name, error='Same destination and arrival')
    if dd + ' ' + dt >= ad + ' ' + at or dd <= currdate():
        return render_template('staffnotadd.html', name=name,
                               error='Time is Wrong (Either having a later departure date or a previous date)')
    query = 'SELECT * FROM flight WHERE airplane_id=%s AND airline_name = %s ' \
            'AND departure_date BETWEEN %s AND %s '
    cursor.execute(query, (plane_id, airline, dd, ad))
    data = cursor.fetchall()
    if data:
        return render_template('staffnotadd.html', name=name,
                               error='The airplane needs some rest, or it can not take two flights concurrently!')
    cursor = conn.cursor()
    query = 'INSERT INTO flight VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    try:
        cursor.execute(query, (num, dd, dt, airline, plane_id, da, ad, at, price, aa, status))
        conn.commit()
    except:
        return render_template('staffnotadd.html', name=name, error='Error in adding')
    # Generating the tickets
    cursor.execute('SELECT seat_amount FROM airplane WHERE ID = %s AND airline_name = %s', (plane_id, airline))
    amount = cursor.fetchone()['seat_amount']
    cursor.execute('SELECT ticket_id FROM ticket')
    data = cursor.fetchall()
    avoid = []
    for f in data:
        avoid.append(f['ticket_id'])
    for k in range(amount):
        ci = random.randint(1000000, 1000000000)
        while ci in avoid:
            ci = random.randint(1000000, 1000000000)
        query = 'INSERT INTO ticket VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(query,
                       (ci, num, dd, dt, airline, price, 1))
        conn.commit()
    return render_template('staffsuccess.html')


# Staff's airplane creation page
@app.route('/staffCreateAirplane')
def staffCreateAirplane():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline_name = session['airline']
    return render_template('staffCreateAirplane.html', airline_name=airline_name)


# Staff's airplane creation verification page
@app.route('/staffCreateAirplaneAuth', methods=['GET', 'POST'])
def create_plane():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    name = session['name']
    airline_name = session['airline']
    seat_amount = request.form['seat_amount']
    plane_id = request.form['airplane_id']
    query = 'INSERT INTO airplane VALUES (%s, %s, %s)'
    try:
        cursor = conn.cursor()
        cursor.execute(query, (plane_id, airline_name, seat_amount))
        conn.commit()
        cursor.close()
        return render_template('staffsuccess.html')
    except:
        return render_template('staffnotaddplane.html', name=name, error='Something wrong detected')


# Staff's airport creation page
@app.route('/staffCreateAirport')
def staffCreateAirport():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline_name = session['airline']
    return render_template('staffCreateAirport.html', airline_name=airline_name)


# Staff's airport creation verification page
@app.route('/staffCreateAirportAuth', methods=['GET', 'POST'])
def create_airport():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    name = session['name']
    an = request.form['airport_name']
    city = request.form['city']
    query = 'INSERT INTO airport VALUES (%s, %s)'
    cursor = conn.cursor()
    try:
        cursor.execute(query, (an, city))
        conn.commit()
        cursor.close()
        return render_template('staffsuccess.html')
    except:
        return render_template('staffnotaddairport.html', name=name, error='Airport already exists.')


# Staff's view rating page
@app.route('/staffViewRating')
def staffview():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    an = session['airline']
    query = 'SELECT flight_num, AVG(rating) as avr FROM comments WHERE airline_name = %s GROUP BY flight_num'
    cursor = conn.cursor()
    cursor.execute(query, an)
    data = cursor.fetchall()
    fl = []
    for e in data:
        fl.append(e['flight_num'])
    return render_template('staffViewRating.html', airline_name=an, data=data, flight_list=fl)


# Staff's view rating verification page
@app.route('/staffViewComments', methods=['GET', 'POST'])
def staffViewComments():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    flight = request.form['flight']
    query = 'SELECT * FROM comments WHERE flight_num = %s'
    cursor = conn.cursor()
    cursor.execute(query, flight)
    data = cursor.fetchall()
    cursor.close()
    return render_template('staffViewComments.html', name=flight, data=data)


# Staff's status changing page
@app.route('/staffChangeStatus')
def changestatus():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline = session['airline']
    query = 'SELECT flight_number FROM flight WHERE airline_name=%s'
    cursor = conn.cursor()
    cursor.execute(query, airline)
    data = cursor.fetchall()
    flights = [e['flight_number'] for e in data]
    cursor.close()
    return render_template('staffChangeStatus.html', airline_name=airline, flights=flights)


# Staff's status changing verification page
@app.route('/staffStatusChange', methods=['GET', 'POST'])
def status_change():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    name = session['name']
    airline = session['airline']
    flight = request.form['flight_num']
    date = request.form['departure_date']
    new_status = request.form['status']
    query = 'SELECT * FROM flight WHERE airline_name = %s AND flight_number = %s AND departure_date = %s'
    cursor = conn.cursor()
    cursor.execute(query, (airline, flight, date))
    data = cursor.fetchall()
    if not data:
        return render_template('staffnotchange.html', name=name, error='No such flights available.')
    query = 'UPDATE Flight SET status = %s WHERE airline_name = %s' \
            ' AND flight_number = %s AND departure_date = %s'
    cursor.execute(query, (new_status, airline, flight, date))
    conn.commit()
    cursor.close()
    return render_template('staffsuccess.html')


# Staff's flight viewing page
@app.route('/staffViewFlight')
def viewflight():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline = session['airline']
    current = datetime.date.today()
    default_future = datetime.date.today() + relativedelta(days=+30)
    query = 'SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name,' \
            'departure_date, departure_time, arrival_date, arrival_time, status FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s'
    cursor = conn.cursor()
    cursor.execute(query, (airline, current, default_future))
    data = cursor.fetchall()
    return render_template('staffViewFlight.html', booked_flight_data=data, airline_name=airline, start=current,
                           end=default_future, airport=load_airport())


# Staff's flight viewing verification page
@app.route('/staffViewFlightAuth', methods=['GET', 'POST'])
def staffViewFlightsAuth():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline = session['airline']

    query = 'SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name,' \
            'departure_date, departure_time, arrival_date, arrival_time, ' \
            'status FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s'
    try:
        sd, ed = request.form['sd'], request.form['ed']
        sp, dp = request.form['source_airport'], request.form['dest_airport']
    except:
        sd = datetime.date.today()
        ed = sd + relativedelta(days=+30)
        cursor = conn.cursor()
        cursor.execute(query, (airline, sd, ed))
        data = cursor.fetchall()
        return render_template('staffViewFlight.html', booked_flight_data=data, airline_name=airline, start=sd,
                               end=ed, airport=load_airport())
    if sp == 'any':
        sp = ''
    if dp == 'any':
        dp = ''
    if not sp and not dp:
        query = 'SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name,' \
                'departure_date, departure_time, arrival_date, arrival_time, ' \
                'status FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s'
        if not sd and not ed:
            sd = datetime.date.today()
            ed = sd + relativedelta(days=+30)
        if not sd:
            sd = '0000-01-01'
        if not ed:
            ed = '9999-12-31'
        if ed < sd:
            return render_template('staffViewFlight.html', error='A later starting date', airline_name=airline,
                                   start=sd,
                                   end=ed, airport=load_airport())
        cursor = conn.cursor()
        cursor.execute(query, (airline, sd, ed))
        data = cursor.fetchall()
        if ed == '9999-12-31':
            ed = 'future'
        if sd == '0000-01-01':
            sd = 'past'
        if not data:
            return render_template('staffViewFlight.html', error='No satisfying information.', airline_name=airline,
                                   start=sd,
                                   end=ed, airport=load_airport())
        else:
            return render_template('staffViewFlight.html', booked_flight_data=data, airline_name=airline, start=sd,
                                   end=ed, airport=load_airport())
    if not sp and dp:
        query = 'SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name,' \
                'departure_date, departure_time, arrival_date, arrival_time, ' \
                'status FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND arrival_airport_name=%s'
        if not sd and not ed:
            sd = datetime.date.today()
            ed = sd + relativedelta(days=+30)
        if not sd:
            sd = '0000-01-01'
        if not ed:
            ed = '9999-12-31'
        if ed < sd:
            return render_template('staffViewFlight.html', error='A later starting date', airline_name=airline,
                                   start=sd,
                                   end=ed, airport=load_airport())
        cursor = conn.cursor()
        cursor.execute(query, (airline, sd, ed, dp))
        data = cursor.fetchall()
        if ed == '9999-12-31':
            ed = 'future'
        if sd == '0000-01-01':
            sd = 'past'
        if not data:
            return render_template('staffViewFlight.html', error='No satisfying information.', airline_name=airline,
                                   start=sd,
                                   end=ed, airport=load_airport())
        else:
            return render_template('staffViewFlight.html', booked_flight_data=data, airline_name=airline, start=sd,
                                   end=ed, airport=load_airport())
    if not dp and sp:
        query = 'SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name,' \
                'departure_date, departure_time, arrival_date, arrival_time, ' \
                'status FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND departure_airport_name=%s'
        if not sd and not ed:
            sd = datetime.date.today()
            ed = sd + relativedelta(days=+30)
        if not sd:
            sd = '0000-01-01'
        if not ed:
            ed = '9999-12-31'
        if ed < sd:
            return render_template('staffViewFlight.html', error='A later starting date', airline_name=airline,
                                   start=sd,
                                   end=ed, airport=load_airport())
        cursor = conn.cursor()
        cursor.execute(query, (airline, sd, ed, sp))
        data = cursor.fetchall()
        if ed == '9999-12-31':
            ed = 'future'
        if sd == '0000-01-01':
            sd = 'past'
        if not data:
            return render_template('staffViewFlight.html', error='No satisfying information.', airline_name=airline,
                                   start=sd,
                                   end=ed, airport=load_airport())
        else:
            return render_template('staffViewFlight.html', booked_flight_data=data, airline_name=airline, start=sd,
                                   end=ed, airport=load_airport())
    if sp and dp:
        query = 'SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name,' \
                'departure_date, departure_time, arrival_date, arrival_time, ' \
                'status FROM flight WHERE airline_name = %s AND departure_date BETWEEN %s AND %s AND arrival_airport_name=%s AND departure_airport_name=%s'
        if not sd and not ed:
            sd = datetime.date.today()
            ed = sd + relativedelta(days=+30)
        if not sd:
            sd = '0000-01-01'
        if not ed:
            ed = '9999-12-31'
        if ed < sd:
            return render_template('staffViewFlight.html', error='A later starting date', airline_name=airline,
                                   start=sd,
                                   end=ed, airport=load_airport())
        cursor = conn.cursor()
        cursor.execute(query, (airline, sd, ed, dp, sp))
        data = cursor.fetchall()
        if ed == '9999-12-31':
            ed = 'future'
        if sd == '0000-01-01':
            sd = 'past'
        if not data:
            return render_template('staffViewFlight.html', error='No satisfying information.', airline_name=airline,
                                   start=sd,
                                   end=ed, airport=load_airport())
        else:
            return render_template('staffViewFlight.html', booked_flight_data=data, airline_name=airline, start=sd,
                                   end=ed, airport=load_airport())


# Staff's page for viewing specific customer
@app.route('/staffViewSpecific', methods=['GET', 'POST'])
def staffViewSpecific():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    cursor = conn.cursor()
    airline = session['airline']
    try:
        target = request.form['email']
    except:
        target = ' '
    query = 'SELECT DISTINCT flight.flight_number, departure_airport_name, arrival_airport_name, departure_date, ' \
            'arrival_date FROM purchases NATURAL JOIN ' \
            'ticket NATURAL JOIN flight WHERE customer_email = %s AND flight.airline_name = %s'
    cursor.execute(query, (target, airline))
    data = cursor.fetchall()
    return render_template('staffViewSpecific.html', customer_data=data, emails=load_email())


# Staff view report page with default information
@app.route('/staffViewReport')
def viewreport():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline_name = session['airline']
    cursor = conn.cursor()
    last_year = datetime.datetime.now().year - 1
    query = '''SELECT a.city airport_city, COUNT(*) traffic_num FROM airport a, flight f,ticket t
                            WHERE a.name = f.arrival_airport_name
                            AND (f.airline_name, f.flight_number) = (t.airline_name,t.flight_number)
                            AND f.status != "Cancelled"
                            AND f.airline_name = %s
                            AND year(f.arrival_time) = %s
                            AND t.ticket_id in (SELECT ticket_id FROM purchases)
                            GROUP BY airport_city
                            ORDER BY traffic_num DESC
                            LIMIT 3;'''
    cursor.execute(query, (airline_name, last_year))
    top3_destinations_y = cursor.fetchall()

    # get top3 destination during last three months
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    endmark = datetime.date(year, month, day)
    month -= 3
    if month <= 0:
        month += 12
        year -= 1
    startmark = datetime.date(year, month, day)
    query = '''SELECT a.city airport_city, COUNT(*) traffic_num FROM airport a, flight f, ticket t
                WHERE a.name = f.arrival_airport_name
                                    AND (f.airline_name, f.flight_number) = (t.airline_name, t.flight_number)
                                    AND f.status != "Cancelled"
                                    AND f.airline_name = %s
                                    AND f.arrival_date <= %s
                                    AND f.arrival_date >= %s
                                    AND t.ticket_id in (SELECT ticket_id FROM purchases)
                                    GROUP BY airport_city
                                    ORDER BY traffic_num DESC
                                    LIMIT 3;'''
    cursor.execute(query, (airline_name, endmark, startmark))
    top3_destinations_m = cursor.fetchall()
    year = datetime.datetime.now().year - 1
    ly = year

    # get annually_direct
    query = '''SELECT SUM(t.sold_price) annual
                        FROM purchases p , ticket t, flight f
                        WHERE p.ticket_id = t.ticket_id
                        AND (t.airline_name,t.flight_number) = (f.airline_name,f.flight_number)
                        AND f.airline_name = %s
                        AND YEAR(p.purchased_date) = %s'''
    cursor.execute(query, (airline_name, year))
    yearly = cursor.fetchone()["annual"]
    if not yearly:
        yearly = 0

    # get month-wise tickets sold num
    query = '''SELECT COUNT(t.ticket_id) total_ticket_num
            FROM ticket t, purchases p
            WHERE airline_name = %s
            AND t.ticket_id = p.ticket_id
            AND YEAR(p.purchased_date) = %s
            AND MONTH(p.purchased_date) = %s;'''
    xAxis_categories = []
    monthly_ticket_breakdown = []
    current_month = datetime.datetime.now().month
    for i in range(1, 13):
        if current_month + i > 12:
            cursor.execute(query, (airline_name, year + 1, i - current_month))
            xAxis_categories.append("%s.%s" % (year + 1, i - current_month))
        else:
            cursor.execute(query, (airline_name, year, i + current_month))
            xAxis_categories.append("%s.%s" % (year, i + current_month))
        ticket_num = cursor.fetchone()["total_ticket_num"]
        if not ticket_num:
            ticket_num = 0
        monthly_ticket_breakdown.append(ticket_num)
    total_ticket_num = sum(monthly_ticket_breakdown)

    query = '''SELECT SUM(sold_price) revenue
            FROM ticket t, purchases p
            WHERE airline_name = %s
            AND t.ticket_id = p.ticket_id
            AND YEAR(p.purchased_date) = %s
            AND MONTH(p.purchased_date) = %s;'''
    monthly = []
    for i in range(1, 13):
        cursor.execute(query, (airline_name, year, i))
        rv = cursor.fetchone()["revenue"]
        if not rv:
            rv = 0
        rv = float(rv)
        monthly.append(rv)
    q1 = sum(monthly[0:3])
    q2 = sum(monthly[3:6])
    q3 = sum(monthly[6:9])
    q4 = sum(monthly[9:12])

    cursor.close()
    return render_template("staffViewReport.html",
                           total_ticket_num=total_ticket_num,
                           monthly_ticket_breakdown=monthly_ticket_breakdown,
                           xAxis_categories=xAxis_categories,
                           airline_name=airline_name,
                           top3_destinations_y=top3_destinations_y,
                           top3_destinations_m=top3_destinations_m,
                           q1=q1, q2=q2, q3=q3, q4=q4, yearly=yearly, ly=ly
                           )


# Staff view report with specific information (specified time range)
@app.route('/staffViewReportAuth', methods=['GET', 'POST'])
def staffViewReportAuth():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline_name = session['airline']
    cursor = conn.cursor()
    try:
        start = request.form['start_date']
        end = request.form['end_date']
    except:
        start = end = ''
    if not end:
        end = datetime.date.today()
    if not start:
        start = end - relativedelta(years=+1)
    if str(start) > str(end):
        temp = end - relativedelta(years=+1)
        xAxis_categories = []
        ticket_data = []
        ey, em = int(end[:4]), int(end[5:7])
        sy, sm = int(temp[:4]), int(temp[5:7])
        span = 12 * (ey - sy) + (em - sm)
        for i in range(span + 1):
            month = (sm + i) % 12
            yp = (sm + i) // 12 + sy
            query = '''SELECT COUNT(t.ticket_id) total_ticket_num
                               FROM ticket t, purchases p
                               WHERE airline_name = %s
                               AND t.ticket_id = p.ticket_id
                               AND YEAR(p.purchased_date) = %s
                               AND MONTH(p.purchased_date) = %s;'''

            cursor.execute(query, (airline_name, yp, month))
            xAxis_categories.append("%s.%s" % (yp, month))
            ticket_num = cursor.fetchone()["total_ticket_num"]
            if not ticket_num:
                ticket_num = 0
            ticket_data.append(int(ticket_num))
        interval = temp + ' to ' + end
        return render_template('staffViewReportSpecific.html', interval=interval, total_ticket_num=sum(ticket_data),
                               monthly_ticket_breakdown=ticket_data, xAxis_categories=xAxis_categories,
                               airline_name=airline_name,
                               error='Invalid starting and ending date. Showing the default.')
    else:
        start = str(start)
        end = str(end)
        xAxis_categories = []
        ticket_data = []
        ey, em = int(end[:4]), int(end[5:7])
        sy, sm = int(start[:4]), int(start[5:7])
        span = 12 * (ey - sy) + (em - sm)
        for i in range(span + 1):
            month = (sm + i) % 12
            yp = (sm + i) // 12 + sy
            query = '''SELECT COUNT(t.ticket_id) total_ticket_num
                        FROM ticket t, purchases p
                        WHERE airline_name = %s
                        AND t.ticket_id = p.ticket_id
                        AND YEAR(p.purchased_date) = %s
                        AND MONTH(p.purchased_date) = %s;'''
            cursor.execute(query, (airline_name, yp, month))
            xAxis_categories.append("%s.%s" % (yp, month))
            ticket_num = cursor.fetchone()["total_ticket_num"]
            if not ticket_num:
                ticket_num = 0
            ticket_data.append(int(ticket_num))
            query = '''SELECT SUM(t.sold_price) money
                        FROM ticket t, purchases p
                        WHERE airline_name = %s
                        AND t.ticket_id = p.ticket_id
                        AND p.purchased_date BETWEEN %s AND %s'''
            cursor.execute(query, (airline_name, start, end))
            data = cursor.fetchall()
            yearly = 0
            for e in data:
                if not e['money']:
                    yearly += 0
                else:
                    yearly += e['money']
        interval = start + ' to ' + end
        cursor.close()
        return render_template('staffViewReportSpecific.html', interval=interval, total_ticket_num=sum(ticket_data),
                               monthly_ticket_breakdown=ticket_data, xAxis_categories=xAxis_categories,
                               airline_name=airline_name, yearly=yearly)


# Staff viewing customer page
@app.route('/staffViewCustomer')
def staffviewcust():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline = session['airline']
    fl = []
    query = 'SELECT flight_number FROM flight WHERE airline_name = %s'
    cursor = conn.cursor()
    cursor.execute(query, airline)
    data = cursor.fetchall()
    cursor.close()
    for e in data:
        fl.append(e['flight_number'])
    query = "SELECT customer.name, customer.email, %s ,date_of_birth, city, state, passport_country, " \
            "COUNT(DISTINCT purchases.ticket_id) AS counter FROM customer, purchases, ticket " \
            "WHERE customer.email = customer_email AND purchases.ticket_id = ticket.ticket_id AND airline_name = %s " \
            "GROUP BY customer.name, customer.email, date_of_birth, city, state, passport_country, %s " \
            "ORDER BY counter DESC LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(query, ('---', airline, '---'))
    customer_data = cursor.fetchone()
    return render_template('staffViewCustomer.html', airline_name=airline, flight_num_option=fl,
                           most_frequent_cust=customer_data, emails=load_email())


# Staff viewing customer verification page
@app.route('/staffViewCustomerAuth', methods=['GET', 'POST'])
def staffViewCustomer():
    try:
        a = session['type']
        if a == 'customer':
            return render_template('customerNotAuthorized.html')
    except:
        return render_template('loginError.html')
    airline = session['airline']
    fl = []
    query = 'SELECT flight_number FROM flight WHERE airline_name = %s'
    cursor = conn.cursor()
    cursor.execute(query, airline)
    data = cursor.fetchall()
    for e in data:
        fl.append(e['flight_number'])
    #  Search for the info for a flight
    flight = request.form['flight']
    date = request.form['departure_date']
    query = 'SELECT DISTINCT name, email,flight.flight_number, date_of_birth,' \
            ' city, state, passport_country, %s FROM customer, purchases ' \
            'NATURAL JOIN ticket, flight WHERE customer.email = purchases.customer_email AND flight.flight_number = ticket.flight_number AND ' \
            'flight.airline_name = %s AND flight.flight_number = %s AND flight.departure_date = %s'
    cursor.execute(query, ('---', airline, flight, date))
    data = cursor.fetchall()
    cursor.close()
    return render_template('staffViewCustomer.html', booked_flight_data=data, airline_name=airline,
                           flight_num_option=fl, emails=load_email())


# ---------------------------------------------- Public Use Case -------------------------------------------------------
# Public logging out page
@app.route('/logout')
def logout():
    name = session['name']
    if session['type'] == 'customer':
        session.pop('name', None)
        session.pop('email', None)
        try:
            session.pop('card', None)
            session.pop('choice', None)
            session.pop('price', None)
        except:
            pass
    else:
        session.pop('name', None)
        session.pop('airline', None)
    session.pop('type', None)
    return render_template('goodbye.html', name=name)


app.secret_key = 'secret'
if __name__ == "__main__":
    app.run(debug=True)
