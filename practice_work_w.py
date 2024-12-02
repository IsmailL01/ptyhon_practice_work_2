import getpass
import json
import os
from datetime import datetime

# Структура данных
users = []
employees = []
change_log = []

# Загрузка данных из файлов
def load_data():
    global users, employees, change_log
    if os.path.exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            users = data.get('users', [])
            employees = data.get('employees', [])
    if os.path.exists('change_log.json'):
        with open('change_log.json', 'r', encoding='utf-8') as f:
            change_log = json.load(f)

# Сохранение данных в файлы
def save_data():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump({'users': users, 'employees': employees}, f, ensure_ascii=False, indent=4)
    with open('change_log.json', 'w', encoding='utf-8') as f:
        json.dump(change_log, f, ensure_ascii=False, indent=4)

# Функции для пользователей
def user_menu(user):
    while True:
        print("\nДобро пожаловать, {}!".format(user['name']))
        print("Выберите действие:")
        print("1. Просмотреть информацию о себе")
        print("2. Обновить информацию")
        print("3. Выйти")

        choice = input("Ваш выбор: ")
        if choice == '1':
            view_self_info(user)
        elif choice == '2':
            update_self_info(user)
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def view_self_info(user):
    print("\nИнформация о вас:")
    print("ID: {}".format(user['employee_id']))
    print("Имя: {}".format(user['name']))
    print("Отдел: {}".format(user['department']))
    print("Дата создания учетной записи: {}".format(user['created_at']))

def update_self_info(user):
    print("\nОбновление информации о себе:")
    while True:
        print("Текущая информация:")
        print("Имя: {}".format(user['name']))
        print("Отдел: {}".format(user['department']))
        
        new_name = input("Введите новое имя (оставьте пустым для пропуска): ")
        if new_name:
            user['name'] = new_name

        new_department = input("Введите новый отдел (оставьте пустым для пропуска): ")
        if new_department:
            user['department'] = new_department

        new_password = getpass.getpass("Введите новый пароль (оставьте пустым для пропуска): ")
        if new_password:
            user['password'] = new_password

        log_change("Обновление информации о пользователе: {}".format(user['username']))
        print("Информация обновлена.")
        save_data()  # Сохраняем данные после обновления
        break

def log_change(action):
    change_log.append({
        'action': action,
        'timestamp': datetime.now().isoformat()
    })

# Функции для администраторов
def admin_menu():
    while True:
        print("\nДобро пожаловать, администратор!")
        print("Выберите действие:")
        print("1. Добавить сотрудника")
        print("2. Удалить сотрудника")
        print("3. Редактировать данные сотрудника")
        print("4. Просмотреть всех сотрудников")
        print("5. Поиск сотрудников")
        print("6. Управление ролями")
        print("7. Просмотреть историю изменений")
        print("8. Выйти")

        choice = input("Ваш выбор: ")
        if choice == '1':
            add_employee()
        elif choice == '2':
            remove_employee()
        elif choice == '3':
            edit_employee()
        elif choice == '4':
            view_all_employees()
        elif choice == '5':
            search_employees()
        elif choice == '6':
            manage_roles()
        elif choice == '7':
            view_change_log()
        elif choice == '8':
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def add_employee():
    name = input("Введите имя сотрудника: ")
    department = input("Введите отдел: ")
    employee_id = len(employees) + 1
    employees.append({'employee_id': employee_id, 'name': name, 'department': department})
    print("Сотрудник добавлен.")
    log_change("Добавлен сотрудник: {}".format(name))
    save_data()  # Сохраняем данные после добавления

def remove_employee():
    employee_id = int(input("Введите ID сотрудника для удаления: "))
    global employees
    employees = [emp for emp in employees if emp['employee_id'] != employee_id]
    print("Сотрудник удален.")
    log_change("Удален сотрудник с ID: {}".format(employee_id))
    save_data()  # Сохраняем данные после удаления

def edit_employee():
    employee_id = int(input("Введите ID сотрудника для редактирования: "))
    for emp in employees:
        if emp['employee_id'] == employee_id:
            new_name = input("Введите новое имя (оставьте пустым для пропуска): ")
            new_department = input("Введите новый отдел (оставьте пустым для пропуска): ")
            if new_name:
                emp['name'] = new_name
            if new_department:
                emp['department'] = new_department
            print("Данные сотрудника обновлены.")
            log_change("Редактированы данные сотрудника с ID: {}".format(employee_id))
            save_data()  # Сохраняем данные после редактирования
            return
    print("Сотрудник не найден.")

def view_all_employees():
    print("\nСписок сотрудников:")
    for emp in employees:
        print("ID: {}, Имя: {}, Отдел: {}".format(emp['employee_id'], emp['name'], emp['department']))

def search_employees():
    search_term = input("Введите имя или отдел для поиска: ").lower()
    found_employees = [emp for emp in employees if search_term in emp['name'].lower() or search_term in emp['department'].lower()]
    
    if found_employees:
        print("\nНайденные сотрудники:")
        for emp in found_employees:
            print("ID: {}, Имя: {}, Отдел: {}".format(emp['employee_id'], emp['name'], emp['department']))
    else:
        print("Сотрудники не найдены.")

def manage_roles():
    username = input("Введите логин пользователя для изменения роли: ")
    user = next((u for u in users if u['username'] == username), None)
    if user:
        new_role = input("Введите новую роль (user/admin): ")
        if new_role in ['user', 'admin']:
            user['role'] = new_role
            print("Роль пользователя обновлена.")
            log_change("Роль пользователя {} изменена на {}".format(username, new_role))
            save_data()  # Сохраняем данные после изменения роли
        else:
            print("Неверная роль. Попробуйте снова.")
    else:
        print("Пользователь не найден.")

def view_change_log():
    print("\nИстория изменений:")
    for log in change_log:
        print("Действие: {}, Время: {}".format(log['action'], log['timestamp']))

def register_user():
    username = input("Введите логин: ")
    if any(u['username'] == username for u in users):
        print("Пользователь с таким логином уже существует.")
        return
    name = input("Введите имя: ")
    department = input("Введите отдел: ")
    password = getpass.getpass("Введите пароль: ")
    created_at = datetime.now().isoformat()
    users.append({
        'username': username,
        'name': name,
        'department': department,
        'password': password,
        'role': 'user',
        'created_at': created_at
    })
    print("Пользователь зарегистрирован.")
    log_change("Зарегистрирован новый пользователь: {}".format(username))
    save_data()  # Сохраняем данные после регистрации

# Основная функция
def main():
    load_data()  # Загружаем данные при запуске
    while True:
        print("\nПожалуйста, авторизуйтесь.")
        username = input("Логин: ")
        password = getpass.getpass("Пароль: ")

        # Проверка учетных данных
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)

        if user:
            if user['role'] == 'user':
                user_menu(user)
            elif user['role'] == 'admin':
                admin_menu()
        else:
            print("Неверный логин или пароль. Попробуйте снова.")
            if input("Хотите зарегистрироваться? (да/нет): ").lower() == 'да':
                register_user()

if __name__ == "__main__":
    main()
