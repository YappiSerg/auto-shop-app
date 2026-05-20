PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_employees;
DROP TABLE IF EXISTS order_parts;
DROP TABLE IF EXISTS order_services;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS services;
DROP TABLE IF EXISTS parts;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS cars;
DROP TABLE IF EXISTS clients;

CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT
);

CREATE TABLE cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    brand VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    year INTEGER,
    vin VARCHAR(17) UNIQUE,
    CONSTRAINT fk_cars_client
        FOREIGN KEY (client_id)
        REFERENCES clients (id)
        ON DELETE CASCADE
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    car_id INTEGER NOT NULL,
    description TEXT,
    started_at TEXT,
    completed_at TEXT,
    total_amount DECIMAL(10, 2),
    CONSTRAINT fk_orders_client
        FOREIGN KEY (client_id)
        REFERENCES clients (id)
        ON DELETE RESTRICT,
    CONSTRAINT fk_orders_car
        FOREIGN KEY (car_id)
        REFERENCES cars (id)
        ON DELETE RESTRICT
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20)
);

CREATE TABLE parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    article VARCHAR(100),
    manufacturer VARCHAR(100),
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE order_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    service_id INTEGER NOT NULL,
    CONSTRAINT fk_order_services_order
        FOREIGN KEY (order_id)
        REFERENCES orders (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_order_services_service
        FOREIGN KEY (service_id)
        REFERENCES services (id)
        ON DELETE RESTRICT
);

CREATE TABLE order_parts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    part_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    CONSTRAINT fk_order_parts_order
        FOREIGN KEY (order_id)
        REFERENCES orders (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_order_parts_part
        FOREIGN KEY (part_id)
        REFERENCES parts (id)
        ON DELETE RESTRICT
);

CREATE TABLE order_employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    CONSTRAINT fk_order_employees_order
        FOREIGN KEY (order_id)
        REFERENCES orders (id)
        ON DELETE CASCADE,
    CONSTRAINT fk_order_employees_employee
        FOREIGN KEY (employee_id)
        REFERENCES employees (id)
        ON DELETE RESTRICT
);

INSERT INTO clients (id, full_name, phone, email, address) VALUES
(1, 'Иванов Иван Иванович', '+79001234567', 'ivanov@example.com', 'г. Москва, ул. Ленина, д. 10'),
(2, 'Петрова Анна Сергеевна', '+79012345678', 'petrova.anna@mail.ru', 'г. Санкт-Петербург, Невский пр., 25'),
(3, 'Сидоров Дмитрий Владимирович', '+79023456789', 'sidorov.dv@gmail.com', 'г. Казань, ул. Баумана, 52'),
(4, 'Козлова Екатерина Андреевна', '+79034567890', NULL, 'г. Новосибирск, ул. Советская, 100'),
(5, 'Морозов Алексей Павлович', '+79045678901', 'morozov.ap@yandex.ru', 'г. Екатеринбург, ул. Малышева, 33');

INSERT INTO cars (id, client_id, brand, model, year, vin) VALUES
(1, 1, 'Toyota', 'Camry', 2020, 'VIN123456789012345'),
(2, 1, 'Lada', 'Granta', 2018, 'VIN123456789012346'),
(3, 2, 'BMW', 'X5', 2022, 'VIN234567890123456'),
(4, 3, 'Kia', 'Rio', 2019, 'VIN345678901234567'),
(5, 4, 'Hyundai', 'Solaris', 2021, 'VIN456789012345678'),
(6, 5, 'Audi', 'A4', 2023, 'VIN567890123456789');

INSERT INTO employees (id, full_name, phone) VALUES
(1, 'Смирнов Андрей Васильевич', '+7 (910) 111-22-33'),
(2, 'Кузнецов Пётр Игоревич', '+7 (911) 222-33-44'),
(3, 'Волков Сергей Николаевич', '+7 (912) 333-44-55'),
(4, 'Лебедев Максим Олегович', '+7 (913) 444-55-66');

INSERT INTO services (id, name, description, price) VALUES
(1, 'Замена масла', 'Замена моторного масла и масляного фильтра', 1200.00),
(2, 'Диагностика двигателя', 'Компьютерная диагностика ЭБУ двигателя', 1500.00),
(3, 'Замена тормозных колодок (перед)', 'Замена передних тормозных колодок', 2500.00),
(4, 'Замена тормозных колодок (зад)', 'Замена задних тормозных колодок', 2200.00),
(5, 'Развал-схождение', 'Компьютерная регулировка углов установки колёс', 2000.00),
(6, 'Замена воздушного фильтра', 'Замена салонного и воздушного фильтра', 800.00),
(7, 'Шиномонтаж (1 колесо)', 'Снятие/установка, балансировка', 600.00),
(8, 'Замена свечей зажигания', 'Замена комплекта свечей', 1800.00),
(9, 'ТО-1 (до 15 000 км)', 'Минимальное техническое обслуживание', 3500.00),
(10, 'ТО-2 (до 30 000 км)', 'Расширенное техническое обслуживание', 6500.00);

INSERT INTO parts (id, name, article, manufacturer, price) VALUES
(1, 'Масло моторное 5W-30', 'OIL-5W30-4L', 'Shell', 3200.00),
(2, 'Масляный фильтр', 'FILTER-OIL-123', 'Mann', 850.00),
(3, 'Тормозные колодки передние', 'BRAKE-FRONT-456', 'Bosch', 2100.00),
(4, 'Тормозные колодки задние', 'BRAKE-REAR-789', 'TRW', 1750.00),
(5, 'Воздушный фильтр', 'FILTER-AIR-101', 'Knecht', 550.00),
(6, 'Салонный фильтр', 'FILTER-CABIN-202', 'UFI', 620.00),
(7, 'Свеча зажигания', 'SPARK-NGK-303', 'NGK', 420.00),
(8, 'Ремень ГРМ', 'BELT-TIMING-404', 'Gates', 4300.00),
(9, 'Амортизатор передний левый', 'SHOCK-FRONT-L-505', 'KYB', 5200.00),
(10, 'Аккумулятор 60 Ач', 'BATTERY-60-606', 'Varta', 7500.00),
(11, 'Лампа ближнего света H7', 'BULB-H7-707', 'Osram', 480.00),
(12, 'Жидкость охлаждающая 5 л', 'COOLANT-5L-808', 'Liqui Moly', 1100.00);

INSERT INTO orders (id, client_id, car_id, description, started_at, completed_at, total_amount) VALUES
(1, 1, 1, 'Плановое обслуживание автомобиля', '2025-05-01 10:00:00', '2025-05-01 13:00:00', 6750.00),
(2, 2, 3, 'Замена передних тормозных колодок', '2025-05-02 11:30:00', '2025-05-02 15:00:00', 4600.00),
(3, 3, 4, 'Регулировка развала-схождения', '2025-05-03 09:00:00', NULL, NULL),
(4, 4, 5, 'Замена воздушного и салонного фильтра', '2025-05-04 12:00:00', '2025-05-04 13:30:00', 1970.00);

INSERT INTO order_services (id, order_id, service_id) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 3, 5),
(5, 4, 6);

INSERT INTO order_parts (id, order_id, part_id, quantity) VALUES
(1, 1, 1, 1),
(2, 1, 2, 1),
(3, 2, 3, 1),
(4, 4, 5, 1),
(5, 4, 6, 1);

INSERT INTO order_employees (id, order_id, employee_id) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 2, 3),
(4, 3, 3),
(5, 4, 4);
