from datetime import datetime

day=datetime.today().day
month=datetime.today().month
if month<9:
    month='0'+str(month)
month=str(month)
day=str(day)

input_file_name='RequerimientoExtPlazo_'+day+month+'.txt'

normalization=2
if(normalization==1):
    output_file_name='INPUT_LOAN_TAM'
elif(normalization==2):
    output_file_name='INPUT_LOAN_FILE_MORA'
else:
    raise Exception('Ingresar una normalización adecuada')

print('Archivo de entrada: '+input_file_name)
print('Archivo de salida: '+output_file_name)

input_file = open(input_file_name)
raw_output_file = open(output_file_name,'w')
output_file_10 = open('OP_10.txt','w')
output_file_16 = open('OP_16.txt','w')

lines = input_file.readlines()
for counter, line in enumerate(lines):
    fields=line.strip().split('\t')
    if(counter!=0):
        fields[1]=fields[1].replace('"', '')
        while(len(fields[3])<3):
            fields[3]='0'+fields[3]
        output_file_10.write(fields[1]+'\n')
        register='000000'+fields[1]
        output_file_16.write(register+'\n')
        register=register+';'+fields[3]+';'
        if(normalization==2):
            register=register+'003;'
        print(register)
        raw_output_file.write(register+'\n')

input_file.close()
raw_output_file.close()
output_file_16.close()
output_file_10.close()