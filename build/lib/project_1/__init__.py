#Project 1 Package
r'''
Projeto 1 do curso de Tratamento de Dados Astronômicos

Author: Ellen Costa de Almeida
email: ellen15@astro.ufrj.br

___

Esse pacote serve para reduzir bias e flat field de dados astronômicos.

Funções:
    -matrix64
    -save_fits
    -master_bias
    -master_flat
    -science

'''
import numpy as np
import glob
from astropy.io import fits


class TUDAO(object):
    r'''Primeiramente leia o arquivo README.md para saber a estrutura de pastas que deve ser OBRIGATORIAMENTE utilizada!
    Entre com o caminho da pasta da noite de observação da seguinte forma:
		Nome da pasta = data
		Entrada da função = /home/ellen15/data/		***não esqueca da barra no final do caminho***
	'''
    def __init__(self, data_path):
        self.data_path = data_path

    def matrix64(self,folder):
        r'''Função para tornar todos os arquivos fits de uma pasta em matrizes float64.
        Exemplo:
                 entrada = matrix64('bias')
                 retorna um master_bias.fits na pasta bias
        '''
        files = np.sort(glob.glob(self.data_path+folder+'/*.fits'))		#lista o caminho de todos os arquivos da pasta
        files_fits = []
        for i in range(len(files)):
			#passa de fits para matriz utilizavel
            matrix = fits.getdata(files[i])
			#passa os dados para float64
            matrix = matrix.astype(np.float64)
			#inclui o a matrix do fits na lista files_fits
            files_fits.append(matrix)
        #retorna TODAS as matrizes dos arquivos fits
        return files_fits

    def save_fits(self,folder,matrix,output):
        r'''Função para salvar uma matriz em arquivo fits na pasta escolhida.
		Exemplo:
		         input = save_fits('bias',matrix_master_bias,'master_bias')
		         retorna um arquivo chamado master_bias.fits na pasta bias
		              -> o arquivo em questão contém os dados da matriz matrix_master_bias
		'''
        hdu = fits.PrimaryHDU()
        hdu.data = matrix
        hdu.writeto(self.data_path+folder+'/'+output+'.fits')


    def master_bias(self,save=True):
        r'''Função para obter o master_bias de uma noite de observação, ou seja, a combinação das medianas de todos os bias da noite.
		Temos duas formas de saida para esta funcao:

		 1 - Retorna o arquivo fits do master_bias
				Exemplo:
				         input = master_bias() ou master_bias(True) -> Como a opção 'True' é default, você pode optar por escrever ou não
				         Retorna um arquivo chamado master_bias.fits na pasta bias

		2 - Retorna a matriz master_bias (matriz utilizada para fazer operações matemáticas com os dados já que tem a forma float64)
		        Exemplo:
		                 input = master_bias(False)
		                 Retorna a matriz master_bias

		A função executa um teste estatístico para saber se o bias está correto, então se a a mediana não estiver perto de 1, aparecerá uma mensagem de erro para que o usuário confira seus arquivos originais de bias e tente novamente.

		OBSERVAÇÃO IMPORTANTE: Se você já tem uma imagem master_bias.fits e deseja refazer o processo com o save==True, não esqueça de excluí-lo antes de continuar para que essa imagem não seja usada na criação do próximo master_bias.fits.
		'''
        bias_median = np.median(self.matrix64('bias'),axis=0)
        #teste estatistico para verificar a confiabilidade do bias, ou seja, se a mediana esta perto de 1
        teste = round(np.median(self.matrix64('bias')),2)
        if (teste < 1.1) or (teste > 0.9):
            if save == True:
                self.save_fits('bias',bias_median,'master_bias')
            else:
                return bias_median
        else:
            print(r'Você é burro, cara. Confere esses bias aí, na moral!')


    def master_flat(self,save=True):
        r'''Função para obter o master_flat de uma noite de observação, ou seja, a combinação das medianas de todos os flats normalizados (flat/sua mediana) da noite de observacao.
		Temos duas formas de saída para esta função:

		 1 - Retorna o arquivo fits do master_flat_field
				Exemplo:
				         input = master_flat() ou master_flat(True) -> Como a opcão 'True' é default, você pode optar por escrever ou não
				         Retorna um arquivo chamado master_flat_field.fits na pasta flat_field

		2 - Retorna a matriz master_flat_field (matriz utilizada para fazer operações matemáticas com os dados já que tem a forma float64)
		        Exemplo:
		                 input = master_flat(False)
		                 Retorna a matriz master_flat_field

		A função executa um teste estatístico para saber se o flat field está correto, então se a a mediana de cada flat individual não estiver perto de 1, aparecerá uma mensagem de erro para que o usuário confira seus arquivos originais de flat field e tente novamente.

		OBSERVAÇÃO IMPORTANTE: Se você já tem uma imagem master_flat.fits e deseja refazer o processo com o save==True, não esqueça de excluí-lo antes de continuar para que essa imagem não seja usada na criação do próximo master_flat.fits.
		'''
		#lista de flats em float64
        flats = self.matrix64('flat_field')
		#lista para adicionar os flats normalizados
        normalized_flats = []
        for i in range(len(flats)):
            median = np.median(flats[i] - self.master_bias(save=False),axis=0)
			#normaliza cada flat
            normal = (flats[i] - self.master_bias(save=False))/median
            #teste estatistico para verificar a confiabilidade do bias, ou seja, se a mediana esta perto de 1
            teste = round(np.median(normal),2)
            if (teste > 0.9) or (teste < 1.1):
                normalized_flats.append(normal)
            else:
                print(r'Como você é burro, cara! Confere esses flats aí, na moral!')
		#cria a mediana de todos os flats normalizados
        ff_median = np.median(normalized_flats,axis=0)
        if save == True:
            self.save_fits('flat_field',ff_median,'master_flat_field')
        else:
            return ff_median

    def science(self):
        r'''Função para obter as imagens de ciência reduzidas do bias e flat.
        Exemplo:
                input = science()
                Retorna todas as imagens de ciência renomeadas para nomeoriginal_red.fits na pasta 'science'.

        Primeiro a função subtrai o master_bias e depois divide pelo master_flat.
        '''
        sci_original_names = files = np.sort(glob.glob(self.data_path+'science/*.fits'))
		#lista de imagens de ciencia em float64
        sci_files = self.matrix64('science')
        #lista de imagens de ciencia sem bias e flat
        sci_final = []
        for i in range(len(sci_files)):
			#reduz o bias da imagem de ciencia
            sci_bias = sci_files[i] - self.master_bias(save=False)
			#reduz o flat da imagem de ciencia
            sci_ff = sci_bias / self.master_flat(save=False)
            hdu = fits.PrimaryHDU()
            hdu.data = sci_ff
			#salva a imagem de ciencia reduzida como nomeoriginal_red.fits
            hdu.writeto(sci_original_names[i][:-5]+'_red.fits')
