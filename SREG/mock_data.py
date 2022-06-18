
import re
import numpy as np
import pandas as pd
from faker import Faker

from datetime import datetime

# Classe Paciente, com as informações essenciais usadas para a linkagem das bases
class Paciente(object):
    TEM_CPF : bool
    NU_CPF : str
    NU_CNS : str
    NM_PACIENT : str
    NM_MAE_PAC : str
    DT_NASC : str
    CS_SEXO : int
    CS_RACA : int
    SG_UF_NOT : str
    ID_MUNICIP : str
    NM_LOGRADO : str
    NU_NUMERO : int
    NM_BAIRRO : str
    NM_COMPLEM : str
    
    def __init__(self, TEM_CPF, NU_CPF, TEM_CNS, NU_CNS, NM_PACIENT, NM_MAE_PAC, DT_NASC, CS_SEXO, CS_RACA, SG_UF_NOT, ID_MUNICIP, NM_LOGRADO, NU_NUMERO, NM_BAIRRO, NM_COMPLEM):
        self.TEM_CPF = TEM_CPF
        self.NU_CPF = NU_CPF
        self.TEM_CNS = TEM_CNS
        self.NU_CNS = NU_CNS
        self.NM_PACIENT = NM_PACIENT
        self.NM_MAE_PAC = NM_MAE_PAC
        self.DT_NASC = DT_NASC
        self.CS_SEXO = CS_SEXO
        self.CS_RACA = CS_RACA
        self.SG_UF_NOT = SG_UF_NOT
        self.ID_MUNICIP = ID_MUNICIP
        self.NM_LOGRADO = NM_LOGRADO
        self.NU_NUMERO = NU_NUMERO
        self.NM_BAIRRO = NM_BAIRRO
        self.NM_COMPLEM = NM_COMPLEM
   
    @staticmethod
    def generate_first_name(names, names_p, names_sex, sexo, random_state = np.random.RandomState(0)):
        '''
            Utiliza uma base com os 250 nomes mais frequentes no Brasil e suas
            proporções para gerar um primeiro nome aleatório segundo o sexo do
            paciente.
        '''
        rd = random_state
        if(sexo == 1):
            return rd.choice(names[names_sex == 1], p = names_p[names_sex == 1]/np.sum(names_p[names_sex == 1])).title()
        elif(sexo == 2):
            return rd.choice(names[names_sex == 2], p = names_p[names_sex == 2]/np.sum(names_p[names_sex == 2])).title()
        else:
            return rd.choice(names, p = names_p/np.sum(names_p)).title()

    @staticmethod
    def generate_surname(surnames, p, length = 10, random_state = np.random.RandomState(None)):
        '''
            Utiliza uma base com os 1000 sobrenomes mais frequentes no Brasil para
            gerar um sobrenome aleatório como combinação desses sobrenomes da base.
        '''
        rd = random_state
        return " ".join(rd.choice(surnames, length, p = p, replace = False))
    
    @staticmethod
    def modify_surname(surnames, surnames_p, surname, rd = np.random.RandomState(None)):
        '''
            Recebe o sobrenome e o altera "levemente" de modo a utilizá-lo como
            sobrinome da mãe do paciente.
        '''
        # Substitui da|de|do|das|dos quando se encontram no meio do sobrenome
        surname = surname.replace(" da "," da_").replace(" do "," do_").replace(" das "," das_"). \
                          replace(" dos "," dos_").replace(" de "," de_"). \
                          replace(" Da "," Da_").replace(" Do "," do_").replace(" Das "," das_"). \
                          replace(" Dos "," Dos_").replace(" De "," de_"). \
                          replace("Neto", "").replace("Filho", "").replace("Segundo", "")
        # Substitui da|de|do|das|dos quando se encontram no início do sobrenome
        surname = re.sub(r"(^da) |(^do) |(^de) |(^das) |(^dos) ",
                         r"\g<1>\g<2>\g<3>\g<4>\g<5>_",
                         surname)
        words = np.array(surname.split())
        # Se o sobrenome contém mais de 3 palavras, remove uma amostra de palavras
        if(len(words) > 1):
            # Número de palavras a serem removidas (0 ou 1)
            words_to_remove = rd.binomial(2, p = 0.8)
            # Índices para o sorteio das palavras removidas
            index = np.arange(len(words))
            # Sorteia os índices a serem removidos
            remove_index = rd.choice(index, words_to_remove, replace = False)
            # Remove os índices sorteados
            words = words[list(set(index) - set(remove_index))]

        # Adiciona (ou não) mais nomes para o sobrenome (de 0 a 2)
        words = list(words)
        words.append(Paciente.generate_surname(surnames, surnames_p, rd.binomial(2, 0.2), rd))

        return " ".join(words).strip().replace("_", " ")
        
    
