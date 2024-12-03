from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

app = Flask(__name__)
CORS(app)  # Habilita o CORS para todas as rotas

# Carregar o dataset
dataset_path = "data.csv"  # Certifique-se de que o arquivo está no local correto
df = pd.read_csv(dataset_path)

# Exibir as primeiras linhas para verificar as colunas
print("Visualizando as primeiras linhas do dataset:")
print(df.head())

# Atualizar os nomes das colunas para corresponder ao dataset
df['start_time'] = pd.to_datetime(df['tpep_pickup_datetime'])  # Nome correto da coluna
df['end_time'] = pd.to_datetime(df['tpep_dropoff_datetime'])  # Nome correto da coluna

# Calcular o tempo decorrido da viagem
df['trip_duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60  # Convertido para minutos

# Filtrar viagens com distância maior que 0
df = df[df['trip_distance'] > 0]

# Adicionar uma função para calcular o preço estimado da viagem
def calculate_taxi_fare(distance, rate_per_km=2.5, base_fare=3):
    """
    Calcula o preço da corrida de táxi com base na distância.
    :param distance: Distância percorrida em quilômetros.
    :param rate_per_km: Tarifa por quilômetro.
    :param base_fare: Tarifa base.
    :return: Preço total da corrida.
    """
    return base_fare + (distance * rate_per_km)

# Adicionar a coluna com o preço estimado
df['fare_estimate'] = df['trip_distance'].apply(calculate_taxi_fare)

# Selecionar as features e o target
X = df[['trip_distance', 'trip_duration']]
y = df['fare_estimate']

# Dividir os dados em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelagem: Regressão Linear
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

# Predições: Regressão Linear
y_pred_linear = linear_model.predict(X_test)

# Avaliação: Regressão Linear
print("\nRegressão Linear:")
print(f"RMSE: {mean_squared_error(y_test, y_pred_linear, squared=False):.2f}")
print(f"R²: {r2_score(y_test, y_pred_linear):.2f}")

# Modelagem: Árvore de Decisão
tree_model = DecisionTreeRegressor(random_state=42)
tree_model.fit(X_train, y_train)

# Predições: Árvore de Decisão
y_pred_tree = tree_model.predict(X_test)

# Avaliação: Árvore de Decisão
print("\nÁrvore de Decisão:")
print(f"RMSE: {mean_squared_error(y_test, y_pred_tree, squared=False):.2f}")
print(f"R²: {r2_score(y_test, y_pred_tree):.2f}")

@app.route('/calculate', methods=['POST'])
def calculate_trip():
    """
    Recebe os dados de distância e duração, faz a previsão usando Regressão Linear e Árvore de Decisão
    e retorna o preço estimado por ambos os modelos.
    """
    data = request.get_json()

    # Extrair distância e duração da viagem do corpo da requisição
    distance = data.get('trip_distance')
    trip_duration = data.get('trip_duration')

    if distance is None or trip_duration is None:
        return jsonify({'error': 'Os dados de distância e duração são obrigatórios!'}), 400

    # Criar um dataframe para entrada
    user_input = pd.DataFrame([[distance, trip_duration]], columns=['trip_distance', 'trip_duration'])

    # Predição usando Regressão Linear
    fare_linear = linear_model.predict(user_input)[0]

    # Predição usando Árvore de Decisão
    fare_tree = tree_model.predict(user_input)[0]

    return jsonify({
        'fare_linear': round(fare_linear, 2),
        'fare_tree': round(fare_tree, 2)
    })

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'API para calcular preço e duração de corridas de táxi usando modelos de Regressão Linear e Árvore de Decisão'})

if __name__ == '__main__':
    app.run(debug=True)
