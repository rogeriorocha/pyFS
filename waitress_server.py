from waitress import serve
import application
serve(application.create_app(), host='0.0.0.0', port=5000)