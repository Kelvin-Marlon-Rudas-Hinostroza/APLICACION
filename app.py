from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Cargar y preprocesar datos
data = pd.read_csv('mejorados_resumenes.csv')
texts = data['texto'].tolist()
summaries = data['resumen'].tolist()

# Preprocesar los datos
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts).toarray()

# Crear etiquetas numéricas para los resúmenes
y_labels = np.array([summaries.index(summary) for summary in summaries])

# Definir el modelo con más capas ocultas
model = keras.Sequential([
    layers.Input(shape=(X.shape[1],)),  # Capa de entrada
    layers.Dense(128, activation='relu'),  # Capa oculta 1
    layers.Dense(64, activation='relu'),   # Capa oculta 2
    layers.Dense(32, activation='relu'),   # Capa oculta 3
    layers.Dense(len(set(summaries)), activation='softmax')  # Capa de salida para múltiples resúmenes
])

# Compilar el modelo
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
model.fit(X, y_labels, epochs=50, batch_size=32)  # Aumentar el número de épocas a 50

def resumir_texto(texto):
    texto_transformado = vectorizer.transform([texto]).toarray()
    prediccion = model.predict(texto_transformado)
    resumen_index = np.argmax(prediccion[0])
    resumen = summaries[resumen_index]
    return resumen

# Ruta principal: index.html
@app.route('/')
def home():
    return render_template('index.html')

# Nueva ruta: principal.html
@app.route('/principal.html')
def principal():
    return render_template('principal.html')   

# Ruta para procesar el resumen
@app.route('/resumir', methods=['POST'])
def resumir():
    try:
        texto = request.json['texto']
        resumen = resumir_texto(texto)
        return jsonify({'resumen': resumen})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
