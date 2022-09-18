import re
import logging
from typing import Match, Pattern, TypedDict


logging.basicConfig(format='[%(asctime)s] %(levelname)s %(message)s', level=logging.DEBUG)


def convert_hour_to_seconds(hour: str) -> str:
    '''Receive an hour in HH format 
    and transforms it in seconds.
    The seconds count from 00 to 23'''
    hours: int = int(hour)

    MINUTES_IN_HOUR: int = 60
    SECONDS_IN_MINUTE: int = 60
    SECONDS_IN_HOUR: int = MINUTES_IN_HOUR * SECONDS_IN_MINUTE
    return str(hours * SECONDS_IN_HOUR)

def parse_timetable_from_timetables(timetables: str) -> list[str]:
    '''Receive a string with several timetables and return
    a list with all of them in the string'''
    re_timetable: Pattern = re.compile(r'(\d{2} a \d{2})')
    return re_timetable.findall(timetables)

def get_start_and_end_time_from_timetable(timetable: str) -> dict[str, str] :
    '''Receive a timetable (only one) and get the start and the final hour of it'''
    re_timetable: Pattern = re.compile(r'(\d{2}) a (\d{2})')
    start_hour: str
    end_hour: str
    hours_found: Match | None = re_timetable .search(timetable) 
    
    if hours_found:
        start_hour, end_hour = (
                hours_found.groups()
        )

        time_dict: dict[str, str] = {
            'start_time': start_hour,
            'end_time': end_hour,
            'str_timetable': timetable

        }
        return time_dict
    else:
        raise Exception('the argument is not a timetable')

def parse_days(days: str) -> list[str]:
    '''Receive a string with several days and return a list with 
    all of them'''
    re_days: Pattern = re.compile(r'(\w{2})')

    days_found = re_days.findall(days)
    return days_found

def timetable_to_timetable_dict(days: str, timetable: str) -> dict:
    '''Receive a string with days and a string with timetables.
    Return a dict with the start and end time and the same but
    converted to seconds (useful for time comparisons)'''
    timetables_list: list[str] = parse_timetable_from_timetables(timetable)
    days_list: list[str] = parse_days(days)

    assert len(days_list) >= len(timetables_list), 'CANT BE MORE TIMETABLES THAN DAYS'

    COURSE_TIMETABLES_KEY: str = 'course_timetables'
    COURSE_START_TIME_KEY: str = 'start_time'
    COURSE_END_TIME_KEY: str = 'end_time'
    COURSE_START_TIME_IN_SECS_KEY: str = 'start_time_in_secs'
    COURSE_END_TIME_IN_SECS_KEY: str = 'end_time_in_secs'
    STR_TIMETABLE_KEY: str = 'str_timetable'

    timetable_dict: dict = {}
    if COURSE_TIMETABLES_KEY not in  timetable_dict:
        timetable_dict.update({
            COURSE_TIMETABLES_KEY: {}
        })
    for i, day in enumerate( days_list ):
        try:
            current_day_timetable = timetables_list[i]
        except IndexError:
            current_day_timetable = timetables_list[-1]


        start_end_dict: dict = get_start_and_end_time_from_timetable(current_day_timetable)
        start_time: str | None = start_end_dict.get(COURSE_START_TIME_KEY)
        end_time: str | None = start_end_dict.get(COURSE_END_TIME_KEY)
        str_timetable: str | None = start_end_dict.get(STR_TIMETABLE_KEY)
        new_start_end_dict: dict = {}

        if start_time and end_time and str_timetable:
            start_time_in_seconds: str = convert_hour_to_seconds(start_time) 
            end_time_in_seconds: str = convert_hour_to_seconds(end_time )

            new_start_end_dict.update({
                COURSE_START_TIME_IN_SECS_KEY: start_time_in_seconds,
                COURSE_END_TIME_IN_SECS_KEY: end_time_in_seconds,
                STR_TIMETABLE_KEY: str_timetable
                
            })

        timetable_dict[COURSE_TIMETABLES_KEY].update(
            {
                day: new_start_end_dict
            }
        )

    return timetable_dict


    
