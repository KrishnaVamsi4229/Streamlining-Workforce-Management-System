from flask import *
import sqlite3

app = Flask(__name__)

database = 'hr.db'

def get_db_connection():
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection

@app.route('/')
def index():
    connection = get_db_connection()
    employees = connection.execute('SELECT * FROM employees').fetchall()
    connection.close()
    return render_template('index.html', employees=employees)

@app.route('/employee/<int:id>')
def employee_detail(id):
    connection = get_db_connection()
    employee = connection.execute('SELECT * FROM employees WHERE id = ?', (id,)).fetchone()
    connection.close()
    return render_template('employee_detail.html', employee=employee)

@app.route('/create', methods=('GET', 'POST'))
def create_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']
        performance_score = request.form['performance_score']
        
        connection = get_db_connection()
        connection.execute('INSERT INTO employees (name, position, salary, performance_score) VALUES (?, ?, ?, ?)',
                     (name, position, salary, performance_score))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))
    return render_template('create_employee.html')

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update_employee(id):
    connection = get_db_connection()
    employee = connection.execute('SELECT * FROM employees WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']
        performance_score = request.form['performance_score']
        
        connection.execute('UPDATE employees SET name = ?, position = ?, salary = ?, performance_score = ? WHERE id = ?',
                     (name, position, salary, performance_score, id))
        connection.commit()
        connection.close()
        return redirect(url_for('index'))

    connection.close()
    return render_template('update_employee.html', employee=employee)

@app.route('/delete/<int:id>', methods=('POST',))
def delete_employee(id):
    connection = get_db_connection()
    connection.execute('DELETE FROM employees WHERE id = ?', (id,))
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

    
@app.route('/generate_performance_report/<int:id>')
def generate_performance_report(id):
    connection = get_db_connection()
    employee = connection.execute('SELECT * FROM employees WHERE id = ?', (id,)).fetchone()
    connection.close()
    
    if employee:
        performance_score = employee['performance_score']
        return render_template('performance_report.html', employee=employee, performance_score=performance_score)
    else:
        return 'Employee not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)


