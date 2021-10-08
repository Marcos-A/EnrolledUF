import csv
from sys import argv
import copy

RESULT_FILE = 'result.csv'

CODE_DICT = {"014":"MP01",
             "015":"MP02",
             "003":"MP03",
             "016":"MP04",
             "017":"MP05",
             "018":"MP06",
             "019":"MP07",
             "008":"MP08",
             "009":"MP09",
             "010":"MP10",
             "020":"MP11",
             "012":"MP12",
             "013":"MP13",
             "021":"MP14",
             "022":"MP15"}

MP_DICT = {"MP01":dict.fromkeys(range(1, 5)),
           "MP02":dict.fromkeys(range(1, 4)),
           "MP03":dict.fromkeys(range(1, 4)),
           "MP04":dict.fromkeys(range(1, 4)),
           "MP05":dict.fromkeys(range(1, 4)),
           "MP06":dict.fromkeys(range(1, 5)),
           "MP07":dict.fromkeys(range(1, 7)),
           "MP08":dict.fromkeys(range(1, 3)),
           "MP09":dict.fromkeys(range(1, 2)),
           "MP10":dict.fromkeys(range(1, 5)),
           "MP11":dict.fromkeys(range(1, 2)),
           "MP12":dict.fromkeys(range(1, 3)),
           "MP13":dict.fromkeys(range(1, 2)),
           "MP14":dict.fromkeys(range(1, 5)),
           "MP15":dict.fromkeys(range(1, 5))
           }
    
STUDENTS_DICT = {}


def read_file(filename):
    with open(filename, 'r', encoding='latin-1') as saga_file:
        file_dict = csv.DictReader(saga_file, delimiter=",")
        for row in file_dict:
            student_name = row["00_NOM"]
            student_enrolled_data = row["02_MATRICULADES"]
            student_uf_list = extract_uf_list(student_enrolled_data)

            add_to_student_dict(student_name, student_uf_list)
    # print(STUDENTS_DICT)



def extract_uf_list(student_enrolled_data):
    uf_list = [code for code in student_enrolled_data.split(',') if len(code) == 5]
    return uf_list


def add_to_student_dict(student_name, student_uf_list):
    student_mp_dict = copy.deepcopy(MP_DICT)

    for uf in student_uf_list:
        mp = CODE_DICT[uf[0:3]]
        uf = uf[-1]
        student_mp_dict[mp][int(uf)] = 'x'
    
    STUDENTS_DICT[student_name] = student_mp_dict

    
def generate_file():
    with open(RESULT_FILE, 'w', encoding='utf-8') as result_file:
        file_writer = csv.writer(result_file)
        file_writer.writerow(generate_file_header_list())
        for student_name in STUDENTS_DICT:
            student_mp_dict = STUDENTS_DICT[student_name]
            file_writer.writerow(generate_student_uf_list(student_name, student_mp_dict))


def generate_file_header_list():
    header_list = ["ESTUDIANT"]
    for mp in MP_DICT:
        for uf in MP_DICT[mp]:
            item = mp + "-UF" + str(uf)
            header_list.append(item)
    
    return header_list


def generate_student_uf_list(student_name, student_mp_dict):
    student_uf_list = [student_name]
    for mp in student_mp_dict:
        for uf in student_mp_dict[mp]:
            if student_mp_dict[mp][uf] is None:
                student_uf_list.append("")
            else:
                student_uf_list.append(student_mp_dict[mp][uf])

    return student_uf_list


if __name__ == "__main__":
    filename = argv[1]
    read_file(filename)
    generate_file()

