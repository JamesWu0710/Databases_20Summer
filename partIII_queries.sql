-- PROJECT PART III
-- cw2961, xg764, yl5662

---------------------------------------------------- Public ----------------------------------------------------

--search for flights based on departure_airport_name/city, arrival_airport_name/city, and departure_date
SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status 
FROM flight, airport as S, airport as T 
WHERE departure_airport_name = %s
	AND arrival_airport_name = %s 
	AND departure_date BETWEEN %s AND %s;

--search for flights based on departure_airport_name, arrival_city, and departure_date
SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status 
FROM flight, airport as S, airport as T 
WHERE departure_airport_name = %s
	AND arrival_airport_name in (SELECT name FROM airport WHERE city=%s) 
	AND departure_date BETWEEN %s AND %s;

--search for flights based on departure_city, arrival_airport_name, and departure_date
SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status 
FROM flight, airport as S, airport as T 
WHERE arrival_airport_name = %s
	AND departure_airport_name in (SELECT name FROM airport WHERE city=%s) 
	AND departure_date BETWEEN %s AND %s;

--search for flights based on departure_city, arrival_city, and departure_date	
SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status 
FROM flight, airport as S, airport as T 
WHERE arrival_airport_name in (SELECT name FROM airport WHERE city=%s)
	AND departure_airport_name in (SELECT name FROM airport WHERE city=%s) 
	AND departure_date BETWEEN %s AND %s;
	
--search for flights based on departure_airport_name, arrival_airport_name, flight_number and departure_date	
SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status 
FROM flight, airport as S, airport as T 
WHERE departure_airport_name = S.name 
	AND arrival_airport_name = T.name 
	AND flight_number = %s 
	AND departure_date BETWEEN %s AND %s;

--search for flights based on airline_name, flight_number and departure_date					
SELECT DISTINCT airline_name, flight_number, departure_airport_name, departure_time, arrival_airport_name, arrival_time, base_price, status 
FROM flight 
WHERE airline_name=%s 
	AND flight_number = %s 
	AND departure_date = %s;

----------------------------------------------------Customer----------------------------------------------------
--view purchased future flights
SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, arrival_airport_name, arrival_date, sold_price, status 
FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
WHERE customer_email = %s 
	AND CONCAT(departure_date, ' ', departure_time) > SYSDATE();
	
--view purchased flights between a specific range of time, specifying arrival_airport_name
SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, arrival_airport_name, arrival_date, sold_price, status 
FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
WHERE customer_email = %s 
	AND arrival_airport_name = %s 
	AND departure_date BETWEEN  %s AND %s;
	
--view purchased flights between a specific range of time, specifying departure_airport_name
SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, arrival_airport_name, arrival_date, sold_price, status 
FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
WHERE customer_email = %s 
	AND departure_airport_name = %s 
	AND departure_date BETWEEN  %s AND %s;
	
--view purchased flights between a specific range of time, specifying arrival_airport_name and departure_airport_name
SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, arrival_airport_name, arrival_date, sold_price, status 
FROM flight NATURAL JOIN ticket NATURAL JOIN purchases 
WHERE customer_email = %s 
	AND departure_airport_name = %s 
	AND arrival_airport_name = %s 
	AND departure_date BETWEEN  %s AND %s;

--search for future flights on a specific day
SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, arrival_airport_name, arrival_date, sold_price, status 
FROM flight, airport as S, airport as T 
WHERE departure_airport_name = S.name
	AND arrival_airport_name = T.name 
	AND S.city = %s 
	AND T.city = %s 
	AND CONCAT(departure_date, " ", departure_time) > SYSDATE()
	AND departure_date = %s;
	
--search for all future flights
SELECT DISTINCT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, arrival_airport_name, arrival_date, sold_price, status
FROM flight, airport as S, airport as T 
WHERE departure_airport_name = S.name 
	AND arrival_airport_name = T.name 
	AND S.city = %s 
	AND T.city = %s 
	AND flight_number = %s 
	AND CONCAT(departure_date, " ", departure_time) > SYSDATE();
                    
