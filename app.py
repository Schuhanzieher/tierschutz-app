from flask import Flask
from config import Config
from models import db, STATUS_MAP


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Template-Filter
    @app.template_filter("status_emoji")
    def status_emoji_filter(status_code):
        return STATUS_MAP.get(status_code, {}).get("emoji", "?")

    @app.template_filter("status_label")
    def status_label_filter(status_code):
        return STATUS_MAP.get(status_code, {}).get("label", "unbekannt")

    @app.template_filter("status_css")
    def status_css_filter(status_code):
        return STATUS_MAP.get(status_code, {}).get("css_class", "")

    @app.template_filter("datum")
    def datum_filter(d):
        if d is None:
            return "\u2014"
        return d.strftime("%d.%m.%Y")

    # Routen registrieren
    from routes import register_routes
    register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5001)
