%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import os
from astropy.io import fits


class TUDAO(object):
    '''
    Primeiramente leia o arquivo README.md para saber a estrutura de pastas que deve ser OBRIGATORIAMENTE utilizada!
    Entre com o caminho da pasta da noite de observacao da seguinte forma:
		Nome da pasta = Data
		Entrada da funcao = /home/ellen15/Data/		***nao esqueca da barra no final do caminho***
    
    '''	
	def __init__(self, data_path):
		self.data_path = data_path
		
	def master_bias(self):
		bias_files = glob.glob(data_path+'bias/*.fits')                 #lista com o caminho de todos os arquivos bias da noite
		bias_fits = fits.getdata(bias_files)							#lista com todos os bias da noite
		bias_fits = bias_fits.astype(np.float64)						#passando para float64
		bias_median = np.median(bias_fits)								#cria a mediana de todas as imagens
		hdu = fits.PrimaryHDU()	
		hdu.data = median
		hdu.writeto(data_path+'bias/master_bias.fits')					#salva o master_bias em um arquivo fits
	

	def master_flat(self):
		ff_files = glob.glob(data_path+'flat_field/*.fits')             #lista com o caminho de todos os arquivos bias da noite
		ff_fits = fits.getdata(ff_files)								#lista com todos os bias da noite
		ff_fits = ff_fits.astype(np.float64)							#passando para float64
		ff_median = np.median(ff_fits)									#cria a mediana de todas as imagens
		hdu = fits.PrimaryHDU()	
		hdu.data = median
		hdu.writeto(data_path+'flat_field/master_ff.fits')				#salva o master_bias em um arquivo fits	
		
	def sci_bias(self):
		sci_files = glob.glob(data_path+'science/*.fits')
		sci_bias_files = 	