def compare_timetable_interference(first_timetable: str | dict, second_timetable: str | dict) -> bool:
    '''Return if second timetable interfere with first_timetable'''
    
    if isinstance(first_timetable, str) and isinstance(second_timetable, str):
        first_timetable_dict: dict = get_start_and_end_time_from_timetable(first_timetable)
        second_timetable_dict: dict = get_start_and_end_time_from_timetable(second_timetable)
    elif isinstance(first_timetable, dict) and isinstance(second_timetable, dict):
        first_timetable_dict: dict = first_timetable
        second_timetable_dict: dict = second_timetable
    else:
        raise Exception('arguments must be both dicts or str')

    COURSE_START_TIME_KEY: str = 'start_time'
    COURSE_END_TIME_KEY: str = 'end_time'

    first_timetable_start_secs: str = convert_hour_to_seconds(first_timetable_dict[COURSE_START_TIME_KEY])
    first_timetable_end_secs: str = convert_hour_to_seconds(first_timetable_dict[COURSE_END_TIME_KEY])
    second_timetable_start_secs: str = convert_hour_to_seconds(second_timetable_dict[COURSE_START_TIME_KEY])
    second_timetable_end_secs: str = convert_hour_to_seconds(second_timetable_dict[COURSE_END_TIME_KEY])

    start_time_between_course: bool = first_timetable_start_secs > second_timetable_start_secs and\
        first_timetable_start_secs < second_timetable_end_secs

    end_time_between_course: bool = first_timetable_end_secs > second_timetable_start_secs and\
        first_timetable_end_secs < second_timetable_end_secs

    start_time_between_course2: bool = second_timetable_start_secs > first_timetable_start_secs and\
        second_timetable_start_secs < first_timetable_end_secs

    end_time_between_course2: bool = second_timetable_end_secs > first_timetable_start_secs and\
        second_timetable_end_secs < first_timetable_end_secs

    start_time_is_interfering: bool = second_timetable_start_secs == first_timetable_start_secs or\
        start_time_between_course or start_time_between_course2

    end_time_is_interfering: bool =  second_timetable_end_secs ==  first_timetable_end_secs or \
        end_time_between_course or end_time_between_course2

    if start_time_is_interfering or end_time_is_interfering:
        return True
    return False



