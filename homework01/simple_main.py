import os
import sys
import json


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def adrb_files_in_catalog(directory):
    adrb_files = []
    for file in os.listdir(directory):
        if file.endswith(".adrb"):
            adrb_files.append(file)
    return adrb_files


def render_menu(*args):
    global opened_address_book
    global deleted_contact
    global address_book_changed
    print('-'*40)
    if opened_address_book:
        print(f'Открыта адресная книга {opened_address_book}')
    else: 
        print(f'Нет открытых адресных книг')
    print('-'*40)
    if deleted_contact:
        print(deleted_contact)
        print('-'*40)
        deleted_contact = False
    if address_book_changed:
        print(f'Адресная книга была изменена!\nНе забудьте сохранить изменения перед выходом!')
        print('-'*40)
        deleted_contact = False
    keys=[]
    for menu_item in main_menu:
        keys.append(menu_item['key'])
        key = menu_item['key']
        title = menu_item['title']
        print(f'{key}) {title}\n')
    return keys


def open_address_book(*args):
    global opened_address_book
    global ADBOOKS_CATALOG
    current_address_book_ = []
    allowed_adrb_files = adrb_files_in_catalog(ADBOOKS_CATALOG)
    print('Список адресных книг:')
    for file in allowed_adrb_files: print(file)
    ab_filename = input('Введите название файла адресной книги: ')
    if ab_filename in allowed_adrb_files:
        ab_path = f'{ADBOOKS_CATALOG}{ab_filename}'
        with open(ab_path, 'r', encoding='UTF-8') as ab:
            current_address_book_ = json.load(ab)
        opened_address_book = ab_filename
        return current_address_book_
    else:
        print('Адресной книги с таким именем не существует!')


def list_contact_id():
    global current_address_book
    list_id = []
    for contact in current_address_book:
        list_id.append(contact['id'])
    return list_id


def show_contacts(*args):
    global current_address_book
    clear_console()
    for contact in current_address_book:
        print(f"ID:\t\t{contact['id']}")
        print(f"ФИО:\t\t{contact['name']}")
        print(f"Адрес:\t\t{contact['address']}")
        print(f"E-mail:\t\t{contact['email']}")
        print(f"Тел.:\t\t{contact['phone_number']}")
        print(f"Дата рождения:\t{contact['birth_date']}")
        print(f"Работа:\t\t{contact['company']}")
        print(f"Специальность:\t{contact['job']}")
        print('-'*40)
    input('Нажмите ENTER для возврата в меню.')
    return


def find_contact(*args):
    global current_address_book
    symbols_to_remove = ['+','-','(',')',' ']
    to_filter_address_book = input('Введите строку для поиска контактов: ')
    for contact in current_address_book:
        for symbol in symbols_to_remove:
            contact['phone_number'] = contact['phone_number'].replace(symbol, '')
        # print(str(contact).find(to_filter_address_book))
        is_finded = (str(contact)).lower().find(to_filter_address_book.lower())
        if is_finded != -1:
            print(f"ID:\t\t{contact['id']}")
            print(f"ФИО:\t\t{contact['name']}")
            print(f"Адрес:\t\t{contact['address']}")
            print(f"E-mail:\t\t{contact['email']}")
            print(f"Тел.:\t\t{contact['phone_number']}")
            print(f"Дата рождения:\t{contact['birth_date']}")
            print(f"Работа:\t\t{contact['company']}")
            print(f"Специальность:\t{contact['job']}")
            print('-'*40)
        else:
            continue
    input('Нажмите ENTER для возврата в меню.')
    return


def add_contact(*args):
    global current_address_book
    global contact_template
    global address_book_changed
    contact_to_add = {}
    contact_to_add['id'] = max(list_contact_id()) + 1
    print('Введите данные контакта:')
    for key,value in contact_template.items():
        if key == 'id':
            continue
        new_value = input(f'Введите {value}: ')
        contact_to_add[key] = new_value
    print(contact_to_add)
    if input('Данные корректны? (ДА - Y / Нет - N): ').lower() == 'y':
        current_address_book.append(contact_to_add)
        address_book_changed = True
    return 'Контакт добавлен.'


