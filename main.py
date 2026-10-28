import json

# ===== 1. STACK (Struktur Data) =====
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop() if self.items else None
    def is_empty(self):
        return len(self.items) == 0

# ===== 2. RULE BONUS - POLYMORPHISM =====
class BonusRule:
    def calculate(self, salary): 
        return 0

class Perf2026Rule(BonusRule): # Override
    def calculate(self, salary): 
        return salary * 0.20

class Senior10Rule(BonusRule):
    def calculate(self, salary): 
        return salary * 0.10

class Lead2026Rule(BonusRule):
    def calculate(self, salary): 
        return salary * 0.25

class NoBonusRule(BonusRule):
    def calculate(self, salary): 
        return 0

def get_bonus_rule(code):
    if code == "PERF2026": 
        return Perf2026Rule()
    if code == "SENIOR10": 
        return Senior10Rule()
    if code == "LEAD2026": 
        return Lead2026Rule()
    return NoBonusRule()

# ===== 3. EMPLOYEE - INHERITANCE & OVERRIDE =====
class Employee:
    def __init__(self, emp_id, name, base_salary, is_permanent, bonus_code):
        self.emp_id = emp_id
        self.name = name
        self.base_salary = base_salary
        self.is_permanent = is_permanent
        self.bonus_rule = get_bonus_rule(bonus_code)
    
    def calculate_salary(self): # Akan di-override
        bonus = self.bonus_rule.calculate(self.base_salary)
        return self.base_salary + bonus

class PermanentEmployee(Employee): # Inheritance
    def calculate_salary(self): # Override
        bonus = self.bonus_rule.calculate(self.base_salary)
        tunjangan_tetap = self.base_salary * 0.10
        return self.base_salary + bonus + tunjangan_tetap

class ContractEmployee(Employee): # Inheritance
    def calculate_salary(self): # Override
        bonus = self.bonus_rule.calculate(self.base_salary)
        return self.base_salary + bonus

# ===== 4. SENSOR - INHERITANCE & POLYMORPHISM =====
class SensorReading:
    def __init__(self, sensor_id, location, temperature, status, operator_id):
        self.sensor_id = sensor_id
        self.location = location
        self.temperature = temperature
        self.status = status
        self.operator_id = operator_id
    def get_action(self):
        return "Cek manual"

class DangerSensor(SensorReading):
    def get_action(self): # Override
        return "BAHAYA! EVAKUASI & MATIKAN MESIN!"

class WarningSensor(SensorReading):
    def get_action(self):
        return "WARNING! Perlu pengecekan segera"

class NormalSensor(SensorReading):
    def get_action(self):
        return "Aman - Lanjutkan operasi"

def sensor_factory(data): # Polymorphism factory
    if data['status'] == 'DANGER' or data['temperature'] > 80:
        return DangerSensor(**data)
    elif data['status'] == 'WARNING' or data['temperature'] > 60:
        return WarningSensor(**data)
    else:
        return NormalSensor(**data)

# ===== 5. MAIN PROGRAM =====
print("=== UTS OOP STMIK WIDYA UTAMA ===\n")

# Load Employee
with open('employee.json') as f:
    emp_data = json.load(f)

stack_emp = Stack()
for e in emp_data['employees']:
    if e['is_permanent']:
        obj = PermanentEmployee(e['emp_id'], e['name'], e['base_salary'], e['is_permanent'], e['bonus_code'])
    else:
        obj = ContractEmployee(e['emp_id'], e['name'], e['base_salary'], e['is_permanent'], e['bonus_code'])
    stack_emp.push(obj)

print("--- GAJI KARYAWAN (pakai Stack LIFO) ---")
while not stack_emp.is_empty():
    emp = stack_emp.pop()
    print(f"{emp.emp_id} | {emp.name} | Total Gaji: Rp {emp.calculate_salary():,.0f} | Rule: {emp.bonus_rule.__class__.__name__}")

# Load Sensor
with open('sensor_logs.json') as f:
    sensor_data = json.load(f)

print("\n--- SENSOR LOG (Polymorphism) ---")
stack_sensor = Stack()
for s in sensor_data['readings']:
    obj = sensor_factory(s)
    stack_sensor.push(obj)

while not stack_sensor.is_empty():
    s = stack_sensor.pop()
    print(f"{s.sensor_id} di {s.location} Suhu {s.temperature}°C -> {s.get_action()}")

print("\n=== SELESAI ===")