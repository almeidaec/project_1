Projeto 1 do curso de Tratamento de Dados Astronômicos
Autora: Ellen Costa de Almeida
email: ellen15@astro.ufrj.br

$Pacotes necessários:
  -numpy
  -glob
  -astropy.io

$Instalação:
-Rode o comando 'python setup.py install' no mesmo diretório que se encontra o arquivo setup.py
-Entre no ipython ou no jupyter
-Importe o pacote como 'import project_1 as projeto' (ou qualquer nome que o usuário queira)
-Como o script foi feito utilizando classes, precisaremos executá-lo da seguinte forma:
    -Crie uma variável contendo o caminho da pasta com os dados da observação como entrada da classe da redução
    Ex: x = projeto.TUDAO('/home2/ellen15/Downloads/data/')

$Estrutura de pastas:
O pacote utiliza uma estrutura de pastas muito simples para fazer a redução.
-data             -> Pasta principal contendo todos os arquivos de bias, flat e ciência
  -bias           -> Pasta contendo APENAS os fits de bias
  -flat_field     -> Pasta contendo APENAS os fits de flat field
  -science        -> Pasta contendo APENAS os fits de ciência
  -red            -> Pasta que será utilizada para salvar todas as imagens reduzidas (master_flat, master_bias e science_red)
Então, antes de rodar qualquer função, crie as pastas citadas acima.

$Executando as funções:
-O projeto foi estruturado em 5 funções:
      -matrix64
      -save_fits
      -master_bias
      -master_flat
      -science

-Para rodar qualquer uma das funções acima, o usuário deve prosseguir da seguinte forma:
Ex. 'x.master_bias()' para executar a função master_bias
Para mais informações, todas as funções têm informações adicionais. Basta executar o comando help(x.nomedafunção) para saber mais.

$Observações importantes:
      
