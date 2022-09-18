import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import config
import sys
sys.path.append('src')
from src import file_management as filema
from src import webdriver_operations as webop
from src import dict_management as dictma


def main():
    # important constants for the program
    USEFUL_SIGNATURES_NAMES: list[str] = config.SIGNATURES_TO_SELECT
    USEFUL_COLUMNS_INDEX: list[int] = config.USEFUL_COLUMNS_INDEX
    USEFUL_COLUMNS_NAMES: list[str] = config.USEFUL_COLUMNS_HEADERS
    CAMPUS: str = config.COURSES_CAMPUS
    PRESENCIAL_COURSES_PATH: str = config.PRESENCIAL_COURSES_XL_FILE_PATH
    VIRTUAL_COURSES_PATH: str = config.VIRTUAL_COURSES_XL_FILE_PATH
    GECKO_DRIVER_PATH: str = config.GECKO_DRIVER_PATH
    USERNAME: str = config.UASD_ACCESS_USERNAME
    PASSWORD: str = config.UASD_ACCESS_PASSWORD

    personal_uasd_dict_list = filema.get_signatures_from_file(
        campus_where = CAMPUS, 
        signatures_file=PRESENCIAL_COURSES_PATH,
        signatures_names= USEFUL_SIGNATURES_NAMES, 
        useful_columns_index= USEFUL_COLUMNS_INDEX,
        useful_columns_names = USEFUL_COLUMNS_NAMES 
    )
    virtual_uasd_dict_list = filema.get_signatures_from_file(
        campus_where = CAMPUS, 
        signatures_file=VIRTUAL_COURSES_PATH,
        signatures_names= USEFUL_SIGNATURES_NAMES, 
        useful_columns_index= USEFUL_COLUMNS_INDEX,
        useful_columns_names = USEFUL_COLUMNS_NAMES 
    )

    all_signatures_data = [*virtual_uasd_dict_list, *personal_uasd_dict_list]
    all_signatures_nrc = list(set(element['NRC'] for element in all_signatures_data))

    service = Service(executable_path=GECKO_DRIVER_PATH)
    driver = webdriver.Firefox(service=service)
    webop.open_uasd_in_selection_page(driver = driver,
                            username = USERNAME,
                            password = PASSWORD)
    time.sleep(5)
    signatures_found = webop.search_signatures_by_nrc_in_uasd( driver, all_signatures_nrc)


    for i, signature in enumerate( signatures_found ):
        current_signature_list_dict = dictma.get_dicts_from_dicts_list(all_signatures_data, {'NRC': signature['NRC']}, can_be_several=True)


        if current_signature_list_dict:

            if len( current_signature_list_dict ) > 1:
                current_signature_full_data = dictma.merge_dicts(current_signature_list_dict)
            else:
                current_signature_full_data = current_signature_list_dict[0]




            signatures_found[i].update({
                'Dias': current_signature_full_data['Dias'],
                'Horario': current_signature_full_data['Horario'] ,
                'Asignatura': current_signature_full_data['Asignatura']
            })


    USEFUL_KEYS = ['Status','Asignatura', 'NRC', 'Dias', 'Horario']
    SIGNATURES_INFO_FILE = config.OUTPUT_FILE_PATH
    filema.write_signatures_data(SIGNATURES_INFO_FILE, signatures_found, USEFUL_KEYS)


if __name__ == "__main__":
    main()
else:
    raise Exception('must be executed as script')
