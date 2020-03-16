from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd

# Obtém a URL
def getUrl(paginacao):
	'''
	Obtém a URL que abriga os anúncios analisados

	param int paginacao: O número da paginação
	'''
	return "https://sp.olx.com.br/grande-campinas/autos-e-pecas/motos?o="+str(paginacao)

def dictToCsv(item_dic):
	'''	
	Coloca o conjunto de daodos no formato correto e o salva em um arquivo '.csv'
	
	param dara_frame item_dic: O conjunto de dados contendo todos os anúncios
	'''
	csv = []
	print(item_dic)
	# Salvando os itens em um csv
	for i in range(len(item_dic)):
		csv.append([])

		if 'Categoria' in item_dic[i]:
			csv[i].append(item_dic[i]['Categoria'])
		else:
			csv[i].append(float('NaN'))

		if 'Modelo' in item_dic[i]:
			csv[i].append(item_dic[i]['Modelo'])
		else:
			csv[i].append(float('NaN'))

		if 'Cilindrada' in item_dic[i]:
			csv[i].append(item_dic[i]['Cilindrada'])
		else:
			csv[i].append(float('NaN'))	

		if 'Quilometragem' in item_dic[i]:
			csv[i].append(item_dic[i]['Quilometragem'])
		else:
			csv[i].append(float('NaN'))

		if 'Ano' in item_dic[i]:
			csv[i].append(item_dic[i]['Ano'])
		else:
			csv[i].append(float('NaN'))

		if 'url' in item_dic[i]:
			csv[i].append(item_dic[i]['url'])
		else:
			csv[i].append(float('NaN'))

		if 'preco' in item_dic[i]:
			csv[i].append(item_dic[i]['preco'])
		else:
			csv[i].append(float('NaN'))			

	header = ['categoria', 'modelo', 'cilindrada', 'quilometragem', 'ano', 'url', 'preco']
	pd.DataFrame(csv).to_csv('olx_data2.csv', header=header, index=False)


def getInformation():
	print("Obtendo os dados")

	chrome = webdriver.Chrome()
	# Percorre a paginação da categoria para obter os links de todos os anúncios
	url_list = []
	for i in (range(1, 100)):

		# Obtem a página da categoria na paginação i
		chrome.get(getUrl(i))

		itens = chrome.find_elements_by_class_name('OLXad-list-link ')
		
		for item in itens:
			item_link = item.get_attribute('href')
			url_list.append(item_link)


	"""
	* Agora que temos todas as URLS dos anúncios, vamos acessar cada um individualmente e obter as 
	* informações que serão analisadas.
	"""
	item_dic = {}
	item_index = 0
	for i, url in enumerate(url_list):	

		# Verifica se a palavra 'olx.com.br' existe no 'item', para prevenir propaganda
		if "olx.com.br" not in url:
			continue

		chrome.get(url)

		try:
			preco = chrome.find_elements_by_xpath("//*[@class='sc-bZQynM sc-1wimjbb-0 dSAaHC']")[0].get_attribute('textContent')
			preco = preco[3:]
			preco = int(preco.replace('.', ''))
		except:
			print("Preço inexistente")
			preco = float('NaN')

		# Obtém os títulos dos campos
		valores_textuais = chrome.find_elements_by_xpath("//*[@class='sc-bZQynM sc-1f2ug0x-0 iwOlty']")

		# Obtém os valores de 'Categoria', 'Modelo', 'Ano' e 'Quilometragem'
		valores_reais = chrome.find_elements_by_xpath("//*[@class='sc-57pm5w-0 sc-1f2ug0x-2 dBeEuJ' or @class='sc-bZQynM sc-1f2ug0x-1 dPJyDS']")

		item_dic[item_index] = {}
		for j in range(5):
			try:
				# Os campos podem não vir em ordem ou se que existirem, então vamos colocar todos os dados em 'item_dict' e depois passar tudo para csv
				item_dic[item_index][valores_textuais[j].get_attribute('textContent')] = valores_reais[j].get_attribute('textContent')
			except:
				print("Erro")
				print(item_dic)
				print(valores_reais)

		# Insere a URL nos atributos do anúncio para futuras inspeções manuais
		item_dic[item_index]['url'] = url
		item_dic[item_index]['preco'] = preco


		item_index += 1
		

	print(len(item_dic))
	dictToCsv(item_dic)

	#np.save('dataset.npy', item_dic)
	chrome.quit()



if __name__ == '__main__':
	getInformation()
