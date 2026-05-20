import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:2006@localhost/car_service")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/statistics',)
def stats():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT COALESCE(SUM(total_amount), 0) AS total_revenue FROM orders WHERE completed_at IS NOT NULL")
    total_revenue = cur.fetchone()['total_revenue']

    cur.execute("""
        SELECT COUNT(DISTINCT id) AS total_clients
        FROM clients 
    """)
    total_clients = cur.fetchone()['total_clients']

    cur.execute("""
        SELECT 
            p.id,
            p.name,
            p.article,
            p.price,
            COALESCE(SUM(op.quantity), 0) AS total_sold
        FROM parts p
        LEFT JOIN order_parts op ON p.id = op.part_id
        LEFT JOIN orders o ON op.order_id = o.id AND o.completed_at IS NOT NULL
        GROUP BY p.id, p.name, p.article, p.price
        ORDER BY total_sold DESC, p.name
    """)
    parts_sales = cur.fetchall()
    cur.execute("""
        SELECT 
            s.id,
            s.name,
            s.price,
            COUNT(os.order_id) AS total_done
        FROM services s
        LEFT JOIN order_services os ON s.id = os.service_id
        LEFT JOIN orders o ON os.order_id = o.id AND o.completed_at IS NOT NULL
        GROUP BY s.id, s.name, s.price
        ORDER BY total_done DESC, s.name
    """)
    services_sales = cur.fetchall()

    cur.execute("""
        SELECT 
            e.id,
            e.full_name,
            COUNT(oe.order_id) AS orders_done
        FROM employees e
        LEFT JOIN order_employees oe ON e.id = oe.employee_id
        LEFT JOIN orders o ON oe.order_id = o.id AND o.completed_at IS NOT NULL
        GROUP BY e.id, e.full_name
        ORDER BY orders_done DESC, e.full_name
    """)
    employees_stats = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('statistics.html',
                           total_revenue=total_revenue,
                           total_clients=total_clients,
                           parts_sales=parts_sales,
                           services_sales=services_sales,
                           employees_stats=employees_stats)

@app.route('/orders')
def orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            o.id,
            c.full_name AS client_name,
            CONCAT(cr.brand, ' ', cr.model, ' (', COALESCE(cr.year::TEXT, '-'), ')') AS car,
            o.description,
            o.started_at,
            o.completed_at,
            o.total_amount
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        JOIN cars cr ON o.car_id = cr.id
        ORDER BY o.started_at DESC
    """)
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('orders.html', orders=orders)


@app.route('/orders/<int:order_id>/complete', methods=['POST'])
def complete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT completed_at FROM orders WHERE id = %s", (order_id,))
    row = cur.fetchone()

    cur.execute("""
        SELECT COALESCE(SUM(s.price), 0) AS services_total
        FROM order_services os
        JOIN services s ON os.service_id = s.id
        WHERE os.order_id = %s
    """, (order_id,))
    services_total = cur.fetchone()['services_total']

    cur.execute("""
        SELECT COALESCE(SUM(p.price * op.quantity), 0) AS parts_total
        FROM order_parts op
        JOIN parts p ON op.part_id = p.id
        WHERE op.order_id = %s
    """, (order_id,))
    parts_total = cur.fetchone()['parts_total']

    total_amount = services_total + parts_total

    cur.execute("""
        UPDATE orders 
        SET completed_at = NOW(), total_amount = %s 
        WHERE id = %s
    """, (total_amount, order_id))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('orders'))

@app.route('/clients')
def clients():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM clients ORDER BY id DESC")
    clients = cur.fetchall()

    cur.close()
    conn.close()
    return render_template('clients.html', clients=clients)

@app.route('/clients', methods=['POST'])
def add_client():
    full_name = request.form['full_name']
    phone = request.form.get('phone')
    email = request.form.get('email')
    address = request.form.get('address')
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO clients (full_name, phone, email, address) VALUES (%s, %s, %s, %s)",
        (full_name, phone, email, address)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('clients'))


@app.route('/cars/<int:client_id>')
def cars(client_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients WHERE id = %s", (client_id,))
    client = cur.fetchone()
    cur.execute("SELECT * FROM cars WHERE client_id = %s", (client_id,))
    cars = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('cars.html', client=client, cars=cars)

@app.route('/cars', methods=['POST'])
def add_car():
    client_id = request.form['client_id']
    brand = request.form['brand']
    model = request.form['model']
    year = request.form.get('year') or None
    vin = request.form.get('vin') or None
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO cars (client_id, brand, model, year, vin) VALUES (%s, %s, %s, %s, %s)",
        (client_id, brand, model, year, vin)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('cars', client_id=client_id))


@app.route('/orders/new', methods=['GET', 'POST'])
def new_order_form():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT id, full_name FROM clients")
    clients = cur.fetchall()
    
    cur.execute("SELECT id, name, price FROM services")
    services = cur.fetchall()
    
    cur.execute("SELECT id, name, article, price FROM parts")
    parts = cur.fetchall()
    
    cur.execute("SELECT id, full_name FROM employees")
    employees = cur.fetchall()
    
    cars = []
    selected_client_id = request.form.get('client_id')
    if selected_client_id:
        cur.execute("SELECT id, brand, model, year, vin FROM cars WHERE client_id = %s",(selected_client_id,))
        cars = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template('new_order.html',
                           clients=clients,
                           services=services,
                           parts=parts,
                           employees=employees,
                           cars=cars,
                           selected_client_id=selected_client_id
                           )



#для кнопки оформить заказ
@app.route('/orders/create', methods=['POST'])
def create_order():
    client_id = request.form['client_id']
    car_id = request.form['car_id']
    description = request.form.get('description') or None
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO orders (client_id, car_id, description, started_at) VALUES (%s, %s, %s, NOW()) RETURNING id",
        (client_id, car_id, description)
    )
    order_id = cur.fetchone()['id']
    
    service_ids = request.form.getlist('service_ids')
    for sid in service_ids:
        cur.execute("INSERT INTO order_services (order_id, service_id) VALUES (%s, %s)", (order_id, sid))
    
    part_ids = request.form.getlist('part_ids')
    quantities = request.form.getlist('quantities')
    for pid, qty in zip(part_ids, quantities):
        if qty.isdigit() and int(qty) > 0:
            cur.execute(
                "INSERT INTO order_parts (order_id, part_id, quantity) VALUES (%s, %s, %s)",
                (order_id, pid, int(qty))
            )
    
    emp_ids = request.form.getlist('employee_ids')
    for eid in emp_ids:
        cur.execute("INSERT INTO order_employees (order_id, employee_id) VALUES (%s, %s)", (order_id, eid))
    
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('new_order_form'))


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
