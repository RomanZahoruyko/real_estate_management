from database_setup import setup_database
from simple_request import *
from business_logic import add_lease_contract, update_lease_contract, delete_lease_contract, update_reporting
from models import Tenant, Owner, Property, LeaseContract, Payments, Reporting, engine
from reports import generate_word_report

setup_database()


def manage_properties():
    while True:
        print("\nОблік об'єктів нерухомості:")
        print("1) Переглянути всі об'єкти")
        print("2) Додати новий об'єкт")
        print("3) Оновити ціну об'єкта")
        print("4) Редагувати адресу об'єкта")
        print("5) Видалити об'єкт")
        print("6) Повернутися до головного меню")

        try:
            choice = int(input("Виберіть дію (1-6): "))
            if choice == 1:
                print_records(Property)

            elif choice == 2:
                address = input("Введіть адресу об'єкта: ")
                price = float(input("Введіть ціну об'єкта: "))
                owner_id = int(input("Введіть ID власника: "))
                type_ids = list(map(int, input("Введіть ID типів (через пробіл): ").split()))

                create_record(Property, address=address, price=price, owner_id=owner_id)  # Передаємо значення
                print("Об'єкт додано успішно.")

            elif choice == 3:
                property_id = int(input("Введіть ID об'єкта для оновлення ціни: "))
                new_price = float(input("Введіть нову ціну: "))
                update_record(Property, property_id, 'id', price=new_price)
                print("Ціна оновлена успішно.")

            elif choice == 4:
                property_id = int(input("Введіть ID об'єкта для редагування адреси: "))
                new_address = input("Введіть нову адресу: ")
                update_record(Property, property_id, 'id', address=new_address)
                print("Адреса оновлена успішно.")

            elif choice == 5:
                property_id = int(input("Введіть ID об'єкта для видалення: "))
                delete_record(Property, property_id)
                print("Об'єкт видалено успішно.")

            elif choice == 6:
                print("Повернення до головного меню.")
                break

            else:
                print("Неправильний вибір. Спробуйте ще раз.")

        except ValueError:
            print("Будь ласка, введіть правильне значення.")
def manage_lease_contracts():
    while True:
        print_ascii_title()
        print("================================")
        print("\nУправління орендними договорами:")
        print("1) Переглянути всі орендні договори")
        print("2) Додати новий орендний договір")
        print("3) Оновити інформацію про орендний договір")
        print("4) Видалити орендний договір")
        print("5) Повернутися до головного меню")

        try:
            choice = int(input("Виберіть дію (1-5): "))

            if choice == 1:
                contracts = session.query(LeaseContract).all()
                for contract in contracts:
                    print(f"Код Контракту: {contract.contract_id}, "
                          f"Початок оренди: {contract.start_date}, "
                          f"Кінець оренди: {contract.end_date}, "
                          f"Код нерухомості: {contract.property_id}, "
                          f"Код Орендодавця: {contract.owner_id}, "
                          f"Код Орендаря: {contract.tenant_id}")

            elif choice == 2:
                start_date = input("Введіть дату початку оренди (YYYY-MM-DD): ")
                end_date = input("Введіть дату кінця оренди (YYYY-MM-DD): ")
                property_id = int(input("Введіть ID нерухомості: "))
                owner_id = int(input("Введіть ID орендодавця: "))
                tenant_id = int(input("Введіть ID орендаря: "))
                paid_month = input("Введіть Кількість Оплачених Місяців: ")
                add_lease_contract(start_date=start_date, end_date=end_date, property_id=property_id, owner_id=owner_id,
                                   tenant_id=tenant_id, paid_month=paid_month)

                print("Орендний договір додано успішно.")

            elif choice == 3:
                contract_id = int(input("Введіть ID орендного договору для оновлення: "))
                contract = session.query(LeaseContract).get(contract_id)
                if contract:
                    new_start_date = input("Введіть нову дату початку оренди (YYYY-MM-DD): ")
                    new_end_date = input("Введіть нову дату кінця оренди (YYYY-MM-DD): ")
                    update_lease_contract(contract_id=contract_id, new_start_date=new_start_date, new_end_date=new_end_date)
                    print("Інформацію про орендний договір оновлено успішно.")
                else:
                    print("Орендний договір не знайдено.")

            elif choice == 4:
                contract_id = int(input("Введіть ID орендного договору для видалення: "))
                contract = session.query(LeaseContract).get(contract_id)
                if contract:
                    delete_lease_contract(contract_id)
                    print("Орендний договір видалено успішно.")
                else:
                    print("Орендний договір не знайдено.")

            elif choice == 5:
                print("Повернення до головного меню.")
                break

            else:
                print("Неправильний вибір. Спробуйте ще раз.")

        except ValueError:
            print("Будь ласка, введіть правильне значення.")
