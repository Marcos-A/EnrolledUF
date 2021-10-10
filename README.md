# EnrolledUF
Script that takes a CSV file downloaded from [SAGA](https://inlab.fib.upc.edu/en/saga-system-administration-and-academic-management-public-schools-under-department-education) and generates a clean display of the student's enrolled UF in two diferent formats: CSV (result_per_student.csv) and TXT (result_per_mp.txt).

The codes in this version apply just to GAJ2 during the academic year 2021-22.

## Requeriments
The downloaded CSV must include the following columns:
- 00_NOM
- 01_IDENTIFICADOR_DE_L'ALUMNE
- 02_MATRICULADES

## Options
The TXT result file will include either:
- every enrolled UF
- only the enrolled UF pending from GAJ1

You can toggle this option setting the CLEAN_GAJ1_MP_AND_UF_FROM_RESULT_FILE_PER_MP constant to False or True respectively.

## How to run
From the terminal execute the following command:

`$ python enrolled_uf.py saga_downloaded_file_path.csv`
