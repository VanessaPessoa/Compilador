from lexico import Lexico

lexico = Lexico('./pas/program.txt')
tabela_token = lexico.analisador_sintatico()