--search for the amount of remaining tickets
SELECT (seat_amount - COUNT(ticket_id)) AS remain 
FROM airplane , ticket natural right outer join flight
WHERE airplane.ID = airplane_id 
	AND flight.flight_number = %s 
GROUP BY flight.flight_number;

--search for remaining tickets
SELECT ticket_id 
FROM ticket NATURAL JOIN flight 
WHERE departure_date = %s 
	AND flight_number=%s 
	AND avail = "1";

--purchase tickets
INSERT INTO Purchases VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
	SELECT ticket_id 
	FROM Ticket 
	WHERE airline_name = '%s'
		AND flight_number = '%s'
		AND departure_date = '%s'
		AND departure_time = '%s'
        AND ticket_id not in (SELECT ticket_id FROM Purchases)
		LIMIT 1;
		
UPDATE ticket
SET avail = "0"
WHERE ticket_id = %s;

--search for flight info about a specific ticket
SELECT airline_name,flight_number,departure_airport_name,departure_time,
       arrival_airport_name,arrival_time,base_price,status
FROM Flight 
WHERE airline_name = '%s' 
	AND flight_number = '%s'
	AND departure_date = '%s'
	AND departure_time = '%s';

--Track spending in the past year
SELECT SUM(sold_price) AS yeartot
FROM ticket NATURAL JOIN purchases 
WHERE customer_email = %s 
	AND YEAR(purchased_date) = %s;                   

--Track spending in the past month
SELECT SUM(sold_price) AS tot_price 
FROM ticket NATURAL JOIN purchases
WHERE customer_email = %s 
	AND YEAR(purchased_date) = %s 
	AND MONTH(purchased_date) = %s;

--Track spending within a specified range
SELECT SUM(sold_price) AS total_spending
FROM ticket NATURAL JOIN purchases
WHERE customer_email = %s 
	AND purchased_date BETWEEN %s AND %s;

--Rate and Comment
INSERT INTO comments VALUES (%s,%s,%s,%s,%s);
                                                         

---------------------------------------------------Airline Staff-----------------------------------------------
--view flight based on airline_name and departure_date
SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name,departure_date, departure_time, arrival_date, arrival_time, status 
FROM flight 
WHERE airline_name = %s 
	AND departure_date BETWEEN %s AND %s;

--view flight based on airline_name, departure_date, and arrival_airport_name	
SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name, departure_date, departure_time, arrival_date, arrival_time, status 
FROM flight 
WHERE airline_name = %s 
	AND departure_date BETWEEN %s AND %s 
	AND arrival_airport_name=%s;
	
--view flight based on airline_name, departure_date, arrival_airport_name, and departure_airport_name 	
SELECT DISTINCT flight_number,  departure_airport_name, arrival_airport_name, departure_date, departure_time, arrival_date, arrival_time, status 
FROM flight 
WHERE airline_name = %s 
	AND departure_date BETWEEN %s AND %s 
	AND arrival_airport_name=%s 
	AND departure_airport_name=%s;
	
--search for flights on a specific day
SELECT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, arrival_airport_name, arrival_date, sold_price, status 
FROM flight, airport as S, airport as T 
WHERE departure_airport_name = S.name
	AND arrival_airport_name = T.name 
	AND S.city = %s 
	AND T.city = %s 
	AND departure_date = %s;
	
--search for future flights
SELECT flight.airline_name, flight.flight_number, departure_airport_name, departure_date, arrival_airport_name, arrival_date, sold_price, status
FROM flight, airport as S, airport as T 
WHERE departure_airport_name = S.name 
	AND arrival_airport_name = T.name 
	AND S.city = %s 
	AND T.city = %s 
	AND flight_number = %s 
	AND CONCAT(departure_date, " ", departure_time) > SYSDATE();

--create new flights
INSERT INTO Flight VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);

