from cryptography.fernet import Fernet

class File:
    def list(path): # retorna arquivo
        file = open(path, "r")
        return file

    def add(path, line): # adiciona uma linha de um arquivo
        file = open(path, 'r')
        elements = file.readlines()
        line = line.replace('\n', '') + '\n'
        elements.append(line)
        file = open(path, 'w')
        file.writelines(elements)
        file.close()
        
    def remove(path, content): # remove uma linha de um arquivo
        elements = []
        file = open(path, 'r')
        for line in file:
            if not (content in line):
                elements.append(line)
        file = open(path, 'w')
        file.writelines(elements)
        file.close()
        
    def find(path, content, delimiter = '&'): # procura conteúdo na linha
        file = open(path, 'r')
        for line in list(path):
            if content in line:
                element = {}
                key = 0 
                for item in line.split(delimiter):
                    element.update({key:item})
                    key += 1
                return element

    def elements(path, delimiter = '&'):
        elements = []
        for line in File.list(path):
            element = {}
            key = 0 
            for item in line.split(delimiter):
                element.update({key:item})
                key += 1
            elements.append(element)
        return elements

class Crypt():
    def encrypt(text, key = b'q587vzuygHeu08pBCQbN8lkw26pYBTlf2Fue12yFLUk='): # criptografa
        f = Fernet(key)
        token = f.encrypt(bytes(f'{text}', 'utf-8'))
        return token

    def generate_key(): # gera uma chave de criptografia
        key = Fernet.generate_key() 
        return key

    def decrypt(token, key = b'q587vzuygHeu08pBCQbN8lkw26pYBTlf2Fue12yFLUk='): # decriptografa
        f = Fernet(key)
        text = f.decrypt(token)
        return text.decode("utf-8") 
      