def edit_contact(*args):
    global address_book_changed
    global contact_template
    while True:
        id_to_edit = input('Введите ID контакта для изменения: ')
        if int(id_to_edit) in list_contact_id():
            for contact in current_address_book:
                if contact['id']  == int(id_to_edit):
                    contact['name'] = input(f"Изменить текущее значение ФИО ({contact['name']}): ")
                    contact['address'] = input(f"Изменить текущее значение Адрес ({contact['address']}): ")
                    contact['email'] = input(f"Изменить текущее значение E-mail ({contact['email']}): ")
                    contact['phone_number'] = input(f"Изменить текущее значение Тел ({contact['phone_number']}): ")
                    contact['birth_date'] = input(f"Изменить текущее значение Дата рождения ({contact['birth_date']}): ")
                    contact['company'] = input(f"Изменить текущее значение Работа ({contact['company']}): ")
                    contact['job']  = input(f"Изменить текущее значение Специальность ({contact['job']}): ")
                    address_book_changed = True
                    return 'Контакт успешно изменён!'
                else:
                    continue
        input('Контакт с таким ID не найден.\nНажите ENTER для возврата в основное меню.')
        return 'Контакт с таким ID не найден.'


def delete_contact(*args):
    global address_book_changed
    id_to_delete = input('Введите ID контакта для удаления: ')
    if int(id_to_delete) in list_contact_id():
        k = 0
        for contact in current_address_book:
            if contact['id'] == int(id_to_delete):
                current_address_book.pop(k)
                deleted_contact_ = contact
                address_book_changed = True
                return 'Контакт успешно удалён!'
            else:
                k+=1
                continue
    input('Контакт с таким ID не найден.\nНажите ENTER для возврата в основное меню.')
    return 'Контакт с таким ID не найден.'


def save_address_book(*args):
    global current_address_book
    global opened_address_book
    global address_book_changed
    ab_path = f'{ADBOOKS_CATALOG}{opened_address_book}'
    with open(ab_path, 'w', encoding='UTF-8') as ab:
        json.dump(current_address_book, ab, indent=4, ensure_ascii=False)
        address_book_changed = False
    return 'Адресная книга успешно сохранена!'


def exit_from_program(*args):
    global address_book_changed
    if address_book_changed :
        while True:
            save_book = input('Сохранить изменения в адресной книге? (ДА - Y / Нет - N): ')
            if save_book.lower() == 'y':
                save_address_book()
                sys.exit(0)
            elif save_book.lower() == 'n':
                sys.exit(0)
            else:
                print('Не корректный символ!')
                continue
    sys.exit(0)


ADBOOKS_CATALOG = './adbooks/'
ADBOOKS_FORMAT = '.adrb'
current_address_book = ''
opened_address_book = ''
finded_contacts = ''
added_contact = ''
deleted_contact = ''
saved_address_book = ''
address_book_changed = False

main_menu = [
    # {'id': '10', 'masterId': '0', 'key': '1', 'title': 'Создать адресную книгу', 'handler': create_address_book},
    {'id': '10', 'masterId': '0', 'key': '1', 'title': 'Открыть адресную книгу', 'handler': open_address_book, 'returned_object' : 'current_address_book'},
    {'id': '20', 'masterId': '0', 'key': '2', 'title': 'Показать все контакты', 'handler': show_contacts, 'returned_object' : 'showed_contacts'},
    {'id': '30', 'masterId': '0', 'key': '3', 'title': 'Поиск контакта', 'handler': find_contact,  'returned_object' : 'finded_contacts'},
    {'id': '40', 'masterId': '0', 'key': '4', 'title': 'Добавить контакт', 'handler': add_contact, 'returned_object' : 'added_contact'},
    {'id': '50', 'masterId': '0', 'key': '5', 'title': 'Изменить контакт', 'handler': edit_contact,  'returned_object' : 'edited_contact'},
    {'id': '60', 'masterId': '0', 'key': '6', 'title': 'Удалить контакт', 'handler': delete_contact,  'returned_object' : 'deleted_contact'},
    {'id': '70', 'masterId': '0', 'key': '7', 'title': 'Сохранить измеения в адресной книге', 'handler': save_address_book, 'returned_object' : 'saved_address_book'},
    {'id': '90', 'masterId': '0', 'key': '0', 'title': 'Выход', 'handler': exit_from_program}
]
contact_template = {
    'id' : 'ID',
    'name' : 'ФИО',
    'address' : "Адрес",
    'email' : "E-mail",
    'phone_number': "Тел",
    'birth_date' : "Дата рождения",
    'company' : "Работа",
    'job' : "Специальность"
}


while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    allowed_keys = render_menu()
    arguments = []
    your_choise = input('Выберите пункт меню: ')
    if your_choise in allowed_keys:
        locals()[main_menu[allowed_keys.index(your_choise)]['returned_object']] = main_menu[allowed_keys.index(your_choise)]['handler'](arguments)
    else:
        print('Нет такого пункта меню!')
        input()
        continue