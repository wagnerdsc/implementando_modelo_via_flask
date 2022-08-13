from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle

""""
import pandas as pd
from sklearn.model_selection import train_test_split
"""

modelo = pickle.load(open('modelo.sav','rb'))

colunas = ['tamanho','ano','garagem']

""""
df = pd.read_csv('casas.csv')

colunas = ['tamanho','ano','garagem']

# df = df[colunas]

X = df.drop('preco',axis = 1)
y = df['preco']

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3, random_state=42)

modelo = LinearRegression()
modelo.fit(X_train, y_train)
"""

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'julio'
app.config['BASIC_AUTH_PASSWORD'] = 'alura'

basic_auth = BasicAuth(app)

@app.route('/')
def home():
    return "Minha primeira API"

@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(from_lang='pt-br', to="en")
    polaridade = tb_en.sentiment.polarity
    return "polaridade: {}".format(polaridade)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])

app.run(debug=True)