--change flight status
UPDATE Flight 
SET status = %s 
WHERE airline_name = %s
	AND flight_number = %s 
	AND departure_date = %s;
	
--add airplane
INSERT INTO Airplane VALUES(%s,%s,%s);

--add airport
INSERT INTO Airport VALUES(%s,%s);

--view the most frequent customer
SELECT customer.name, customer.email, %s ,date_of_birth, city, state, passport_country, COUNT(DISTINCT purchases.ticket_id) AS counter 
FROM customer, purchases, ticket 
WHERE customer.email = customer_email 
	AND purchases.ticket_id = ticket.ticket_id 
	AND airline_name = %s 
GROUP BY customer.name, customer.email, date_of_birth, city, state, passport_country, %s 
ORDER BY counter 
DESC LIMIT 1;

--view month_wise tickets sold
SELECT COUNT(t.ticket_id) total_ticket_num
FROM ticket t, purchases p
WHERE airline_name = %s
	AND t.ticket_id = p.ticket_id
	AND YEAR(p.purchased_date) = %s
	AND MONTH(p.purchased_date) = %s;

--view annually revenue earned 
SELECT SUM(t.sold_price) annual
FROM purchases p , ticket t, flight f
WHERE p.ticket_id = t.ticket_id
	AND (t.airline_name,t.flight_number) = (f.airline_name,f.flight_number)
	AND f.airline_name = %s
	AND YEAR(p.purchased_date) = %s;
	
--view month_wise revenue earned 
SELECT COUNT(t.ticket_id) total_ticket_num
FROM ticket t, purchases p
WHERE airline_name = %s
	AND t.ticket_id = p.ticket_id
	AND YEAR(p.purchased_date) = %s
	AND MONTH(p.purchased_date) = %s;

--view top3 destinations for last year
SELECT Airport.city, COUNT(ticket_id) as traffic_num
FROM Airport as a, Flight as f,Ticket as t
WHERE a.name = f.arrival_airport_name
	AND (f.airline_name, f.flight_number) = (t.airline_name,t.flight_number)
	AND f.status != "Cancelled"
	AND f.airline_name = '%s'
	AND year(f.arrival_date) = %s
	AND year(f.arrival_time) = %s
	AND t.ticket_id in (SELECT ticket_id FROM Purchases)
GROUP BY Airport.city
ORDER BY traffic_num DESC
LIMIT 3;
	
--view top3 destinations of past three months
SELECT a.city airport_city, COUNT(*) traffic_num 
FROM airport a, flight f, ticket t
WHERE a.name = f.arrival_airport_name
	AND (f.airline_name, f.flight_number) = (t.airline_name, t.flight_number)
	AND f.status != "Cancelled"
	AND f.airline_name = %s
	AND f.arrival_date <= %s
	AND f.arrival_date >= %s
	AND t.ticket_id in (SELECT ticket_id FROM purchases)
GROUP BY airport_city
ORDER BY traffic_num DESC
LIMIT 3;

--view average rate 
SELECT flight_num, AVG(rating) as avr 
FROM comments 
WHERE airline_name = %s 
GROUP BY flight_num;

--view all the rates and comments 
SELECT *
FROM comments 
WHERE airline_name = %s 
GROUP BY flight_num;

--view a customer's flight info in one specific airline 	
SELECT DISTINCT flight.flight_number, departure_airport_name, arrival_airport_name, departure_date, arrival_date 
FROM purchases NATURAL JOIN ticket NATURAL JOIN flight 
WHERE customer_email = %s 
	AND flight.airline_name = %s;
	
--view customer info
SELECT DISTINCT name, email,flight.flight_number, date_of_birth,city, state, passport_country, %s 
FROM customer, purchases NATURAL JOIN ticket, flight 
WHERE customer.email = purchases.customer_email 
	AND flight.flight_number = ticket.flight_number 
	AND flight.airline_name = %s 
	AND flight.flight_number = %s 
	AND flight.departure_date = %s;













