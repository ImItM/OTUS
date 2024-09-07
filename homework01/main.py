import os
import sys
import json


def clear_console():
    '''Очистка консоли перед отрисовкой'''
    os.system('cls' if os.name == 'nt' else 'clear')


def adrb_files_in_catalog(directory: str):
    '''Функция возвращает список фалов с расширением adrb в каталоге'''
    adrb_files = []
    for file in os.listdir(directory):
        if file.endswith(".adrb"):
            adrb_files.append(file)
    return adrb_files


def render_top_info_block(opened_address_book_f: str, address_book_changed_f: bool):
    '''Вывод информационного блока над меню'''
    print('-'*40)
    if opened_address_book_f:
        print(f'Открыта адресная книга {opened_address_book}')
    else: 
        print(f'Нет открытых адресных книг')
    print('-'*40)
    if address_book_changed_f:
        print(f'\033[34mАдресная книга была изменена!\nНе забудьте сохранить изменения перед выходом!\033[0m')
        print('-'*40)


def render_menu():
    '''Функция для отрисовки главного меню'''
    keys=[]
    for menu_item in MAIN_MENU:
        keys.append(menu_item['key'])
        key = menu_item['key']
        title = menu_item['title']
        print(f'{key}) {title}\n')
    return keys


def render_contact_view(contact_template_f: dict, contacts_to_render_f: list, static_text_f: str, get_data: bool):
    '''Функция работает в двух режимах, в зависимости от параметра get_data. 
    Если get_data = True то вывод списка контактов, переданных в contacts_to_render_f
    Если get_data = False то редактирование контакта, переданного  в contacts_to_render_f'''
    for contact in contacts_to_render_f:
        if get_data:
            for key in contact_template_f.keys():
                print(f'{static_text_f}{contact_template_f[key]}:\t\t{contact[key]}')
        else:
            for key in contact_template_f.keys():
                if key == 'id':
                    continue
                else:
                    contact[key] = input(f'{static_text_f}{contact_template_f[key]}({contact[key]}): ')
            return contact
        print('-'*40)


def open_address_book():
    '''Функция вывода списка адресных книг и открытие выбранной.'''
    current_address_book_f = []
    opened_address_book_f = []
    allowed_adrb_files = adrb_files_in_catalog(ADBOOKS_CATALOG)
    print('Список адресных книг:')
    for file in allowed_adrb_files: print(file)
    ab_filename = input('Введите название файла адресной книги: ')
    if ab_filename in allowed_adrb_files:
        ab_path = f'{ADBOOKS_CATALOG}{ab_filename}'
        with open(ab_path, 'r', encoding='UTF-8') as ab:
            current_address_book_f = json.load(ab)
        opened_address_book_f = ab_filename
    else:
        input('Адресной книги с таким именем не существует!\nНажмите ENTER для возврата в меню.')
    return current_address_book_f, opened_address_book_f

def list_contact_id(current_address_book_for_find_id):
    '''Функция возвращает список id контактов в адресной книге'''
    list_id = [0]
    for contact in current_address_book_for_find_id:
        list_id.append(contact['id'])
    return list_id


def show_contacts(current_address_book_f: list):
    '''Функция выводит все контакты открытой адресной книги'''
    clear_console()
    render_contact_view(CONTACT_TEMPLATE, current_address_book_f, '', True)
    input('Нажмите ENTER для возврата в меню.')


def find_contact(current_address_book_f: list):
    '''Функция поиска контактов в адресной книге.
    Поиск производится по всем полям контакта.'''
    finded_contacts_f = []
    symbols_to_remove = ['+','-','(',')',' ']
    to_filter_address_book = input('Введите строку для поиска контактов: ')
    for contact in current_address_book_f:
        for symbol in symbols_to_remove:
            contact['phone_number'] = contact['phone_number'].replace(symbol, '')
        is_finded = (str(contact)).lower().find(to_filter_address_book.lower())
        if is_finded != -1:
            finded_contacts_f.append(contact)
        else:
            continue
    if finded_contacts_f:
        render_contact_view(CONTACT_TEMPLATE, finded_contacts_f, '', True)
    else:
        print ('Контакты, удовлетворяющие условиям поиска не найдены.')
    input('Нажмите ENTER для возврата в меню.')
    return


def add_contact(current_address_book_f: list):
    '''Функция добавления контакта в адресную книгу'''
    contact_to_add = {}
    contact_to_add['id'] = max(list_contact_id(current_address_book_f)) + 1
    print('Введите данные контакта:')
    for key,value in CONTACT_TEMPLATE.items():
        if key == 'id':
            continue
        new_value = input(f'Введите {value}: ')
        contact_to_add[key] = new_value
    print(contact_to_add)
    if input('Данные корректны? (ДА - Y / Нет - любая другая клавиша): ').lower() == 'y':
        current_address_book_f.append(contact_to_add)
        address_book_changed_f = True
    return current_address_book_f, address_book_changed_f


