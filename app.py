from flask import Flask
from src.routes.network import network_bp

app = Flask(__name__)

# Registrar rutas
app.register_blueprint(network_bp, url_prefix='/network')

if __name__ == '__main__':
    app.run(debug=True)
