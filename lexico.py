import os
import re


class Lexico:

    def __init__(self, path_filename):
        self.caminho = os.path.dirname(path_filename)
        self.reservado = ("program",  "var",  "integer",  "real",  "boolean",  "procedure",  "begin", "end", "if",
                          "then", "else", "while", "do", 'not', 'true', 'false')
        self.delimitador = (';', '.', ':', '(', ')')
        arquivo = open(path_filename, 'r')
        conteudo = arquivo.read()
        self.lista = list(conteudo)
        self.posicao_caracter = -1
        self.linha = 1
        self.token = ''
        self.linha_tabela = dict()
        self.tabela = list()

    def leia_caracter(self, i):
        return self.lista[i]

    def letra(self, caracter):
        if re.findall("[a-zA-Z]", caracter):
            return True
        else:
            return False

    def digito(self, caracter):
        if re.findall("[0-9]", caracter):
            return True
        else:
            return False

    def adicionar_tabela(self, classificador):
        self.linha_tabela['Token'] = self.token
        self.linha_tabela['Classificador'] = classificador
        self.linha_tabela['Linha'] = self.linha
        self.tabela.append(self.linha_tabela.copy())
        self.token = ''

    def fill_blanks(self, data, size):
        data = str(data)
        if len(data) > size:
            data = data[:size]
        return str('|  ' + data.ljust(size))

    def resultado_lexico(self):
        table = []
        table.append(self.fill_blanks('Token', 30) + self.fill_blanks("Classification",
                                                                      30) + self.fill_blanks('Line', 5) + '  |')
        table.append(
            '================================================================================')
        for item in self.tabela:
            token = item["Token"].rstrip("\n")
            classification = item["Classificador"].rstrip("\n")
            line = item["Linha"]
            table.append(self.fill_blanks(token, 30) + self.fill_blanks(classification,
                                                                        30) + self.fill_blanks(line, 5) + '  |')

        with open("./resultado/tabela_token.txt", "w") as file:
            for i in table:
                file.write(str(i + '\n'))

            return table

    def analisador_sintatico(self):
        while True:
            self.posicao_caracter += 1

            if self.posicao_caracter == len(self.lista):
                return self.resultado_lexico()

            caracter = self.leia_caracter(self.posicao_caracter)

            if caracter == ' ':
                continue

            if caracter == '\n':
                self.linha += 1
                continue

            if self.letra(caracter):
                self.identificador()
                continue

            if caracter in ['+', '-']:
                self.token = caracter
                self.adicionar_tabela('Operadores aditivos')
                continue

            if caracter in ['*', '/']:
                self.token = caracter
                self.adicionar_tabela('Operadores multiplicativos')
                continue

            if caracter == ':':
                self.token += caracter
                self.atribuicao()
                continue

            if caracter in self.delimitador:
                self.token = caracter
                self.adicionar_tabela('Delimitador')
                continue

            if caracter == '=':
                self.token = caracter
                self.adicionar_tabela('Operadores relacionais')
                continue

            if caracter == '>':
                self.token = caracter
                self.posicao_caracter += 1
                caracter = self.leia_caracter(self.posicao_caracter)
                if caracter == '=':
                    self.token += caracter
                if caracter == '\n':
                    self.linha += 1
                self.adicionar_tabela('Operadores relacionais')
                continue

            if caracter == '<':
                self.token = caracter
                self.posicao_caracter += 1
                caracter = self.leia_caracter(self.posicao_caracter)
                if caracter == '=' or caracter == '>':
                    self.token += caracter
                if caracter == '\n':
                    self.linha += 1
                self.adicionar_tabela('Operadores relacionais')
                continue


    def atribuicao(self):
        self.posicao_caracter += 1
        proximo_caracter = self.leia_caracter(self.posicao_caracter)
        if proximo_caracter == '=':
            self.token += proximo_caracter
            self.adicionar_tabela('Comando de atribuicao')
        elif proximo_caracter == ' ':
            self.adicionar_tabela('Delimitador')

    def identificador(self):
        caracter = self.leia_caracter(self.posicao_caracter)
        while self.letra(caracter) or self.digito(caracter) or caracter == '_':
            self.token += caracter
            self.posicao_caracter += 1
            caracter = self.leia_caracter(self.posicao_caracter)

        if self.token in self.reservado:
            self.adicionar_tabela('Palavra chave')
        elif self.token == 'and':
            self.adicionar_tabela('Operadores multiplicativos')
        elif self.token == 'or':
            self.adicionar_tabela('Operadores aditivos')
        else:
            self.adicionar_tabela('Identificador')

        if caracter == '\n':
            self.linha += 1

        if caracter in self.delimitador:
            self.token = caracter
            self.adicionar_tabela('Delimitador')

