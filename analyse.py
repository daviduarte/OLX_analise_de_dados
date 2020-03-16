import numpy as np
import pandas as pd
import matplotlib as mpl 
## agg backend is used to create plot as a .png file
mpl.use('agg')
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

def cilindradaXpreco(data, modelo=None):	

	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['modelo'].replace('', np.nan, inplace=True)
	data['modelo'].replace(' ', np.nan, inplace=True)

	data['cilindrada'].replace('', np.nan, inplace=True)
	data['cilindrada'].replace(' ', np.nan, inplace=True)
	data['cilindrada'].replace('0', np.nan, inplace=True)

	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['preco'].replace('', np.nan, inplace=True)
	data['preco'].replace(' ', np.nan, inplace=True)
	#print('--'+data['modelo'][0]+'--')

	# Retira motos acima de 1000 cilindradas pois não temos a informação precisa
	# TODO: Verificar a cilindrada atrvés de outras informações, como título, modelo e descrição do anúncio
	data['cilindrada'] = data['cilindrada'].replace('Acima de 1.000', np.nan)

	# Exclui todas as linhas em que possuam NaN nas colunas 'preco' e modelo
	data.dropna(subset=['preco', 'modelo', 'cilindrada'], inplace=True)

	if modelo != None:
		# Seleciona as motos com o modelo definido por 'modelo'
		data = data.loc[data['modelo'] == modelo]

	# Tratar outliers
	# TODO: Implementar um método de detecção de outliers mais eficaz
	#data = data[data['ano'] < 200000]
	#data = data[data['ano'] > 0]

	# Plota as 
	fig, ax = plt.subplots()

	cilindrada = data['cilindrada'].astype('int', copy=True)
	preco = data['preco']

	ax.scatter(cilindrada, preco, s=30)
	
	if modelo == None:
		ax.set(xlabel='Cilindrada', ylabel='Preço',
    		   title='Cilindrada x Preço (todos os modelos)')	
	else:
		ax.set(xlabel='Quilometragem', ylabel='Preço',
    		   title='Quilometragem x Preço ('+modelo+')')	
	ax.grid()

	fig.savefig("cilindradaXpreco.png")
	plt.show()


def quilometragemXpreco(data, modelo):		
	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['modelo'].replace('', np.nan, inplace=True)
	data['modelo'].replace(' ', np.nan, inplace=True)

	data['quilometragem'].replace('', np.nan, inplace=True)
	data['quilometragem'].replace(' ', np.nan, inplace=True)
	data['quilometragem'].replace('0', np.nan, inplace=True)

	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['preco'].replace('', np.nan, inplace=True)
	data['preco'].replace(' ', np.nan, inplace=True)
	#print('--'+data['modelo'][0]+'--')


	# Exclui todas as linhas em que possuam NaN nas colunas 'preco' e modelo
	data.dropna(subset=['preco', 'modelo', 'quilometragem'], inplace=True)

	# Seleciona as motos com o modelo definido por 'modelo'
	data = data.loc[data['modelo'] == modelo]

	# Tratar outliers
	# TODO: Implementar um método de detecção de outliers mais eficaz
	data = data[data['quilometragem'] < 200000]
	data = data[data['quilometragem'] > 0]


	# Plota as 
	fig, ax = plt.subplots()

	quilometragem = data['quilometragem'].astype('int', copy=True)
	preco = data['preco']

	ax.scatter(quilometragem, preco)
	
	ax.set(xlabel='Quilometragem', ylabel='Preço',
    	   title='Quilometragem x Preço ('+modelo+')')	
	ax.grid()

	fig.savefig("quilometragemXpreco.png")
	plt.show()	


def anoXpreco(data, modelo):		
	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['modelo'].replace('', np.nan, inplace=True)
	data['modelo'].replace(' ', np.nan, inplace=True)

	data['ano'].replace('', np.nan, inplace=True)
	data['ano'].replace(' ', np.nan, inplace=True)
	data['ano'].replace('0', np.nan, inplace=True)

	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['preco'].replace('', np.nan, inplace=True)
	data['preco'].replace(' ', np.nan, inplace=True)
	#print('--'+data['modelo'][0]+'--')


	# Exclui todas as linhas em que possuam NaN nas colunas 'preco' e modelo
	data.dropna(subset=['preco', 'modelo', 'ano'], inplace=True)

	# Seleciona as motos com o modelo definido por 'modelo'
	data = data.loc[data['modelo'] == modelo]

	# Tratar outliers
	# TODO: Implementar um método de detecção de outliers mais eficaz
	#data = data[data['ano'] < 200000]
	#data = data[data['ano'] > 0]

	fig, ax = plt.subplots()

	ano = data['ano'].astype('int', copy=True)
	preco = data['preco']

	ax.scatter(ano, preco)
	
	ax.set(xlabel='Ano', ylabel='Preço',
    	   title='Ano x Preço ('+modelo+')')	
	ax.grid()

	fig.savefig("anoXpreco.png")
	plt.show()	



