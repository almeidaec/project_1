#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import os
from astropy.io import fits
from numba import jit


class TUDAO(object):
    '''
    Primeiramente leia o arquivo README.md para saber a estrutura de pastas que deve ser OBRIGATORIAMENTE utilizada!
    Entre com o caminho da pasta da noite de observacao da seguinte forma:
		Nome da pasta = Data
		Entrada da funcao = /home/ellen15/Data/		***nao esqueca da barra no final do caminho***
            
    '''
    @jit	
    def __init__(self, data_path):
		self.data_path = data_path
	
	@jit
    def matrix64(self,folder):
        '''Funcao para tornar todos os arquivos fits de uma pasta em matrizes float64. Exemplo: '''									
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
		
	@jit	
    def save_fits(self,folder,matrix,output):
        hdu = fits.PrimaryHDU()
        hdu.data = matrix
        hdu.writeto(self.data_path+folder+'/'+output+'.fits')	
			
		
    def master_bias(self,save=True):
        bias_median = np.median(self.matrix64('bias'),axis=0)
        #teste estatistico para verificar a confiabilidade do bias, ou seja, se a mediana esta perto de 1
        teste = round(np.median(self.matrix64('bias')),2)
        if (teste < 1.1) or (teste > 0.9):
			if save == True:
				self.save_fits('bias',bias_median,'master_bias')
			else:
				return bias_median	
        else:
            print('Voce e burro, cara.')    			                             
	
	
    def master_flat(self,save=True):
		#lista de flats em float64
		flats = self.matrix64('flat_field')
		#lista para adicionar os flats normalizados
		normalized_flats = []
		for i in range(len(flats)):
			median = np.median(flats[i] - self.master_bias(False),axis=0)
			#normaliza cada flat
			normal = flats[i]/median
			normalized_flats.append(normal)
		#cria a mediana de todos os flats normalizados
		ff_median = np.median(normalized_flats,axis=0)
        #teste estatistico para verificar a confiabilidade do bias, ou seja, se a mediana esta perto de 1
		teste = round(np.median(normalized_flats),2)
		if (teste < 0.9) or (teste > 1.1):
			if save == True:
				self.save_fits('flat_field',ff_median,'master_flat_field')
			else:
				return ff_median	
		else:
			print('Como voce e burro, cara.')
	
		
    def science(self):
		sci_original_names = files = np.sort(glob.glob(self.data_path+'data/*.fits'))
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
			
		 	
