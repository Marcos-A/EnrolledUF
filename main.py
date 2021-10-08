import csv
from sys import argv
import copy

RESULT_FILE_PER_STUDENT = 'result_per_student.csv'
RESULT_FILE_PER_MP = 'result_per_mp.txt'
CLEAN_GAJ1_MP_AND_UF_FROM_RESULT_FILE_PER_MP = True

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
    
MP_NAME_DICT = {"MP01":"Comunicació empresarial i atenció al client",
                "MP02":"Operacions administratives de compravenda",
                "MP03":"Operacions administratives de recursos humans",
                "MP04":"Operacions auxiliars de gestió de tresoreria",
                "MP05":"Tècnica comptable",
                "MP06":"Tractament de la documentació comptable",
                "MP07":"Tractament informàtic de la informació",
                "MP08":"Operacions administratives de suport",
                "MP09":"Anglès",
                "MP10":"Empresa i Administració",
                "MP11":"Empresa a l’aula",
                "MP12":"Formació i orientació laboral",
                "MP13":"Formació en centres de treball",
                "MP14":"Organització i estructura de l’àmbit jurídic i judicial",
                "MP15":"Tramitació processal i auxili judicial"}

STUDENTS_DICT = {}

MP_WITH_ENROLLED_STUDENTS_DICT = dict.fromkeys(["MP01", "MP02", "MP03", "MP04", "MP05",
                                                "MP06", "MP07", "MP08", "MP09", "MP10",
                                                "MP11", "MP12", "MP13", "MP14", "MP15"])

GAJ2_MP_EXCEPT_MP07 = ["MP04", "MP06", "MP08", "MP09", "MP11", "MP12", "MP13", "MP15"]
GAJ2_MP07_UF = ["UF4", "UF5", "UF6"]


def read_file(filename):
    with open(filename, 'r', encoding='latin-1') as saga_file:
        file_dict = csv.DictReader(saga_file, delimiter=",")
        for row in file_dict:
            student_name = row["00_NOM"]
            student_enrolled_data = row["02_MATRICULADES"]
            student_uf_list = extract_uf_list(student_enrolled_data)

            add_to_student_dict(student_name, student_uf_list)



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

    
def generate_file_per_student():
    with open(RESULT_FILE_PER_STUDENT, 'w', encoding='utf-8') as result_file:
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


def mp_with_enrolled_students_dict():
    for student in STUDENTS_DICT:
        for mp in STUDENTS_DICT[student]:
            student_mp_dict = STUDENTS_DICT[student][mp]
            check = any(student_mp_dict.values())
            if check is True:
                student_mp_uf_dict = STUDENTS_DICT[student][mp]
                uf_list = get_list_from_dict_of_uf(student_mp_uf_dict)

                if MP_WITH_ENROLLED_STUDENTS_DICT[mp] is None:
                    MP_WITH_ENROLLED_STUDENTS_DICT[mp] = []
                MP_WITH_ENROLLED_STUDENTS_DICT[mp].append(student + ": " + ", ".join(uf_list))

    return MP_WITH_ENROLLED_STUDENTS_DICT
                

def generate_file_per_mp():
    if CLEAN_GAJ1_MP_AND_UF_FROM_RESULT_FILE_PER_MP:
        clean_gaj1_mp_and_uf()
    with open(RESULT_FILE_PER_MP, "w") as result_file:
        for mp in MP_WITH_ENROLLED_STUDENTS_DICT:
            result_file.write(mp + " - " + MP_NAME_DICT[mp] + ':'+'\n')
            for student in MP_WITH_ENROLLED_STUDENTS_DICT[mp]:
                result_file.write('\t• ' + student + '\n')
            result_file.write('\n')


def clean_gaj1_mp_and_uf():
    for mp in GAJ2_MP_EXCEPT_MP07:
        del MP_WITH_ENROLLED_STUDENTS_DICT[mp]

    for uf in GAJ2_MP07_UF:
        new_mp07_data = []
        for student in MP_WITH_ENROLLED_STUDENTS_DICT["MP07"]:
            new_student = student
            if uf in new_student:
                new_student = student.replace(uf, "").replace(" ,", "").strip()
                if new_student[-1] == ',':
                    new_student = new_student[:-1]
            new_mp07_data.append(new_student)
        MP_WITH_ENROLLED_STUDENTS_DICT["MP07"] = new_mp07_data
    MP_WITH_ENROLLED_STUDENTS_DICT["MP07"] = [student for student in MP_WITH_ENROLLED_STUDENTS_DICT["MP07"] if "UF" in student]


def get_list_from_dict_of_uf(student_mp_uf_dict):
    uf_list = []
    i = 1
    for uf in student_mp_uf_dict:
        if student_mp_uf_dict[uf] is not None:
            uf_list.append("UF" + str(i))
        i += 1
    
    return uf_list


if __name__ == "__main__":
    filename = argv[1]
    read_file(filename)
    generate_file_per_student()
    mp_with_enrolled_students_dict()
    generate_file_per_mp()
    

