from datetime import datetime
from time import sleep
from os import mkdir, path

day=datetime.today().day
month=datetime.today().month
if day<=9:
    day='0'+str(day)
if month<=9:
    month='0'+str(month)
month=str(month)
day=str(day)

input_file_name='RequerimientoExtPlazo_'+day+month+'.txt'
if not path.isfile(input_file_name):
    print(f"Archivo de entrada {input_file_name} inexistente.")
    sleep(5)
    exit(0)

output_folder = 'Salida/'
if not path.isdir(output_folder):
    mkdir(output_folder)

while True:
    print('--------------------')
    normalization=0
    while(normalization<1 or normalization>2):
        try:
            normalization=int(input('Ingrese el número de normalización (1 o 2): '))
        except ValueError:
            print('Valor no numérico ingresado. Saliendo del programa.')
            sleep(5)
            exit(0)
            
        if(normalization==1):
            raw_output_file_name='INPUT_LOAN_TAM'
            output_file_10_name='N1_10.txt'
            output_file_16_name='N1_16.txt'
            break
        elif(normalization==2):
            raw_output_file_name='INPUT_LOAN_FILE_MORA'
            output_file_10_name='N2_10.txt'
            output_file_16_name='N2_16.txt'
            break
        else:
            print('Solo puede ingresar 1 o 2')
            
    print('Archivo de entrada: '+input_file_name)
    print('Archivo de salida: '+raw_output_file_name)

    raw_output_file = open(output_folder+raw_output_file_name,'w')
    input_file = open(input_file_name)
    output_file_10 = open(output_folder+output_file_10_name,'w')
    output_file_16 = open(output_folder+output_file_16_name,'w')
    sql_query=open(output_folder+'query.sql','w')
    sql_query.write("SELECT ACCT_NO, to_date(date_payment + 2415020, 'j') FROM REPS WHERE ACCT_NO IN ( ")

    lines = input_file.readlines()
    counter_wrong_operations=0
    for counter, line in enumerate(lines):
        fields=line.strip().split('\t')
        if(counter!=0):
            fields[1]=fields[1].replace('"', '')
            if(int(fields[3])>24):
                print(fields[1]+' no considerada por número de cuotas: '+str(fields[3]))
                counter_wrong_operations+=1
                continue
            while(len(fields[3])<3):
                fields[3]='0'+fields[3]
            output_file_10.write(fields[1]+'\n')
            register='000000'+fields[1]
            output_file_16.write(register+'\n')
            if counter != len(lines)-1:
                sql_query.write(f"'{register}', ")
            else:
                sql_query.write(f"'{register}'")
            register=register+';'+fields[3]+';'
            if(normalization==2):
                register=register+'003;'
            print(register)
            raw_output_file.write(register+'\n')
    sql_query.write(");")

    print('Registros totales: '+str(counter-counter_wrong_operations))

    input_file.close()
    raw_output_file.close()
    output_file_16.close()
    output_file_10.close()
    sql_query.close()