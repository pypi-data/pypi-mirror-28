"""
Esta distribuição contem um conjunto de classes e funçoes
utilizadas para a criação de um sistema automatizado de
gerenciamento de uma turma
"""



class Pessoa:
    """
    Esta classe descreve uma pessoa com os atributos Nome e Email 
    """
    def __init__(self, a_Nome, a_Email=''):
        self._Nome = a_Nome
        self._Email = a_Email
    def getNome(self):
        return self._Nome
    def getEmail(self):
        return self._Email


class Aluno(Pessoa):
    """
    A classe aluno herda de Pessoa os atributos Nome e Email. Além disso
    ela tem o atributo Matricula
    """
    def __init__(self, a_Nome, a_Matricula,a_Email=''):
        Pessoa.__init__(self,a_Nome,a_Email)
        self._Matricula = a_Matricula
    def getMatricula(self):
        return self._Matricula 
    


class Turma(list):
    """
    Esta classe define uma Turma. Em termos gerais, ela é uma lista de objetos
    Aluno. Cada um destes objetos representa um determinado aluno. Além disso,
    a classe também define atributos que definem a turma, como Nome da matéria,
    carga horária, códico da disciplina, período e etc.
    """
    def __init__(self, a_Nome, a_Periodo, a_Numero, a_CH = 90, a_Codigo='', a_ABV=''):
        list.__init__([]) #Lista de alunos
        self._Nome = a_Nome
        self._CH = a_CH
        self._Codigo = a_Codigo
        self._ABV = a_ABV
        self._Periodo = a_Periodo
        self._Numero = a_Numero
    def getNome(self):
        return self._Nome
    def getPeriodo(self):
        return self._Periodo
    def getNumero(self):
        return self._Numero
    def getCH(self):
        return self._CH
    def getABV(self):
        return self._ABV
    def getCodigo(self):
        return self._Codigo
    def getTamanho(self):
        return self.__len__()
    

     


def CriaTurma(arq_turma):
    """
    Esta função cria um objeto Turma a partir dos dados de um arquivo de texte
    arq_turma. Este arquivo se encontra no formado especifico da UERJ e
    apresenta em suas linhas o nome da disciplina, o número da turma, o
    período letivo e uma lista com o nome e a matricula dos alunos incritos
    na turma.
    """
    line = 1
    try:
        with open(arq_turma) as f:
            for linha in f:
                if line==2:
                    temp_nome = linha.strip().split(':')
                elif line ==3:
                    temp_numero = linha.strip().split(':')
                elif line==4:
                    temp_periodo = linha.strip().split(':')
                    temp_turma = Turma(temp_nome[1],temp_periodo[1],temp_numero[1])
                elif line>6:
                    temp_aluno = linha.strip().split('\t')
                    temp_turma.append(Aluno(temp_aluno[0],temp_aluno[1]))
                line += 1
        return temp_turma    
    except IOError as err:
        print("Erro: " + str(err) )
        return(None)