def create_patient(TEM_CPF = None, NU_CPF = None, TEM_CNS = None, NU_CNS = None, 
                   NM_PACIENT = None, NM_MAE_PAC = None,
                   DT_NASC = None, CS_SEXO = None, CS_RACA = None,
                   NU_CEP = None, SG_UF_NOT = None, ID_MUNICIP = None,
                   NM_LOGRADO = None, NU_NUMERO = None, NM_BAIRRO = None, NM_COMPLEM = None,
                   random_state = None, prob_CPF = 0.8, prob_CNS = 0.6):
    
    # --- Carregamento e preparo para geração do primeiro nome... ---
    brazilian_names = pd.read_csv("../../brazilNamesGenderRatio.csv", encoding = "latin1")
    # 250 primeiros nomes mais frequentes no Brasil
    names = brazilian_names.sort_values("total", ascending = False).iloc[:250,:]
    # Calcula as proporções que os nomes aparecem dentre os 250 mais frequentes
    names_p = names.total / np.sum(names.total)
    # Nomes utilizados para pessoas do sexo masculino (1) ou feminino (2)
    names_sex = np.array([1 if(list(names.male)[j] > list(names.female)[j]) else 2 for j in range(names.shape[0])])
    # Toma uma lista np.array com os nomes
    names = names.firstName.to_numpy()

    # --- Carregamento e preparo para a geração do sobrenome... ---
    surnames = pd.read_csv("../../MostCommonSurnames.csv", encoding = "latin1", header = None).iloc[:,1:]
    surnames.columns = ["sobrenome", "frequencia", "proporcao"]

    surnames_prop = []
    for j in range(surnames.shape[0]):
        surnames_prop.append( 1/float(surnames.loc[j,"proporcao"].split(":")[1].replace(",",".")) )
    surnames.proporcao = surnames_prop/np.sum(surnames_prop)
    
    if(random_state is None or type(random_state) == type(int)):
        rd = np.random.RandomState(seed = random_state)
        Faker.seed(random_state)
    else:
        rd = random_state
    
    faker = Faker(["pt-BR"])
    
    
    # Dados para a geração de nomes
    #     É de grande interesse que os nomes gerados satisfaçam minimamente a estrutura
    #     presente nos nomes brasileiros. Assim, usa-se uma base de dados tomada de uma
    #     pesquisa que envolve os nomes mais comuns utilizados por homens e mulheres
    #     brasileiros.
    #     https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/ORH029
    #
    # Para a geração dos sobrenomes procura-se manter um certo padrão entre o nome da mãe
    # e o nome do paciente, mas de modo que não necessariamente os sobrenomes sejam iguais.
    # Foi utilizada a base de https://forebears.io/brazil/surnames
    
    paciente = {}
    paciente["TEM_CPF"] = TEM_CPF
    paciente["NU_CPF"] = NU_CPF
    paciente["TEM_CNS"] = TEM_CPF
    paciente["NU_CNS"] = NU_CNS
    paciente["NM_PACIENT"] = NM_PACIENT
    paciente["NM_MAE_PAC"] = NM_MAE_PAC
    paciente["DT_NASC"] = DT_NASC
    paciente["CS_SEXO"] = CS_SEXO
    paciente["CS_RACA"] = CS_RACA
    paciente["SG_UF_NOT"] = SG_UF_NOT
    paciente["ID_MUNICIP"] = ID_MUNICIP
    paciente["NM_LOGRADO"] = NM_LOGRADO
    paciente["NU_NUMERO"] = NU_NUMERO
    paciente["NM_BAIRRO"] = NM_BAIRRO
    paciente["NM_COMPLEM"] = NM_COMPLEM
    
    if(TEM_CPF is None or TEM_CPF == "auto"):
        # Gera um valor bool com base na probabilidade de um paciente ter cpf
        paciente["TEM_CPF"] = (rd.random() <= prob_CPF)
    if(paciente["TEM_CPF"] and ( NU_CPF is None or NU_CPF == "auto" )):
        paciente["NU_CPF"] = faker.cpf()
    if(TEM_CNS is None or TEM_CNS == "auto"):
        # Gera um valor bool com base na probabilidade de um paciente ter cpf
        paciente["TEM_CNS"] = (rd.random() <= prob_CNS)
    if(paciente["TEM_CNS"] and ( NU_CPF is None or NU_CPF == "auto" )):
        # Gera 15 números aleatoriamente para determinar o número do cartão CNS
        paciente["NU_CNS"] = "".join(rd.choice(list("0123456789"), 15,))
    if(CS_SEXO is None or CS_SEXO == "auto"):
        # Gera 20% de informações não informativas e 80% de um dos dois sexos
        paciente["CS_SEXO"] = rd.choice([1,2,9], p = [0.4 ,0.4, 0.2])
    if(NM_PACIENT is None or NM_PACIENT == "auto"):
        # --- Criação do nome completo ---
        first_name = Paciente.generate_first_name(names, names_p, names_sex, paciente["CS_SEXO"], rd)
        # Permite até 5 sobrenomes, mas tem como média cerca de 2 sobrenomes
        surname = Paciente.generate_surname(surnames.sobrenome, surnames.proporcao, rd.binomial(4, 0.2)+1, rd)
        paciente["NM_PACIENT"] = first_name +" "+ surname
        
    if(NM_MAE_PAC is None or NM_MAE_PAC == "auto"):
        mae_first_name = Paciente.generate_first_name(names, names_p, names_sex, 2, rd)
        paciente["NM_MAE_PAC"] = mae_first_name +" "+ Paciente.modify_surname(surnames.sobrenome, surnames.proporcao, surname, rd)
    if(DT_NASC is None or DT_NASC == "auto"):
        paciente["DT_NASC"] = faker.date_between(start_date = "-95y", end_date = "-10m")
    if(CS_RACA is None or CS_RACA == "auto"):
        # 1: Branca (Prob 0.327)
        # 2: Preta (Prob 0.084)
        # 3: Amarela (Prob 0.006)
        # 4: Parda (Prob 0.378)
        # 5: Indígena (Prob 0.005)
        # 9: Ignorado (Prob 0.20)
        
        paciente["CS_RACA"] = rd.choice([1,2,3,4,5,9], p = [0.327, 0.084, 0.006, 0.378, 0.005, 0.20])
    if(SG_UF_NOT is None or SG_UF_NOT == "auto"):
        # Lê os dados dos municípios brasileiros
        f = open("../../municipios_brasil.txt", "r")
        municipios = []
        UFs = []
        for line in f.readlines():
            municipios.append( line.replace("\n","")[:-5] )
            UFs.append( line[-4:-2] )
        
        j = rd.choice(np.arange(len(municipios)))
        
        paciente["SG_UF_NOT"] = UFs[j]
    if(ID_MUNICIP is None or ID_MUNICIP == "auto"):
        paciente["ID_MUNICIP"] = municipios[j]
    if(NM_LOGRADO is None or NM_LOGRADO == "auto"):
        paciente["NM_LOGRADO"] = faker.street_name()
    if(NU_NUMERO is None or NU_NUMERO == "auto"):
        paciente["NU_NUMERO"] = faker.building_number()
    if(NM_BAIRRO is None or NM_BAIRRO == "auto"):
        paciente["NM_BAIRRO"] = faker.bairro()
    if(NM_COMPLEM is None or NM_COMPLEM == "auto"):
        complemento = rd.choice(["", "apt", "bloco", "casa"], p = [0.55, 0.3, 0.1, 0.05])
        if(complemento == "apt"):
            complemento = "APT "+ str(rd.randint(130))
        elif(complemento == "bloco"):
            complemento = "BLOCO "+ str(rd.randint(16))
        elif(complemento == "casa"):
            complemento = "casa "+ rd.choice(["preta", "amarela", "azul", "verde"])
        paciente["NM_COMPLEM"] = complemento
        
    return paciente