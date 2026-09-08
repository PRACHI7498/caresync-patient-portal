CREATE TABLE patient (patient_id INT PRIMARY KEY, name VARCHAR(100), age INT, gender VARCHAR(10), contact VARCHAR(15));

CREATE TABLE doctor (doctor_id INT PRIMARY KEY, name VARCHAR(100), specialty VARCHAR(100), email VARCHAR(100));

CREATE TABLE appointment (appointment_id INT PRIMARY KEY, patient_id INT, doctor_id INT, appointment_date DATE, status VARCHAR(20), FOREIGN KEY (patient_id) REFERENCES patient(patient_id), FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id));

CREATE TABLE billing (billing_id INT PRIMARY KEY, appointment_id INT, amount DECIMAL(10,2), billing_date DATE, payment_status VARCHAR(20), FOREIGN KEY (appointment_id) REFERENCES appointment(appointment_id));

CREATE TABLE activity_log (log_id INT PRIMARY KEY, user_id INT, action VARCHAR(100), timeslmed DATETIME);
