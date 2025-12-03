# lib/employee.py
import sqlite3
from department import Department

CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()

class Employee:

    def __init__(self, name, job_title, salary, department_id=None, id=None):
        self.id = id
        self.name = name
        self.job_title = job_title
        self.salary = salary
        self.department_id = department_id

    def __repr__(self):
        return f"<Employee {self.id}: {self.name}, {self.job_title}, Ksh {self.salary}>"

    # ------------------------------
    # TABLE METHODS
    # ------------------------------
    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT,
                job_title TEXT,
                salary INTEGER,
                department_id INTEGER,
                FOREIGN KEY(department_id) REFERENCES departments(id)
            );
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF_EXISTS employees;")
        CONN.commit()

    # ------------------------------
    # INSTANCE METHODS
    # ------------------------------
    def save(self):
        if self.id:
            self.update()
        else:
            CURSOR.execute("""
                INSERT INTO employees (name, job_title, salary, department_id)
                VALUES (?, ?, ?, ?)
            """, (self.name, self.job_title, self.salary, self.department_id))
            self.id = CURSOR.lastrowid
            CONN.commit()
        return self

    def update(self):
        CURSOR.execute("""
            UPDATE employees
            SET name = ?, job_title = ?, salary = ?, department_id = ?
            WHERE id = ?
        """, (self.name, self.job_title, self.salary, self.department_id, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute("DELETE FROM employees WHERE id = ?", (self.id,))
        CONN.commit()

    # ------------------------------
    # CLASS HELPERS
    # ------------------------------
    @classmethod
    def instance_from_db(cls, row):
        return cls(
            name=row[1],
            job_title=row[2],
            salary=row[3],
            department_id=row[4],
            id=row[0]
        )

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM employees").fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM employees WHERE id = ?", (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute("SELECT * FROM employees WHERE name = ?", (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    # ------------------------------
    # RELATIONSHIP
    # ------------------------------
    def department(self):
        """Return the department this employee belongs to."""
        return Department.find_by_id(self.department_id)