def data_manipulation_menu():
    while True:
        print("\nКерування таблицями:")
        print("1) Управління орендарями")
        print("2) Управління орендодавцями")
        print("3) Управління об'єктами нерухомості")
        print("0) Повернутися до головного меню")

        choice = input("Оберіть пункт меню: ")

        if choice == '1':
            manage_records('Орендарі', Tenant)
        elif choice == '2':
            manage_records('Орендодавці', Owner)
        elif choice == '3':
            manage_records('Об\'єкти нерухомості', Property)
        elif choice == '0':
            print("Повернення до головного меню.")
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")


def manage_records(entity_name, entity_class):
    id_field_mapping = {
        'Орендарі': 'tenant_id',
        'Орендодавці': 'owner_id',
        'Об\'єкти нерухомості': 'property_id',
    }

    id_field = id_field_mapping[entity_name]

    while True:
        print(f"\nМеню управління {entity_name.lower()}:")
        print("1) Додати запис")
        print("2) Оновити запис")
        print("3) Видалити запис")
        print("4) Переглянути всі записи")
        print("0) Повернутися до попереднього меню")

        choice = input("Оберіть пункт меню: ")

        if choice == '1':
            name = input(f"Введіть ім'я {entity_name.lower()}а: ")
            new_entity = {'name': name}
            create_record(entity_class, **new_entity)
        elif choice == '2':
            entity_id = int(input(f"Введіть ID {entity_name.lower()}а для оновлення: "))
            name = input(f"Введіть нове ім'я {entity_name.lower()}а: ")
            update_record(entity_class, entity_id, id_field, name=name)
        elif choice == '3':
            entity_id = int(input(f"Введіть ID {entity_name.lower()}а для видалення: "))
            delete_record(entity_class, entity_id)
        elif choice == '4':
            print_records(entity_class)
        elif choice == '0':
            break
        else:
            print("Невірний вибір, спробуйте ще раз.")
def print_ascii_title():
    print(r"""
 _____  ______ __  __  _____ 
|  __ \|  ____|  \/  |/ ____|
| |__) | |__  | \  / | (___  
|  _  /|  __| | |\/| |\___ \ 
| | \ \| |____| |  | |____) |
|_|  \_\______|_|  |_|_____/  
    """)


def main_menu():
    print_ascii_title()
    while True:
        print("\n== Головне меню ==")
        print("1) Облік об'єктів нерухомості")
        print("2) Управління орендними договорами")
        print("3) Керування таблицями")
        print("4) Генерація звіту")
        print("5) Оновлення таблиці звітність")
        print("6) Вихід")

        try:
            choice = int(input("Виберіть пункт меню (1-5): "))

            if choice == 1:
                manage_properties()
            elif choice == 2:
                print("Ви обрали управління орендними договорами.")
                manage_lease_contracts()
            elif choice == 3:
                print("Ви обрали Керування таблицями.")
                data_manipulation_menu()
            elif choice == 4:
                print("Ви обрали управління Генерацію звіту.")
                prop_id = int(input("Виберіть Код нерухомості..."))
                print("Генерація звіту...")
                generate_word_report(prop_id)
            elif choice == 5:
                print("Ви обрали Оновлення таблиці звітність.")
                update_reporting()
                print_records(Reporting)
            elif choice == 6:
                print("Вихід з програми. До побачення!")
                break
            else:
                print("Неправильний вибір. Спробуйте ще раз.")
        except ValueError:
            print("Будь ласка, введіть число від 1 до 5.")


main_menu()
