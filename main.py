# interface
import PySimpleGUI as sg
sg.theme('random')
from tools import File, Crypt
from auto import email_os
from database import oficinas

def start():
    flayout = [
        [sg.Text('Bem Vindo')],                          #ROW 1
        [sg.Button('SERVIDOR'), sg.Button('OFICINA')]    #ROW 2
    ]
    window = sg.Window('Notification APP', flayout, size=(500,100), element_justification='center')
    event, values = window.read()
    
    if event == 'SERVIDOR':
        output()
    if event == 'OFICINA':
        window.close()
        oficina()

def oficina():
    OFICINA_REF = []
    for oficina in oficinas():
        OFICINA_REF.append(f'{oficina[0]} - {oficina[1]}')
        
    OFICINA_REG = []
    for element in File.elements('oficina.txt', '&&&'):
        OFICINA_REG.append(element[0])
        
    layout = [
        [sg.Text('Oficina'), sg.Listbox(OFICINA_REF, size=(43, 2), key='-OFICINA-')],   #ROW 1
        [sg.Text('Email  '), sg.InputText('', key='-EMAIL-')],                              #ROW 2
        [sg.Text('Senha '), sg.InputText('', key='-PASSWORD-', password_char='*')],         #ROW 3
        [sg.Button('Adicionar')],
        [sg.Text()],
        [sg.Text('Oficinas Registradas')],
        [sg.Listbox(OFICINA_REG, size=(50, 10), key='-BOX-')],
        [sg.Button('Deletar'), sg.Button('Sair')]
    ]
    window = sg.Window('Registrar Oficina', layout)
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            break
        
        if event == 'Adicionar':
            OFICINA = int(values['-OFICINA-'][0][0])
            EMAIL = values['-EMAIL-']
            PASSWORD = values['-PASSWORD-']

            if OFICINA != '' and len(EMAIL) > 5 and len(PASSWORD) > 3:
                File.add('oficina.txt', f'{OFICINA}&&&{EMAIL}&&&{Crypt.encrypt(PASSWORD)}')
            else:
                print('Formulário preecnchido incorretamente. Não possivel associar email à oficina.')
                
            OFICINA_REG = []
            for element in File.elements('oficina.txt', '&&&'):
                OFICINA_REG.append(element[0])
                
            window.find_element('-EMAIL-').Update('')
            window.find_element('-PASSWORD-').Update('')
            window.find_element('-BOX-').Update(OFICINA_REG)
            
        if event == 'Deletar':
            if OFICINA_REG:
                x = values['-BOX-'][0]
                print(x)
                File.remove('oficina.txt', x + '&')
                OFICINA_REG = []
                for line in File.list('oficina.txt'):
                    OFICINA_REG.append(line.split('&')[0])
                window.find_element('-BOX-').Update(OFICINA_REG)

        if event == 'Sair':
            window.close()
            
def output():
    layout = [
    [sg.Text('Application', size=(30, 1), key='-START-')],
    [sg.Output(size = (100, 20))],
    [sg.Button('Iniciar'), sg.Button('Sair')],
    ]
    window = sg.Window('Notification APP', layout, size=(500, 400))
    event, values = window.read()
    if event == 'Iniciar':
        window.find_element('-START-').Update('Application started')
        while True:
            email_os()
    if event == 'Sair':
        window.close()
        
    
start()

 
