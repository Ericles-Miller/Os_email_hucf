import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import time
import datetime

from pymysql import NULL
from tools import File, Crypt
from database import Mensage


def gmail(sender_address, sender_pass, receiver_address, subject, mail_content):
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')




def email_os():
    print('STARTED!!!')
    email_list = [{'email': 'naoresponda.hucf@unimontes.br', 'password':'ckp8yZbU','oficina':5 },
                  {'email': 'naoresponda.hucf@unimontes.br', 'password':'ckp8yZbU','oficina':15},
                  {'email': 'naoresponda.hucf@unimontes.br', 'password':'ckp8yZbU','oficina':3 },
                  {'email': 'naoresponda.hucf@unimontes.br', 'password':'ckp8yZbU','oficina':17},
                  
                 ]
    section = {}
    '''for oficina in File.elements('oficina.txt', '&&&'):
        password = oficina[2].replace("b'", '').replace("'", '')
        password = Crypt.decrypt(bytes(f'{password}', 'utf-8'))
        section.update({ int(oficina[0]): {'oficina': int(oficina[0]), 'email': oficina[1], 'password': password}}) '''
    for i in range(0,len(email_list)):
        password = email_list[i]['password']
        email    = email_list[i]['email']
        oficina  = email_list[i]['oficina']
        section.update({oficina:{'oficina':oficina, 'email':email,'password':password}})

    solicitations = []
    for solicitation in Mensage.os():
        if solicitation['oficina'] in section:
            solicitations.append({**solicitation})
            
    for solicitation in solicitations:
        if solicitation['status'] == 'A':
            subject = 'Ordem de servi??o aberta'
            if solicitation['responsible'] is None:
                mail_content = f"Ol?? {solicitation['requester'].strip().split(' ')[0].capitalize()}, \n\nSua ordem de servi??o,\n\nN??mero: {solicitation['identifier']} \nDescri????o: {solicitation['service']} \n\nFoi aberta por. Em casos de d??vidas, contatar o respons??vel pela execu????o da OS. \n\nEsta mensagem ?? autom??tica e informativa, n??o h?? necessidade de responde-l??."
            else:
                mail_content = f"Ol?? {solicitation['requester'].strip().split(' ')[0].capitalize()}, \n\nSua ordem de servi??o,\n\nN??mero: {solicitation['identifier']} \nDescri????o: {solicitation['service']} \n\nFoi aberta por {solicitation['responsible'].strip().split(' ')[0].capitalize()}. Em casos de d??vidas, contatar o respons??vel pela execu????o da OS. \n\nEsta mensagem ?? autom??tica e informativa, n??o h?? necessidade de responde-l??."

        if solicitation['status'] == 'C':     
            subject = 'Ordem de servi??o finalizada'
        
            if solicitation['user_ends_request'] is None: #.strip().split(' ')[0]
                mail_content = f"Ol?? {solicitation['requester'].strip().split(' ')[0].capitalize()}, \n\nSua ordem de servi??o,\n\nN??mero: {solicitation['identifier']} \nDescri????o: {solicitation['service']} \n\nFoi concluida no per??odo de {solicitation['start_date']} a {solicitation['end_date']}. Para tanto, avalie, se poss??vel, o nosso servi??o, acesando o seguinte caminho no SOUL MV:\nServi??os de Apoio> Manuten????o> Ordem Servi??o> Avalia????o de Ordem de Servi??o.\n\nEsta mensagem ?? autom??tica e informativa, n??o h?? necessidade de responde-l??." 
            else:  
                mail_content = f"Ol?? {solicitation['requester'].strip().split(' ')[0].capitalize()}, \n\nSua ordem de servi??o,\n\nN??mero: {solicitation['identifier']} \nDescri????o: {solicitation['service']} \n\nFoi concluida por {solicitation['user_ends_request'].strip().split(' ')[0].capitalize()} no per??odo de {solicitation['start_date']} a {solicitation['end_date']}. Para tanto, avalie, se poss??vel, o nosso servi??o, acesando o seguinte caminho no SOUL MV:\nServi??os de Apoio> Manuten????o> Ordem Servi??o> Avalia????o de Ordem de Servi??o.\n\nEsta mensagem ?? autom??tica e informativa, n??o h?? necessidade de responde-l??."

        if solicitation['status'] == 'D':
            subject = 'Ordem de servi??o cancelada.'
            mail_content = f"Ol?? {solicitation['requester'].strip().split(' ')[0].capitalize()}, \n\nSua ordem de servi??o,\n\nN??mero:{solicitation['identifier']} \nDescri????o: {solicitation['service']} \n\nFoi cancelada por {solicitation['cancellation_user'].strip().split(' ')[0].capitalize()}\n\nJustificativa: {solicitation['cancellation']}. \n\nEsta mensagem ??autom??tica e informativa, n??o h?? necessidade de responde-l??."

        if solicitation['status'] == 'M':
            subject = 'Ordem de servi??o est?? aguardando material.'
            mail_content = f"Ol?? {solicitation['requester'].strip().split(' ')[0].capitalize()}, \n\nSua ordem de servi??o,\n\nN??mero:{solicitation['identifier']} \nDescri????o: {solicitation['service']} \n\nEst?? aguardando material, devido ?? falta de recurso para efetivar a solicita????o.\n\nJustificativa: {solicitation['observation']}. \n\nEsta mensagem ??autom??tica e informativa, n??o h?? necessidade de responde-l??."

        sender_address = section[solicitation['oficina']]['email']
        sender_pass = section[solicitation['oficina']]['password']
        
        #print(solicitation['oficina'], sender_address, sender_pass)
        mensage = {'sender': sender_address, 'receiver': solicitation['receiver'], 'subject': 'OS', 'description': mail_content, 'status':solicitation['status'], 'identifier': solicitation['identifier']}
        gmail(sender_address, sender_pass, solicitation['receiver'].lower(), subject, mail_content)
        Mensage.register(mensage)
        print(mensage)

