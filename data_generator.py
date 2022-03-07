from pathlib import Path
from random import shuffle
from pprint import pprint

from dateutil.rrule import rrule, DAILY
import datetime
import random

"""
STRUCT_DESCRIPTOR
Содержит количество ставок на каждом уровне и наименование должности на нём.
Числа означают количество узлов на каждом уровне иерархии, кроме последнего,
и, соответственно, количество самих уровней в иерархии.
Для последнего уровня количество ставок задаётся отдельной константой 
LAST_LEVEL_ELEM_COUNT.
"""
STRUCT_DESCRIPTOR = [
    {'quantity': 2, 'position': 'генеральный директор'},
    {'quantity': 3, 'position': 'руководитель департамента'},
    {'quantity': 5, 'position': 'начальник отдела'},
    {'quantity': 10, 'position': 'ведущий специалист'},
]

# Наименование должности на низшем уровне иерархии
ORDINARY_EMPLOYEE = 'инженер'

LAST_LEVEL_ELEM_COUNT = 150

DATA_FILES_SUBPATH = 'data/'


class LocalException(Exception):
    pass


def get_random_date(year_from, year_to):
    return random.choice(
        list(
            rrule(DAILY,
                  dtstart=datetime.date(year_from, 1, 1),
                  until=datetime.date(year_to, 1, 1))
        )
    )


def read_file(filename):
    with open(Path(DATA_FILES_SUBPATH) / filename, "r", encoding="UTF-8") as f:
        values = f.readlines()
    return [value[:-1].replace('\t', '').strip() for value in values]


def generate_persons(count):
    first_man_names = read_file('imena_m_ru.txt')
    middle_man_names = read_file('otch_m_ru.txt')
    second_man_names = read_file('family_m_ru.txt')
    first_woman_names = read_file('imena_f_ru.txt')
    middle_woman_names = read_file('otch_f_ru.txt')
    second_woman_names = read_file('family_f_ru.txt')

    persons = []
    person_id = 0
    try:
        for first_name in first_man_names:
            for middle_name in middle_man_names:
                for second_name in second_man_names:
                    person = {
                        'id': person_id,
                        'first_name': first_name,
                        'middle_name': middle_name,
                        'second_name': second_name
                    }
                    persons.append(person)
                    person_id += 1
                    if person_id == count // 2:
                        raise LocalException
    except LocalException:
        pass

    woman_count = count - person_id
    try:
        for first_name in first_woman_names:
            for middle_name in middle_woman_names:
                for second_name in second_woman_names:
                    person = {
                        'id': person_id,
                        'first_name': first_name,
                        'middle_name': middle_name,
                        'second_name': second_name
                    }
                    persons.append(person)
                    person_id += 1
                    woman_count -= 1
                    if woman_count == 0:
                        raise LocalException
    except LocalException:
        pass

    shuffle(persons)
    return persons


def get_persons(persons, count):
    ret_persons = []
    for person in range(0, count):
        if persons:
            tmp_person = persons.pop()
            tmp_person['childs'] = []
            ret_persons.append(tmp_person)
    return ret_persons


def fill_struct(person_count):
    persons = generate_persons(person_count)
    root = {
            'id': 0,
            'first_name': 'root',
            'middle_name': None,
            'second_name': None,
            'childs': fill_element(0, persons)
        }
    return root


def fill_element(level, persons):
    if level > len(STRUCT_DESCRIPTOR) - 1:
        element_persons = get_persons(persons, LAST_LEVEL_ELEM_COUNT)
        for element in element_persons:
            element['position'] = ORDINARY_EMPLOYEE
            element['employment_date'] = get_random_date(2010, 2022)
        return element_persons

    element_persons = get_persons(persons, STRUCT_DESCRIPTOR[level]['quantity'])
    for element in element_persons:
        element['position'] = STRUCT_DESCRIPTOR[level]['position']
        element['employment_date'] = get_random_date(2010, 2022)

    for person in element_persons:
        person['childs'] = fill_element(level + 1, persons)

    return element_persons


def render_struct(person_count):
    staff = fill_struct(person_count)
    rendered_struct = ''
    if staff:
        for element in staff['childs']:
            rendered_struct += render_element(element)

    return rendered_struct


def render_element(element):
    rendered_element = f'<li>{element["second_name"]}' \
                       f' {element["first_name"]}' \
                       f' {element["middle_name"]}' \
                       f', {element["position"]}' \
                       f', {element["employment_date"].strftime("%d.%m.%Y")}'

    if element['childs']:
        rendered_element += '<ul>'
        for elem in element['childs']:
            rendered_element += render_element(elem)
        rendered_element += '</ul>'

    rendered_element += '</li>'

    return rendered_element


if __name__ == '__main__':
    print(render_struct())
