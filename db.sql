CREATE TABLE IF NOT EXISTS roles(
	id SERIAL primary key,
	code text,
	label text
);


INSERT INTO roles (code, label) VALUES ('admin', 'Administrator');
INSERT INTO roles (code, label) VALUES ('manager', 'Manager');
INSERT INTO roles (code, label) VALUES ('employee', 'Employee');


CREATE TABLE IF NOT EXISTS users (
    id serial PRIMARY KEY,
    login text UNIQUE NOT NULL,
    psw text NOT NULL,
    date timestamp NOT null,
    roles_id INT REFERENCES roles(id)
);

INSERT INTO users (login, psw, date, roles_id) VALUES ('dima', 'pbkdf2:sha256:260000$UQ2QN62E7kGiCmkx$9dbe6b8ac48de55a356f1f49e3be03027e488f7f9f5c8dd1dbc2d30cb724040b', '2023-01-01',1);

CREATE TABLE IF NOT EXISTS departments (
    id SERIAL PRIMARY KEY,
    department_name TEXT NOT NULL,
    description TEXT
);

INSERT INTO departments (department_name, description) VALUES ('ОАИС', 'Отдел аудита информационных систем');


CREATE TABLE IF NOT EXISTS profiles (
    id serial PRIMARY KEY,
    name text NOT NULL,
    working_day numeric NOT NULL,
    user_id INT UNIQUE REFERENCES users(id),
    departments_id INT REFERENCES departments(id)

);
INSERT INTO profiles (name, working_day, departments_id, user_id) VALUES ('Павлов Дмитрий Вячеславович', '0.5', 1, 1);





CREATE TABLE overtime_report (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    task_description TEXT NOT NULL,
    task_date DATE NOT NULL,
    day_type VARCHAR(50) NOT NULL CHECK (day_type IN ('Выходной', 'Рабочий', 'Отпускной', 'Больничный', 'Командировочный')),
    hours_worked DECIMAL(5, 1) NOT NULL,
    profiles_id INTEGER NOT NULL,
    show_bool BOOLEAN DEFAULT true,
    FOREIGN KEY (profiles_id) REFERENCES profiles(id)
);


CREATE TABLE project_accounting (
    id SERIAL PRIMARY KEY,
    num TEXT,
    project_name TEXT NOT null
);


CREATE TABLE project_reports (
    id SERIAL PRIMARY KEY, 
    project_id INTEGER NOT NULL,  -- сведения о проекте
    profiles_id INTEGER NOT NULL, 
    report_date DATE NOT NULL,
    location_work VARCHAR(255) NOT NULL, -- указывает на место работы (выезд/офис).
    hours_spent NUMERIC(5, 1) NOT NULL, -- указывает количество затраченных часов
    works TEXT, -- сокращенное наименование
    clarification text, -- содержит дополнительные уточнения по работе (это поле может быть пустым)
	FOREIGN KEY (profiles_id) REFERENCES profiles(id),
	FOREIGN KEY (project_id) REFERENCES project_accounting(id)
);

-- CREATE TABLE IF NOT EXISTS work_report (
--     id SERIAL PRIMARY KEY,
--     project_id INT NOT NULL,
--     profiles_id INT NOT NULL,
--     project_date DATE NOT NULL,
--     task_performed TEXT NOT NULL,
--     hours_spent NUMERIC NOT NULL,
--     FOREIGN KEY (profiles_id) REFERENCES profiles(id),
--     FOREIGN KEY (project_id) REFERENCES project_accounting(id)
-- );
