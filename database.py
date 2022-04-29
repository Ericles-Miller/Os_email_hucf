from tools import File, Crypt
from connection import ora
from connection import mvintegra
import datetime
import cx_Oracle


def oficinas():
    cur = ora()
    query = 'SELECT cd_oficina, ds_oficina FROM dbamv.oficina'
    return cur.execute(query)

def list_os(days=30):
    cur = ora()
    date_now = datetime.datetime.now()
    if date_now >= datetime.datetime(2020, 12, 14) and date_now <= datetime.datetime(2021, 1, 14):
       date = datetime.datetime(2020, 12, 14)
    else:
        date = date_now - datetime.timedelta(days = days)
    date = date.strftime("%d/%m/%Y")
        
    query = "select O.CD_OS, O.TP_SITUACAO, O.DT_PEDIDO, O.DS_SERVICO, O.CD_OFICINA, DS_EMAIL_ALTERNATIVO, IO.HR_INICIO, IO.HR_FINAL, F.NM_FUNC, (SELECT U.NM_USUARIO FROM DBASGU.USUARIOS U WHERE O.NM_SOLICITANTE = U.CD_USUARIO) AS NOME_SOLICITANTE, (SELECT U.NM_USUARIO FROM DBASGU.USUARIOS U WHERE O.CD_RESPONSAVEL = U.CD_USUARIO) AS NOME_RESPONSAVEL, (SELECT U.NM_USUARIO FROM DBASGU.USUARIOS U WHERE O.CD_USUARIO_CANCELAMENTO = U.CD_USUARIO), O.DS_JUSTIFICA_CANCELAMENTO, O.DS_OBSERVACAO from DBAMV.SOLICITACAO_OS O, DBAMV.ITSOLICITACAO_OS IO, DBAMV.FUNCIONARIO F where O.DT_PEDIDO >= to_date('{}') AND O.CD_OS = IO.CD_OS(+) AND IO.CD_FUNC = F.CD_FUNC(+) AND TP_SITUACAO !='S'".format(date)
    solicitations = cur.execute(query)
    list_solicitations = []

    
    for solicitation in solicitations:
        solicitation = { 'identifier': solicitation[0], 'status': solicitation[1], 'date': solicitation[2], 'service': solicitation[3], 'oficina': solicitation[4], 'receiver': solicitation[5], 'start_date': solicitation[6], 'end_date': solicitation[7], 'user_ends_request': solicitation[8], 'requester': solicitation[9], 'responsible': solicitation[10], 'cancellation_user': solicitation[11], 'cancellation': solicitation[12], 'observation': solicitation[13]}
        list_solicitations.append(solicitation)
    return list_solicitations

class Mensage:
    def find(identifier, subject, status):
        cur = ora()
        query = "select * from MENSAGEM_EMAIL M where M.CD_IDENTIFICADOR_MENSAGEM = {} AND M.TP_STATUS = '{}'".format(identifier, status)

        #conta registros
        count = 0
        mensages = cur.execute(query)
        for mensage in mensages:
            count = count+1
        if(count == 0):
            return False
        return True

    def register(mensage):
        con = mvintegra()
        cur = con.cursor()
        date_create = datetime.datetime.now()
        date_create = date_create.strftime("%Y/%m/%d %H:%M:%S")

        param = cur.var(
        cx_Oracle.STRING,
        255,
        arraysize=cur.arraysize,
        outconverter=int
        )
        
        statement = "insert into MENSAGEM_EMAIL(DS_REMETENTE, DS_DESTINATARIO, DS_ASSUNTO, DS_MENSAGEM, TP_STATUS, DT_CRIACAO, CD_IDENTIFICADOR_MENSAGEM, CD_MENSAGEM_EMAIL) values (:1, :2, :3, :4, :5, to_date(:d, :f), :7, dbamv.seq_mensagem_email.nextval) RETURNING MENSAGEM_EMAIL.CD_MENSAGEM_EMAIL INTO :8"
        #values = "values ('{}', '{}', '{}', '{}', '{}', to_date('{}', 'yyyy-mm-dd hh24:mi:ss'), {}, seq_mensagem_email.nextval)".format(mensage['sender'], mensage['receiver'], mensage['subject'], mensage['description'], mensage['status'], date_create, mensage['identifier'])
        cur.execute(statement, { "1":mensage['sender'], "2":mensage['receiver'], "3":mensage['subject'], "4":mensage['description'], "5":mensage['status'], "d":date_create, "f":'yyyy-mm-dd hh24:mi:ss', "7":mensage['identifier'], "8":param})
        con.commit()

     

    def os():
        list_solicitation = []
        for solicitation in list_os():
            exist = Mensage.find(solicitation['identifier'], "OS", solicitation['status'])  
            if not exist:
                list_solicitation.append(solicitation)
        return list_solicitation