def edit_contact(current_address_book_f: list, address_book_changed_f: bool):
    '''Функция редактирования контактов в адресной книге'''
    current_contact_for_change = []
    k = 0
    id_to_edit = input('Введите ID контакта для изменения: ')
    if id_to_edit.isdigit() and int(id_to_edit) in list_contact_id(current_address_book_f):
        for k in range (0, len(current_address_book_f)):
            if current_address_book_f[k]['id'] == int(id_to_edit):
                current_contact_for_change.append(current_address_book_f[k])
                changed_contact = render_contact_view(CONTACT_TEMPLATE, current_contact_for_change, 'Изменить текущее значение ', False)
                current_address_book_f[k] = dict(changed_contact)
                address_book_changed_f = True
                input('Контакт был успешно изменён.\nНажите ENTER для возврата в основное меню.')
                return current_address_book_f, address_book_changed_f
            else:
                continue
    input('Контакт с таким ID не найден.\nНажите ENTER для возврата в основное меню.')
    return current_address_book_f, address_book_changed_f


def delete_contact(current_address_book_f: list, address_book_changed_f: str):
    '''Функция удаления контактов в адресной книге'''
    id_to_delete = input('Введите ID контакта для удаления: ')
    if id_to_delete.isdigit() and int(id_to_delete) in list_contact_id(current_address_book_f):
        k = 0
        for contact in current_address_book_f:
            if contact['id'] == int(id_to_delete):
                current_address_book_f.pop(k)
                address_book_changed_f = True
                input('Контакт удалён.\nНажмите ENTER для возврата в основное меню.')
                return current_address_book_f, address_book_changed_f
            else:
                k+=1
                continue
    input('Контакт с таким ID не найден.\nНажите ENTER для возврата в основное меню.')
    return current_address_book_f, address_book_changed_f
    

def save_address_book(current_address_book_for_save: str, opened_address_book_for_save: str, address_book_changed_after_save: bool):
    '''Функция сохранения адресной книги на диск.'''
    ab_path = f'{ADBOOKS_CATALOG}{opened_address_book_for_save}'
    with open(ab_path, 'w', encoding='UTF-8') as ab:
        json.dump(current_address_book_for_save, ab, indent=4, ensure_ascii=False)
        address_book_changed_after_save = False
    return address_book_changed_after_save


def exit_from_program(current_address_book_f: list, opened_address_book_f: str, address_book_changed_f: bool):
    '''Функция выхода из программы. Перед выходом происходит проверка была ли изменена адресная книга после открытия'''
    if address_book_changed_f :
        save_book = input('Сохранить изменения в адресной книге? (ДА - Y / Нет - любая другая клавиша): ')
        if save_book.lower() == 'y':
            save_address_book(current_address_book_f, opened_address_book_f, address_book_changed_f)
            input('Адресная книга сохранена. Нажмите ENTER для выхода.')
            sys.exit(0)
        else:
            input('Выход без сохранения изменений. Нажмите ENTER для выходаю.')
            sys.exit(0)
    sys.exit(0)


ADBOOKS_CATALOG = './adbooks/'
ADBOOKS_FORMAT = '.adrb'
current_address_book = ''
opened_address_book = ''
address_book_changed = False


MAIN_MENU = [
    {'id': '10', 'masterId': '0', 'key': '1', 'title': 'Открыть адресную книгу'},
    {'id': '20', 'masterId': '0', 'key': '2', 'title': 'Показать все контакты'},
    {'id': '30', 'masterId': '0', 'key': '3', 'title': 'Поиск контакта'},
    {'id': '40', 'masterId': '0', 'key': '4', 'title': 'Добавить контакт'},
    {'id': '50', 'masterId': '0', 'key': '5', 'title': 'Изменить контакт'},
    {'id': '60', 'masterId': '0', 'key': '6', 'title': 'Удалить контакт'},
    {'id': '70', 'masterId': '0', 'key': '7', 'title': 'Сохранить измеения в адресной книге'},
    {'id': '90', 'masterId': '0', 'key': '0', 'title': 'Выход'}
]


CONTACT_TEMPLATE = {
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
    render_top_info_block(opened_address_book, address_book_changed)
    allowed_keys = render_menu()
    # arguments = []
    your_choise = input('Выберите пункт меню: ')
    if your_choise in allowed_keys:
        if your_choise == '1':
            current_address_book, opened_address_book = open_address_book()
        elif your_choise == '2':
            show_contacts(current_address_book)
        elif your_choise == '3':
            find_contact(current_address_book)
        elif your_choise == '4':
            current_address_book,address_book_changed = add_contact(current_address_book)
        elif your_choise == '5':
            current_address_book, address_book_changed = edit_contact(current_address_book, address_book_changed)
        elif your_choise == '6':
            current_address_book, address_book_changed = delete_contact(current_address_book, address_book_changed)
        elif your_choise == '7':
           address_book_changed = save_address_book(current_address_book, opened_address_book, address_book_changed)
        elif your_choise == '0':
            exit_from_program(current_address_book, opened_address_book, address_book_changed)
    else:
        input('Нет такого пункта меню!\nНажмите ENTER для возврата в меню.')
        continue