from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # Habilita o CORS para todas as rotas

# Altere o caminho para o arquivo CSV conforme necessário
dataset_path = "C:/Users/robso/Documents/data.csv"  # Substitua pelo caminho correto do seu arquivo CSV

try:
    df = pd.read_csv(dataset_path)
    print("Arquivo CSV carregado com sucesso.")
except Exception as e:
    print(f"Erro ao carregar o arquivo CSV: {e}")

# Atualiza os nomes das colunas para corresponder ao dataset
df['start_time'] = pd.to_datetime(df['tpep_pickup_datetime'])  # Nome correto da coluna
df['end_time'] = pd.to_datetime(df['tpep_dropoff_datetime'])  # Nome correto da coluna

# Função para calcular o tempo decorrido da viagem
df['trip_duration'] = df['end_time'] - df['start_time']

# Função para calcular o preço estimado da viagem (sem considerar a distância)
def calculate_taxi_fare_based_on_time(duration, base_fare=3, rate_per_minute=0.2):
    """
    Calcula o preço da corrida de táxi com base no tempo.
    :param duration: Tempo decorrido da viagem (em segundos).
    :param base_fare: Tarifa base.
    :param rate_per_minute: Tarifa por minuto de viagem.
    :return: Preço total da corrida.
    """
    # Converte a duração de segundos para minutos
    trip_minutes = duration.total_seconds() / 60
    return base_fare + (trip_minutes * rate_per_minute)

# Função para processar o cálculo de preço e tempo baseado nos dados recebidos
def process_trip_data(start_time_input, end_time_input):
    try:
        # Conversão dos horários para datetime
        start_time = pd.to_datetime(start_time_input)
        end_time = pd.to_datetime(end_time_input)

        # Calcular tempo decorrido
        if end_time < start_time:
            raise ValueError("O horário de término não pode ser anterior ao horário de início.")
        trip_duration = end_time - start_time

        # Calcular preço com base apenas no tempo
        fare = calculate_taxi_fare_based_on_time(trip_duration)

        return {
            'trip_duration': str(trip_duration),
            'fare_estimate': round(fare, 2)
        }
    except ValueError as e:
        return {'error': str(e)}

@app.route('/calculate', methods=['POST'])
def calculate_trip():
    data = request.get_json()
    
    # Extrair os tempos de início e fim do corpo da requisição
    start_time_input = data.get('start_time')
    end_time_input = data.get('end_time')
    
    # Processar a viagem e calcular tempo e preço
    result = process_trip_data(start_time_input, end_time_input)
    
    # Retornar os resultados como JSON
    return jsonify(result)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'API para calcular preço e duração de corridas de táxi'})

if __name__ == '__main__':
    app.run(debug=True)
