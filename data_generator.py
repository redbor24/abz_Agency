from pathlib import Path
from random import shuffle
from pprint import pprint

"""
Числа означают количество узлов на каждом уровне иерархии, кроме последнего,
и, соответственно, количество самих уровней в иерархии.
Для последнего уровня количество не задаётся
"""
STRUCT_DESCRIPTOR = [2, 3, 5, 10]
ALL_PERSON_COUNT = 5000
LAST_LEVEL_ELEM_COUNT = 4
# LAST_LEVEL_ELEM_COUNT = 150
DATA_FILES_SUBPATH = 'data/'


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
                        raise Exception
    except:
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
                        raise Exception
    except:
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


def fill_struct():
    persons = generate_persons(ALL_PERSON_COUNT)
    root = {
            'id': 0,
            'first_name': 'root',
            'middle_name': None,
            'second_name': None,
            # 'child_count': 1,
            'childs': fill_element(0, persons)
        }
    return root


def fill_element(level, persons):
    if level > len(STRUCT_DESCRIPTOR) - 1:
        element_persons = get_persons(persons, LAST_LEVEL_ELEM_COUNT)
        return element_persons

    element_persons = get_persons(persons, STRUCT_DESCRIPTOR[level])
    for person in element_persons:
        person['childs'] = fill_element(level + 1, persons)

    return element_persons


def render_struct():
    staff = fill_struct()
    pprint(staff)
    rendered_struct = ''
    if staff:
        for element in staff['childs']:
        # return f"<ul>{render_element(staff['childs'][0])}</ul>"
            rendered_struct += render_element(element)

    return rendered_struct


def render_element(element):
    rendered_element = f'<li>{element["second_name"]}' \
                        f' {element["first_name"]}' \
                        f' {element["middle_name"]}'

    if element['childs']:
        rendered_element += '<ul>'
        for elem in element['childs']:
            rendered_element += render_element(elem)
        rendered_element += '</ul>'

    rendered_element += '</li>'

    return rendered_element


if __name__ == '__main__':
    # staff_struct = fill_struct()
    # pprint(staff_struct)
    print(render_struct())