def make_courses_timetables(courses_timetables: list[dict[str, str]],
    prefered_days: list[str] = [],
    black_list_days: list[str] = [],
    prefered_courses: list[str] = [],
    black_list_courses: list[str] = [],
    prefered_teachers: list[str] = [],
    black_list_teachers: list[str] = [],
    prefered_interval_of_course: str = '',
    black_interval_of_course: str = ''
) -> list[list]:
    '''receive a list with several dicts of courses and create 
    timetable combining them'''

    TIMETABLES_KEY: str = 'course_timetables'
    TEACHER_KEY: str = 'teacher'
    NAME_KEY: str = 'course_name'
    STR_TIMETABLE_KEY: str = 'str_timetable'
    GENERAL_PUNCTUATION_KEY: str = 'general_punctuation'
    DAYS_PUNCTUATION_KEY: str = 'days_punctuation'
    COURSE_PUNCTUATION_KEY: str = 'course_punctuation'
    TIMETABLE_PUNCTUATION_KEY: str = 'timetable_punctuation'
    TEACHER_PUNCTUATION_KEY: str = 'teacher_punctuation'
    COMMON_DAY_PUNCTUATION_KEY: str = 'common_day_punctuation'
    

    courses_dicts_list: dict = {}

    if prefered_interval_of_course:
        prefered_interval_dict: dict[str, str] = get_start_and_end_time_from_timetable(prefered_interval_of_course)
    else:
        prefered_interval_dict: dict[str, str ] = {}

    if black_interval_of_course:
        black_interval_dict: dict[str, str] = get_start_and_end_time_from_timetable(black_interval_of_course)
    else:
        black_interval_dict: dict[str, str ] = {}

    

    # this groups courses with the same name in [courses_dicts_list]
    for course in courses_timetables:
        current_course_name: str | None = course.get(NAME_KEY)
        course_timetable: dict | None = course.get(TIMETABLES_KEY)
        if current_course_name:
            # if there is no a key in courses_dicts_list with the name of 
            # current_course_name, if creates it with empty list
            # as its value
            if current_course_name not in courses_dicts_list:
                courses_dicts_list.update({
                    current_course_name: []
                })

            # these conditionals filters the course and exclude it if includes
            # something that is in any black_list_* parameter
            if black_list_courses:
                if current_course_name in black_list_courses:
                    continue
            if black_list_days:

                # that is a dict with the days when the course is given
                # as its keys
                in_forbidden_day: bool = False
                if course_timetable:
                    for day in course_timetable:
                        if day in black_list_days:
                            in_forbidden_day = True
                            break
                    if in_forbidden_day:
                        continue

            if black_list_teachers:
                current_course_teacher: str | None = course.get(TEACHER_KEY)
                # if the teacher of the current course is in black list of teachers
                if current_course_teacher in black_list_teachers:
                    continue

            if black_interval_dict:
                if course_timetable:
                    in_forbidden_time: bool = False
                    for day in course_timetable.values():
                        forbidden_str_timetable: str | None = black_interval_dict.get(STR_TIMETABLE_KEY)
                        day_str_timetable: str | None = day.get(STR_TIMETABLE_KEY)

                        if forbidden_str_timetable and day_str_timetable:
                            in_forbidden_time = compare_timetable_interference(forbidden_str_timetable, day_str_timetable)
                            if in_forbidden_time:
                                break

                    if in_forbidden_time:
                        continue
            
            # adds to the apropriate courses if acomplish the conditions
            courses_dicts_list[current_course_name].append(course)

    # this will tell what are the most common days between signatures
    days_counter_dict: dict = {'LU': 0, 'MA': 0, 'MI': 0, 'JU': 0, 'VI': 0, 'SA': 0, 'DO': 0 }
    courses_dict_list: dict
    for courses_dict_list in courses_dicts_list.values():
        course: dict
        for course in courses_dict_list:
            course_timetables: dict | None = course.get(TIMETABLES_KEY)
            if course_timetables:
                current_course_days: list[str] = list(course_timetables.keys())
                for day in current_course_days:
                    days_counter_dict[day] += 1

    days_counter_items: list[tuple[ str, int ]] = list(days_counter_dict.items())
    days_counter_dict = dict(sorted(days_counter_items, key= lambda tu: tu[1], reverse=True))
    days_counter_order_list: list = list(days_counter_dict.keys())


    # this punctuate the courses depending how many prefered conditions 
    # have. the conditions to punctuate are the prefered_* arguments
    # in the function
    courses_dict_list: dict
    for courses_dict_list in courses_dicts_list.values():

        for course in courses_dict_list:
            course_timetable: dict | None = course.get(TIMETABLES_KEY)
            DEFAULT_PUNCTUATION: int | float = 0
            general_punctuation: int | float = DEFAULT_PUNCTUATION


            # this first add the extra punctuation if the days of the course are the most
            # common day
            if course_timetable:
                course_days: list = list(course_timetable.keys())
                max_extra_punctuation_per_common_day: float = 10 / len(course_days)
                extra_days_punctuation_val: int | float = DEFAULT_PUNCTUATION

                # this will add the 
                for day in course_days:
                    current_day_index: int = days_counter_order_list.index(day)
                    # this is the punctuation that will be added 
                    # depending how common is the day
                    extra_punctuation_per_common_day = (
                        max_extra_punctuation_per_common_day /
                        (current_day_index + 1)
                    )

                    extra_days_punctuation_val += extra_punctuation_per_common_day
                    general_punctuation += extra_punctuation_per_common_day

                course.update({
                    COMMON_DAY_PUNCTUATION_KEY: extra_days_punctuation_val
                })


            if prefered_courses:
                course_punctuation_val: int = DEFAULT_PUNCTUATION
                course_name: str | None = course.get(NAME_KEY)
                if course_name:
                    if course_name in prefered_teachers:
                        course_punctuation_val += 10
                        general_punctuation += 10
                course.update({
                    COURSE_PUNCTUATION_KEY: course_punctuation_val
                })
            if prefered_teachers:
                teacher_punctuation_val: int | float = DEFAULT_PUNCTUATION
                teacher_name: str | None = course.get(TEACHER_KEY)
                if teacher_name:
                    if teacher_name in prefered_teachers:
                        teacher_punctuation_val += 10
                        general_punctuation += 10
                course.update({
                    TEACHER_PUNCTUATION_KEY: teacher_punctuation_val
                })
                pass
            if prefered_interval_dict:
                timetable_punctuation_val: int | float = DEFAULT_PUNCTUATION
                prefered_time_str_timetable: str | None = prefered_interval_dict.get(STR_TIMETABLE_KEY) 

                if course_timetable and prefered_time_str_timetable:
                    # this is the punctuation that the course will receive per
                    # time of class that is in the prefered_interval
                    punctuation_per_day_in_good_interval: float = 10 / len(course_timetable.keys())
                    for day in course_timetable:
                        course_str_timetable: str | None = course.get(STR_TIMETABLE_KEY)
                        if course_str_timetable:
                            is_interfering_good: bool = compare_timetable_interference(
                                prefered_interval_dict,
                                course_str_timetable
                            )
                            # if is in the prefered_interval, the timetable punctuation increases
                            if is_interfering_good:
                                timetable_punctuation_val += punctuation_per_day_in_good_interval
                                general_punctuation += punctuation_per_day_in_good_interval


                course.update({
                    TIMETABLE_PUNCTUATION_KEY: timetable_punctuation_val
                })
            if prefered_days:
                days_punctuation_val: int | float = DEFAULT_PUNCTUATION
                if course_timetable:
                    course_days: list = list(course_timetable.keys())
                    punctuation_per_day_prefered_days: float = 10 / len(course_days)

                    # increase the days_punctuation_val if the day is in prefered days
                    for day in course_days:
                        if day in prefered_days:
                            days_punctuation_val += punctuation_per_day_prefered_days
                            general_punctuation += punctuation_per_day_prefered_days

                course.update({
                    DAYS_PUNCTUATION_KEY: days_punctuation_val
                })


            course.update({GENERAL_PUNCTUATION_KEY: general_punctuation})




    # here the dicts of each course will be ordered depending 
    for courses_names in courses_dicts_list:
        original_courses_list: list[dict] | None = courses_dicts_list.get( courses_names )
        if original_courses_list:
            course: dict
            ordered_courses: list[dict] = sorted(original_courses_list,
                key = lambda course: course[GENERAL_PUNCTUATION_KEY])
            courses_dicts_list.update({
                courses_names: ordered_courses
            })


    # # here, the courses dict list will be ordered in descendent accordingly to
    # # its general_punctuation combinated
    # courses_dicts_list_in_list: list[list] = []


    # courses_list: list[dict]
    # signature_name: str
    # for signature_name, courses_list in courses_dicts_list.items():
        # signature_general_punctuation: int | float | None = 0
        # for course in courses_list:
            # course_general_punctuation: int | float | None = course.get(GENERAL_PUNCTUATION_KEY)
            # if course_general_punctuation:
                # signature_general_punctuation += course_general_punctuation

        # list_to_append: list = []
        # list_to_append.append(signature_name)
        # list_to_append.append(courses_list)
        # list_to_append.append(signature_general_punctuation)
        # courses_dicts_list_in_list.append(list_to_append)

    # # here, order the signatures by the accumulate of general puctuation in descendent order
    # ordered_courses_dicts_list_in_list: list[list] = sorted(courses_dicts_list_in_list, key=lambda course: course[2], reverse=True)
    # ordered_courses_dicts_list_in_list = list(map(lambda course: course[:2], ordered_courses_dicts_list_in_list))

    # # here, the signatures are ordered by the general puctuation
    # courses_dicts_list = dict(ordered_courses_dicts_list_in_list)
    # logging.debug(courses_dicts_list)




    list_possible_courses_full_timetable: list[list] = []
    # here will be the first course of all timetables
    course_number: int = 0

    for i in range(3):
        possible_courses_full_timetable: list[dict] = []
        course_dict_list: list[dict]
        for course_dict_list in courses_dicts_list.values():
            if possible_courses_full_timetable:

                course: dict
                for course in course_dict_list:

                    course_timetable: dict | None = course.get(TIMETABLES_KEY)

                    possible_course: dict
                    for possible_course in possible_courses_full_timetable:
                        
                        possible_course_timetable: dict | None = possible_course.get(TIMETABLES_KEY)

                        # this is a list with the days in common in the timetable
                        # of courses added to possible_courses_full_timetable and
                        # course
                        if course_timetable and possible_course_timetable:
                            days_in_common = [day for day in course_timetable if day in possible_course_timetable]

                            for day in days_in_common:
                                possible_course_str_timetable: str | None = possible_course_timetable[day].get(STR_TIMETABLE_KEY)
                                course_str_timetable: str | None = course_timetable[day].get(STR_TIMETABLE_KEY)
                                if possible_course_str_timetable and course_str_timetable:
                                    there_is_interference: bool = compare_timetable_interference(course_str_timetable, possible_course_str_timetable)

                                    if there_is_interference:
                                        break
                            else:
                                continue
                            break
                    else:
                        possible_courses_full_timetable.append(course)
                        break
            else:
                possible_courses_full_timetable.append(course_dict_list[course_number])
                course_number += 1

        list_possible_courses_full_timetable.append(possible_courses_full_timetable)
    return list_possible_courses_full_timetable






    





