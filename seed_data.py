"""
Seed-Skript: Fuellt die Datenbank mit den Kontaktdaten.
Funktioniert ueberall (lokal + PythonAnywhere).

Aufruf:
    python3 seed_data.py
"""

from app import create_app
from models import db, Contact

CONTACTS = [
    {"kategorie": "NGO / Tierschutz", "name_organisation": "Pfotenherz", "kontaktperson": "Jenny", "rolle": "Tierschutzpartner", "status": "gruen", "kontaktweg": "Mail / WhatsApp", "naechster_schritt": "Austausch vertiefen", "zustaendig": "Daniel", "notizen": "sehr empathisch"},
    {"kategorie": "NGO / Tierschutz", "name_organisation": "vegan.bullerbyn e. V.", "rolle": "Bildung & Gemeinschaft", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "Austausch halten", "zustaendig": "Daniel"},
    {"kategorie": "NGO / Tierschutz", "name_organisation": "tierschutz.familie", "rolle": "Community-nah", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "Beteiligung klaeren", "zustaendig": "Daniel"},
    {"kategorie": "NGO / Tierschutz", "name_organisation": "die_tierschutz.familie", "rolle": "Community-nah", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "weiterer Austausch", "zustaendig": "Daniel"},
    {"kategorie": "NGO / Tierschutz", "name_organisation": "Tierschutzhof_heile_seele", "rolle": "Hof & Bildung", "status": "gelb", "kontaktweg": "DM", "naechster_schritt": "Rueckmeldung abwarten", "zustaendig": "Daniel"},
    {"kategorie": "NGO / Tierschutz", "name_organisation": "ANINOVA Stiftung", "rolle": "Investigativ", "status": "gruen", "kontaktweg": "Mail / DM", "naechster_schritt": "Kooperation klaeren", "zustaendig": "Daniel"},
    {"kategorie": "NGO / Tierschutz", "name_organisation": "PETA Deutschland", "rolle": "Reichweite", "status": "gelb", "kontaktweg": "Mail", "naechster_schritt": "Follow-up", "zustaendig": "Daniel"},
    {"kategorie": "NGO / Tierschutz", "name_organisation": "WWF Deutschland", "rolle": "Langfristig", "status": "gelb", "kontaktweg": "intern", "naechster_schritt": "interne Pruefung", "zustaendig": "Daniel"},
    {"kategorie": "NGO / Tierschutz", "name_organisation": "av_frankfurt", "rolle": "Aktivismus", "status": "gelb", "kontaktweg": "DM", "naechster_schritt": "Kontakt vertiefen", "zustaendig": "Daniel"},
    {"kategorie": "Musik / Kultur", "name_organisation": "Unwahr Satzaffe", "rolle": "Live-Act Hip-Hop", "status": "gruen", "kontaktweg": "direkt", "naechster_schritt": "Details spaeter", "zustaendig": "Daniel"},
    {"kategorie": "Musik / Kultur", "name_organisation": "ISDI (Ostintakt)", "rolle": "Live-Act Hip-Hop", "status": "gruen", "kontaktweg": "direkt", "naechster_schritt": "locker halten", "zustaendig": "Daniel"},
    {"kategorie": "Musik / Kultur", "name_organisation": "Ronja (ronjasmusik)", "kontaktperson": "Ronja", "rolle": "Singer-Songwriter", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "im Gespraech", "zustaendig": "Daniel"},
    {"kategorie": "Bildung / Speaker", "name_organisation": "Henri Sarafov", "kontaktperson": "Henri", "rolle": "Veganismus & Aufklaerung", "status": "gruen", "kontaktweg": "direkt", "naechster_schritt": "Format entwickeln", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "Loewensweets", "rolle": "vegane Suessigkeiten", "status": "gruen", "kontaktweg": "direkt", "naechster_schritt": "Einbindung klaeren", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "vanessawinkler.foodstudio", "rolle": "Food & Aesthetik", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "Rolle klaeren", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "vegglyapp", "rolle": "App / Community", "status": "gelb", "kontaktweg": "DM", "naechster_schritt": "spaeter aufnehmen", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "leinlecker_vegan4dogs", "rolle": "Tierfutter Hunde", "status": "gelb", "kontaktweg": "DM", "naechster_schritt": "Austausch fortsetzen", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "vegdog_food", "rolle": "Tierfutter", "status": "gelb", "kontaktweg": "DM", "naechster_schritt": "spaeter", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "GREENFORCE", "rolle": "Food", "status": "gelb", "kontaktweg": "Mail", "naechster_schritt": "langfristig", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "otopia", "rolle": "Food", "status": "gelb", "kontaktweg": "DM", "naechster_schritt": "abwarten", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "REWE voll pflanzlich", "rolle": "Handel", "status": "gelb", "kontaktweg": "Mail", "naechster_schritt": "keine Eile", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "veeze.de", "rolle": "Plattform", "status": "gelb", "kontaktweg": "Mail", "naechster_schritt": "Kontakt halten", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "Vutter!", "rolle": "Tierfutter", "status": "rot", "kontaktweg": "Mail", "naechster_schritt": "pausiert", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "Zuger plant-based", "rolle": "Food", "status": "rot", "kontaktweg": "Mail", "naechster_schritt": "bewusst entschieden", "zustaendig": "Daniel"},
    {"kategorie": "Unternehmen", "name_organisation": "Zucker&Jagdwurst", "rolle": "Food & Medien", "status": "gelb", "kontaktweg": "Mail", "naechster_schritt": "Wiedervorlage 2027", "zustaendig": "Daniel"},
    {"kategorie": "Community", "name_organisation": "happy.eco.living", "rolle": "Kernteam", "status": "gruen", "kontaktweg": "direkt", "naechster_schritt": "laufend", "zustaendig": "Daniel"},
    {"kategorie": "Community", "name_organisation": "vegan_veteran", "rolle": "Multiplikator", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "informell", "zustaendig": "Daniel"},
    {"kategorie": "Community", "name_organisation": "veganelli269", "rolle": "Aktivismus", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "Austausch", "zustaendig": "Daniel"},
    {"kategorie": "Community", "name_organisation": "alina_vegan_foodie", "rolle": "Food & Lifestyle", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "sanft einbinden", "zustaendig": "Daniel"},
    {"kategorie": "Community", "name_organisation": "leipzigisstvegan", "rolle": "lokal", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "regional", "zustaendig": "Daniel"},
    {"kategorie": "Community", "name_organisation": "veganmitrita", "kontaktperson": "Rita", "rolle": "Achtsamkeit", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "Kontakt halten", "zustaendig": "Daniel"},
    {"kategorie": "Community", "name_organisation": "Luisa Vegana", "rolle": "juengere Zielgruppe", "status": "gruen", "kontaktweg": "DM", "naechster_schritt": "Beziehung aufbauen", "zustaendig": "Daniel"},
    {"kategorie": "Presse / Medien", "name_organisation": "urbanite.leipzig", "rolle": "Presse", "status": "gruen", "kontaktweg": "Mail", "naechster_schritt": "Briefing spaeter", "zustaendig": "Daniel"},
]


def seed():
    app = create_app()
    with app.app_context():
        existing = Contact.query.count()
        if existing > 0:
            print(f"Datenbank hat bereits {existing} Kontakte. Uebersprungen.")
            print("Verwende --force um trotzdem zu importieren.")
            import sys
            if "--force" not in sys.argv:
                return

        for data in CONTACTS:
            contact = Contact(
                kategorie=data["kategorie"],
                name_organisation=data["name_organisation"],
                kontaktperson=data.get("kontaktperson"),
                rolle=data.get("rolle"),
                status=data.get("status", "gelb"),
                kontaktweg=data.get("kontaktweg"),
                naechster_schritt=data.get("naechster_schritt"),
                zustaendig=data.get("zustaendig", "Daniel"),
                notizen=data.get("notizen"),
            )
            db.session.add(contact)

        db.session.commit()
        print(f"{len(CONTACTS)} Kontakte importiert.")


if __name__ == "__main__":
    seed()
