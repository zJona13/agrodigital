from flask import Flask
from routes.sesion import ws_sesion
from routes.agricultor import ws_agricultor
from routes.actividad import ws_actividad
from routes.actividad_tipo import ws_actividad_tipo
from routes.parcela import ws_parcela
from routes.cultivo import ws_cultivo

app = Flask(__name__)
app.register_blueprint(ws_sesion)
app.register_blueprint(ws_agricultor)
app.register_blueprint(ws_actividad)
app.register_blueprint(ws_actividad_tipo)
app.register_blueprint(ws_parcela)
app.register_blueprint(ws_cultivo)

@app.route('/')
def home():
    return 'AgroDigital - Running API Restful'

#@app.route('/agricultores')
#def agricultores():
#    return 'lista de agricultores'

#Iniciar el servicio web con Flask
if __name__ == '__main__':
    app.run(port=3008, debug=True, host='0.0.0.0')