"""

Constrói gráficos do tipo boxplot levando em consideração os modelos x preços e salva como .png
@param data dataframe contendo os dados
@param numModelos quantidade de boxplots na imagem.
@return none

"""
def modeloXpreco(data, numModelos):

	# Substitui as strings vazias por NaN, para que depois possamos eliminá-las
	data['modelo'].replace('', np.nan, inplace=True)
	data['modelo'].replace(' ', np.nan, inplace=True)
	#print('--'+data['modelo'][0]+'--')

	# Exclui todas as linhas em que possuam NaN nas colunas 'preco' e modelo
	data.dropna(subset=['preco', 'modelo'], inplace=True)

	
	# Percorre os valores únicos de modelos de motos
	modelNames = []
	modelPrices = []
	for modelo in data.modelo.unique():

		modelNames.append(modelo)

		# Obtém todos os preços das motos que são deste modelo
		precos = data.loc[data['modelo'] == modelo]['preco'].tolist()
		modelPrices.append(precos)


	# Ordena as categorias por quantidade de motos
	newModelNames = []
	newModelPrices = []
	indexCount = []
	for index, item in enumerate(modelPrices):
		maior = float('-Inf')
		indexMaior = 0
		for index2, item2 in enumerate(modelPrices):
			size = len(item2)
			if size > maior:
				maior = size
				indexMaior = index2

		newModelNames.append(modelNames[indexMaior])
		newModelPrices.append(modelPrices[indexMaior])
		del modelNames[indexMaior]
		del modelPrices[indexMaior]

	#print(modelNames)

	# Cria uma instância de figura. A largura da imagem é relacionada ao número de boxplots
	fig = plt.figure(1, figsize=(numModelos*4, 6))

	# Cria uma instância de eixos
	ax = fig.add_subplot(111)	

	# Cria o boxplot
	bp = ax.boxplot(newModelPrices[:numModelos])

	ax.set_xticklabels(newModelNames[:numModelos])
	
	# Salva a Figura
	fig.savefig('vish.png', bbox_inches='tight')


def regressao(data, modelo=None):

	if modelo != None:
		data = data.loc[data['modelo'] == modelo]
		# Se estvermos analisando apenas 1 modelo, a coluna 'modelo' se torna inútil
		data = data.drop(['modelo'], axis=1)
	
	data = data[data['quilometragem'] < 100000]
	data = data[data['quilometragem'] > 0]

	data_com_urls = data
	# remove as URLs
	data = data.drop(['url'], axis=1)

	data = pd.get_dummies(data)
	# Coluna inútil
	data = data.drop(['categoria_Motos'], axis=1)
	preco = np.asarray(data['preco'])
	quilometragem = data['quilometragem']
	
	print("\nVariáveis: ")
	print(list(data))

	X = np.column_stack((np.ones(data['quilometragem'].shape[0]),
						data['quilometragem'],
						data['cilindrada_250'],
						data['cilindrada_300'],
						data['ano_2009'],
						data['ano_2010'],
						data['ano_2011'],
						data['ano_2012'],
						data['ano_2013'],
						data['ano_2014'],
						data['ano_2015']
	))

	#print(preco)
	model = sm.OLS(data['preco'], X)
	results = model.fit()

	fig, ax = plt.subplots(figsize=(8,6))
	ax.plot(data['quilometragem'], data['preco'], 'o', label="data")
	#ax.plot(data['quilometragem'], results.fittedvalues, 'r--.', label="OLS")
	
	data_com_urls = data_com_urls.assign(diferenca_de_preco=pd.Series(np.zeros(len(data_com_urls['preco']))-1).values)	

	#print(list(data_com_urls))

	y = []
	for index, row in data.iterrows():

		x = [row[1],
			row[2],
			row[3],
			row[4],
			row[5],
			row[6],
			row[7],
			row[8],
			row[9],
			row[10]]
		preco_predito = modelo_linear(x, results)
		# Calcula PREÇO REAL - PREÇO PREDITO
		diferenca_de_preco = row['preco'] - preco_predito
		data_com_urls.at[index, 'diferenca_de_preco'] = diferenca_de_preco
		#print("Diferença de preço:")
		#print(diferenca_de_preco)

		y.append(modelo_linear(x, results))
	
	print(data_com_urls)
	ax.plot(data['quilometragem'], y, 'r--.', label="OLS")
	#fig.savefig("vish.png")
	#ax.savefig('vish.png', bbox_inches='tight')

	# Exibe os resultados ordenados pela coluna "diferenca_de_preco" de ordem crescente.
	# Os valores menores são os anúncios mais baratos, em relação ao preço predito
	data_com_urls.sort_values('diferenca_de_preco', ascending=True, inplace=True)
	data_com_urls.to_csv("vaisefuderporra.txt")

def modelo_linear(x, results):
	y = 0
	params = list(results.params)

	# O vetor x tem 1 elemento a menos. Portanto, devemos somar o coeficiente livre da função após o looping
	for i in range(len(x)):
		y += x[i]*params[i+1]

	# Somando o coeficiente livre
	y += params[0]

	return y

def analytic():
	print("Analisando os dados")

	# Carregando os dados
	data = pd.read_csv('olx_data2.csv')
	data = data[data.modelo != 'HONDA ']
	# Retira todos as linhas contendo modelo = 'HONDA'

#	data = data[data.modelo != 'HONDA ']
#	data = data[data.modelo == 'HONDA CB 300R/ 300R FLEX']
#	data.sort_values('preco', ascending=False, inplace=True)

	# Vamos gerar os gráficos
	modeloXpreco(data, 4)
	anoXpreco(data, 'HONDA CB 300R/ 300R FLEX')
	quilometragemXpreco(data, 'HONDA CB 300R/ 300R FLEX')
	cilindradaXpreco(data)

	# Vamos fazer a regressão
	#regressao(data, modelo='HONDA CB 300R/ 300R FLEX')
	regressao(data, modelo='HONDA CB 300R/ 300R FLEX')


if __name__ == '__main__':
	#getInformation()
	analytic()


