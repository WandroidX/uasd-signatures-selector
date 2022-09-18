import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import sys
sys.path.append('src')
from src import file_management as filema
from src import webdriver_operations as webop
from src import dict_management as dictma


def main():
    # USEFUL_SIGNATURES_NAMES: list[str] = ['Biología Básica', 'Laboratorio de Biología Básica', 'Física Básica', 'Introd A Las Ciencias Sociales', 'Matemática Básica', 'Lengua Española Básica II', 'Química Básica', 'Laboratorio de Física Básica']
    USEFUL_SIGNATURES_NAMES: list[str] = [ 'Laboratorio de Biología Básica', 'Física Básica', 'Química Básica', 'Laboratorio de Física Básica']
    USEFUL_COLUMNS_INDEX: list[int] = [2, 10, 11, 4]
    USEFUL_COLUMNS_NAMES: list[str] = ['NRC', 'Horario', 'Dias', 'Asignatura']
    personal_uasd_dict_list = filema.get_signatures_from_file(
        campus_where = 'San Juan', 
        signatures_file=r'c:\users\crist\downloads\personal_uasd_signatures.xlsx',
        signatures_names= USEFUL_SIGNATURES_NAMES, 
        useful_columns_index= USEFUL_COLUMNS_INDEX,
        useful_columns_names = USEFUL_COLUMNS_NAMES 
    )
    virtual_uasd_dict_list = filema.get_signatures_from_file(
        campus_where = 'San Juan', 
        signatures_file=r'c:\users\crist\downloads\virtual_uasd_signatures.xlsx',
        signatures_names= USEFUL_SIGNATURES_NAMES, 
        useful_columns_index= USEFUL_COLUMNS_INDEX,
        useful_columns_names = USEFUL_COLUMNS_NAMES 
    )

    all_signatures_data = [*virtual_uasd_dict_list, *personal_uasd_dict_list]
    all_signatures_nrc = list(set(element['NRC'] for element in all_signatures_data))

    service = Service(executable_path=r'c:\users\crist\downloads\creative_projects\python\geckodriver\geckodriver.exe')
    driver = webdriver.Firefox(service=service)
    webop.open_uasd_in_selection_page(driver = driver,
                            username = '100678858',
                            password = '@Eljefe2005')
    time.sleep(5)
    signatures_found = webop.search_signatures_by_nrc_in_uasd( driver, all_signatures_nrc)
    signatures_info = []


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
    SIGNATURES_INFO_FILE = r'c:\users\crist\desktop\uasd_signatures_info.txt'
    filema.write_signatures_data(SIGNATURES_INFO_FILE, signatures_found, USEFUL_KEYS)


if __name__ == "__main__":
    main()
else:
    raise Exception('must be executed as script')
