from flask import Flask, jsonify, request
from flask_apispec import FlaskApiSpec, doc
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_swagger_ui import get_swaggerui_blueprint

# Instanciación de la aplicación Flask ######################################################################

app = Flask(__name__)

# Ruta /process ##############################################################################################
@app.route('/process', methods=['GET'])
@doc(tags=['process'])
def process():
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    return jsonify({
        "message": f"Recibido param1: {param1} y param2: {param2}"
    })

# Ruta /item ##################################################################################################
# Ruta para manejar el método GET y los parámetros de consulta
@app.route('/item', methods=['GET'])
@doc(tags=['item'])
def get_item():
    param1 = request.args.get('param1')
    param2 = request.args.get('param2')
    return jsonify({
        "message": f"GET recibido param1: {param1} y param2: {param2}"
    })

# Ruta para manejar el método POST con datos en formato JSON
@app.route('/item', methods=['POST'])
@doc(tags=['item'])
def post_item():
    data = request.get_json()
    return jsonify({
        "message": f"POST recibido name: {data.get('name')}, value: {data.get('value')}"
    })

# Ruta para manejar el método PUT con datos en formato JSON
@app.route('/item', methods=['PUT'])
@doc(tags=['item'])
def put_item():
    data = request.get_json()
    return jsonify({
        "message": f"PUT actualizado name: {data.get('name')}, nuevo value: {data.get('value')}"
    })

# Ruta para manejar el método DELETE con datos en formato JSON
@app.route('/item', methods=['DELETE'])
@doc(tags=['item'])
def delete_item():
    data = request.get_json()
    return jsonify({
        "message": f"DELETE eliminado name: {data.get('name')}, value: {data.get('value')}"
    })

# Configuración de la documentación automática usando APISpec #################################################
app.config.update({
    'APISPEC_SPEC': APISpec(
        title="API de muestra",
        version="1.0.0",
        plugins=[MarshmallowPlugin()],
        openapi_version="3.0.2"
    ),
    'APISPEC_SWAGGER_URL': '/swagger.json',  # URL para el JSON de Swagger
})

# Inicializar y registrar la documentación
docs = FlaskApiSpec(app)

# Configuración de la interfaz Swagger UI
SWAGGER_URL = '/swagger-ui'  # URL para acceder a la interfaz de Swagger UI
API_URL = '/swagger.json'  # URL del archivo JSON con la especificación de la API
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

# Registrar el blueprint de Swagger UI en la app Flask
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Ruta para servir el archivo JSON de la especificación Swagger
@app.route('/swagger.json')
def swagger_json():
    return jsonify(docs.spec.to_dict())

# Registrar las vistas de los diferentes métodos para que aparezcan en la documentación
docs.register(process)
docs.register(get_item)
docs.register(post_item)
docs.register(put_item)
docs.register(delete_item)

# Arranque de la aplicación ###########################################################################

if __name__ == '__main__':
    app.run(debug=True)
