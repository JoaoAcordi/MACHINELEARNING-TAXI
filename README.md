
# UniSatc-N3-MachineLearning

Este é um projeto de Machine Learning desenvolvido para a disciplina N3 na UniSatc.

# Passo a Passo para Configurar e Rodar a Aplicação Flask com Frontend HTML

```bash
# 1. Preparar o Ambiente

# Pré-requisitos:
# - Python instalado (versão 3.7 ou superior).
# - Pip (gerenciador de pacotes do Python).
# - Editor de texto/IDE (ex: VS Code).
# - Navegador de internet.

# Instalar o Virtualenv (opcional, mas recomendado):
pip install virtualenv

# 2. Criar o Ambiente Virtual

# Crie um diretório para o projeto:
mkdir taxi-calculator
cd taxi-calculator

# Crie o ambiente virtual:
virtualenv venv

# Ative o ambiente virtual:
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# 3. Instalar as Dependências

# Crie um arquivo requirements.txt com o seguinte conteúdo:
echo "Flask\nflask-cors\npandas" > requirements.txt

# Instale as dependências:
pip install -r requirements.txt

# 4. Preparar o Arquivo CSV

# Certifique-se de que o arquivo `data.csv` está na mesma pasta que o script `app.py`.
# O arquivo deve conter as seguintes colunas:
# - tpep_pickup_datetime
# - tpep_dropoff_datetime

# 7. Rodar o Servidor Flask

# Execute o servidor Flask:
python app.py

# Abra o arquivo HTML no navegador e teste a calculadora.






