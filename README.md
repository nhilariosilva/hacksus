# IntegraSUS
Hackathon de parceria Campus Party e Ministério da Saúde para o projeto Inova Dados.
Encontre mais informações sobre nossa solução em:

### Ana Luiza Martins Cesario, Ludmilla Naud, Natan Hilário da Silva e Nazaré Sampaio.

Link do pitch: https://youtu.be/yRsVfGjhGZM

## Propósito

O IntegraSUS tem o propósito de unificar diferentes bases de dados do SUS de modo a poupar todo o esforço necessário pelos pesquisados do MS da saúde com a construção de bases de dados para suas pesquisas. Atualmente o processo de linkagem de diferentes sistemas do SUS é muito custoso, sendo feito em sua maioria a mão pelos pesquisadores. Esse processo, uma vez levando meses para ser efetuado, pode ser automatizado através de algoritmos de aprendizado de máquina, fazendo com que a linkagem das bases seja extremamento rápida e confiável ao mesmo tempo.

A ideia foi propostas pelas integrantes do grupo Ludmilla e Nazaré, ambas da área de saúde, que sofreram na prática desse problema de falta de unificação dos dados para pesquisa. A construção de um sistema de linkagem de bases não só aumenta a confiança das pesquisas desenvolvidas pelo MS, como também acelera muito toda a linha do caminho da informação.

Obs: Por se tratar de um sistema de linkagem de dados confidenciais do SUS, a plataforma é direcionada para o uso por parte dos funcionários do Ministério da Saúde com a devida autorização para a manipulação desses dados. Os dados reais utilizados para verificar a formatação das variáveis foram pegos em https://opendatasus.saude.gov.br/dataset/srag-2021-e-2022.

## Modelagem

Para o treinamento do modelo, foram usados dados gerados aleatoriamente e linkados de forma metódica. Tem-se uma tabela em que cada linha é uma comparação entre dois indivíduos, sendo cada um de uma base. Assim, se a primeira base de dados tem $n$ e a segunda $m$ indivíduos, é criada uma tabela com $n \times m$ linhas. Como os dados inicialmente são aleatórios tem-se a informação de quais indivíduos são os mesmos. Essa informação (1 se são o mesmo indivíduo, 0 se são diferentes) é usada para o ajuste de um modelo de Regressão Logística, que é feito sobre as variáveis de diferença obtidas entre os pares de indivíduos. A métrica usada para identificar diferença entre os nomes foi a Distância de Leveshtein.

O modelo apresenta a seguinte estrutura
$P(\text{mesmo indivíduo}) = \dfrac{1}{1+\exp(-\eta)}, \ \ \eta = W^t x$

sendo $W$ o vetor de pesos obtido no treinamento do modelo e $x$ o vetor de dados da diferença entre dois indivíduos. P representa a probabilidade associada de uma observação da tabela representar duas vezes o mesmo indivíduo, porém com informação ruidosa.

Os ruídos foram simulados no conjunto de dados, de modo a aproximar de uma aplicação do mundo real. Mesmo com esses ajustes, o modelo foi capaz de obter resultados satisfatórios. Mais informações, além dos códigos são dados na pasta https://github.com/nhilariosilva/hacksus/blob/main/SREG/.

![image](https://user-images.githubusercontent.com/60819864/174445654-3043ba9f-bcc6-48db-a27e-edeacabfc814.png)

A imagem acima representa a probabilidade de todos os pares de observações do conjunto de dados representarem indivíduos iguais. Pontos cujo valor de y são maiores que 50% representam duplas classificadas como sendo o mesmo indivíduo.


