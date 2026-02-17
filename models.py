from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

# Status-Mapping: Interne Codes -> Emoji + Label + CSS
STATUS_MAP = {
    "gruen": {"emoji": "\U0001f7e2", "label": "aktiv / im Austausch", "css_class": "status-green"},
    "gelb":  {"emoji": "\U0001f7e1", "label": "offen / warm / sp\u00e4ter", "css_class": "status-yellow"},
    "rot":   {"emoji": "\U0001f534", "label": "aktuell nicht m\u00f6glich", "css_class": "status-red"},
}

# Emoji -> interner Code (fuer Import)
EMOJI_TO_STATUS = {
    "\U0001f7e2": "gruen",
    "\U0001f7e1": "gelb",
    "\U0001f534": "rot",
}

# Status-Reihenfolge fuer Toggle
STATUS_CYCLE = ["gruen", "gelb", "rot"]

# Vordefinierte Kategorien
KATEGORIEN = [
    "NGO / Tierschutz",
    "Musik / Kultur",
    "Bildung / Speaker",
    "Unternehmen",
    "Community",
    "Presse / Medien",
]

# Aktivitaets-Typen
AKTIVITAETS_TYPEN = [
    "Mail",
    "DM",
    "Anruf",
    "Treffen",
    "Notiz",
]


class Contact(db.Model):
    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True)
    kategorie = db.Column(db.String(50), nullable=False, index=True)
    name_organisation = db.Column(db.String(200), nullable=False)
    kontaktperson = db.Column(db.String(200), nullable=True)
    rolle = db.Column(db.String(300), nullable=True)
    status = db.Column(db.String(10), nullable=False, default="gelb", index=True)
    kontaktweg = db.Column(db.String(100), nullable=True)
    kontaktdaten = db.Column(db.Text, nullable=True)
    letzter_kontakt = db.Column(db.Date, nullable=True)
    naechster_schritt = db.Column(db.Text, nullable=True)
    zustaendig = db.Column(db.String(100), nullable=True, default="Daniel")
    notizen = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def status_emoji(self):
        return STATUS_MAP.get(self.status, {}).get("emoji", "?")

    def status_label(self):
        return STATUS_MAP.get(self.status, {}).get("label", "unbekannt")

    def status_css_class(self):
        return STATUS_MAP.get(self.status, {}).get("css_class", "")

    def next_status(self):
        try:
            idx = STATUS_CYCLE.index(self.status)
            return STATUS_CYCLE[(idx + 1) % len(STATUS_CYCLE)]
        except ValueError:
            return "gelb"

    def __repr__(self):
        return f"<Contact {self.id}: {self.name_organisation}>"


class ActivityLog(db.Model):
    __tablename__ = "activity_log"

    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False, index=True)
    datum = db.Column(db.Date, nullable=False, default=date.today)
    typ = db.Column(db.String(50), nullable=True)
    beschreibung = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    contact = db.relationship(
        "Contact",
        backref=db.backref("activities", lazy="dynamic", order_by="ActivityLog.datum.desc()"),
    )

    def __repr__(self):
        return f"<ActivityLog {self.id}: {self.typ} am {self.datum}>"


# Vordefinierte Organisationsmitglieder
ORGA_MITGLIEDER = [
    "Daniel",
    "Alex",
    "Sarah",
    "Mika",
    "Team",
]

# Text-Generator Vorlagen
TEXT_VORLAGEN = {
    "erstansprache_email": {
        "label": "Erstansprache (E-Mail)",
        "kategorie": "E-Mail",
        "template": """Betreff: Kooperationsanfrage – Tierschutz-Benefizkonzert 2028

Sehr geehrte/r {anrede} {name},

mein Name ist {absender} vom Verein Munkenradio e. V. Wir organisieren ein Tierschutz-Benefizkonzert im Jahr 2028 unter dem Motto „Musik gegen Weltschmerz".

Wir sind auf {organisation} aufmerksam geworden und würden uns sehr freuen, mit Ihnen über eine mögliche Zusammenarbeit zu sprechen.

{details}

Hätten Sie Interesse an einem kurzen Austausch? Ich freue mich auf Ihre Rückmeldung.

Herzliche Grüße
{absender}
Munkenradio e. V.""",
    },
    "erstansprache_dm": {
        "label": "Erstansprache (Social Media DM)",
        "kategorie": "Social Media",
        "template": """Hi {name}! 👋

Ich bin {absender} von Munkenradio e. V. – wir planen ein Tierschutz-Benefizkonzert 2028 und finden eure Arbeit bei {organisation} richtig stark! 🐾

{details}

Hättet ihr Lust, darüber mal zu quatschen? Würde mich mega freuen! 🎶

Liebe Grüße, {absender}""",
    },
    "followup": {
        "label": "Follow-Up / Nachfassen",
        "kategorie": "E-Mail",
        "template": """Betreff: Kurzes Follow-Up – Tierschutz-Benefizkonzert 2028

Hallo {name},

ich hoffe, es geht Ihnen gut! Ich hatte mich vor kurzem wegen einer möglichen Kooperation für unser Tierschutz-Benefizkonzert gemeldet.

{details}

Ich wollte kurz nachfragen, ob Sie Gelegenheit hatten, darüber nachzudenken. Falls Sie Fragen haben, stehe ich gerne zur Verfügung.

Beste Grüße
{absender}
Munkenradio e. V.""",
    },
    "danke": {
        "label": "Dankesnachricht",
        "kategorie": "E-Mail",
        "template": """Betreff: Herzlichen Dank! 🐾

Liebe/r {name},

vielen herzlichen Dank für die tolle Zusammenarbeit und Unterstützung! {details}

Es ist wunderbar zu sehen, wie viele Menschen sich gemeinsam für den Tierschutz einsetzen. Wir freuen uns auf alles, was noch kommt!

Herzliche Grüße
{absender}
Munkenradio e. V.""",
    },
    "social_post": {
        "label": "Social-Media-Post",
        "kategorie": "Social Media",
        "template": """🐾🎶 Musik gegen Weltschmerz! 🎶🐾

Wir freuen uns riesig: {organisation} ist mit dabei beim Tierschutz-Benefizkonzert 2028! 🎉

{details}

Gemeinsam für die Tiere – gemeinsam für eine bessere Welt! 🌍💚

#Tierschutz #Benefizkonzert #MusikGegenWeltschmerz #Munkenradio
{extra_hashtags}""",
    },
    "pressetext": {
        "label": "Pressetext / Ankündigung",
        "kategorie": "Presse",
        "template": """PRESSEMITTEILUNG

Tierschutz-Benefizkonzert 2028 – „Musik gegen Weltschmerz"

{ort}, {datum} – Der Verein Munkenradio e. V. lädt zum großen Tierschutz-Benefizkonzert 2028 ein. Unter dem Motto „Musik gegen Weltschmerz" setzen Künstler:innen und Organisationen gemeinsam ein Zeichen für den Tierschutz.

{details}

Über Munkenradio e. V.:
Munkenradio e. V. verbindet Musik und soziales Engagement. Mit dem Benefizkonzert 2028 möchte der Verein auf Tierschutzthemen aufmerksam machen und Spenden sammeln.

Kontakt:
{absender}
Munkenradio e. V.
E-Mail: {email}""",
    },
}


class ChatRubrik(db.Model):
    __tablename__ = "chat_rubriken"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    emoji = db.Column(db.String(10), nullable=False, default="💬")
    beschreibung = db.Column(db.String(300), nullable=True)
    erstellt_von = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship("ChatMessage", backref="rubrik", lazy="dynamic",
                                order_by="ChatMessage.created_at.asc()")

    def __repr__(self):
        return f"<ChatRubrik {self.id}: {self.name}>"


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.Integer, primary_key=True)
    absender = db.Column(db.String(100), nullable=False)
    nachricht = db.Column(db.Text, nullable=False)
    rubrik_id = db.Column(db.Integer, db.ForeignKey("chat_rubriken.id"), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatMessage {self.id}: {self.absender}>"


class ProjektNotiz(db.Model):
    """Wissensdatenbank: Strategien, Erkenntnisse, Plaene."""
    __tablename__ = "projekt_notizen"

    id = db.Column(db.Integer, primary_key=True)
    titel = db.Column(db.String(300), nullable=False)
    kategorie = db.Column(db.String(100), nullable=False, index=True)
    inhalt = db.Column(db.Text, nullable=False)
    prioritaet = db.Column(db.String(20), nullable=False, default="mittel")  # hoch, mittel, niedrig
    erstellt_von = db.Column(db.String(100), nullable=False, default="Daniel")
    angepinnt = db.Column(db.Boolean, default=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ProjektNotiz {self.id}: {self.titel}>"


# Kategorien fuer Wissensdatenbank
NOTIZ_KATEGORIEN = [
    "Instagram & Social Media",
    "Partnergewinnung",
    "Content-Strategie",
    "Automatisierung & Tools",
    "Konzert-Planung",
    "Vegane Bewegung",
    "Finanzen & Foerderung",
    "Allgemein",
]

NOTIZ_PRIORITAETEN = {
    "hoch": {"emoji": "🔴", "label": "Hoch", "css": "text-danger"},
    "mittel": {"emoji": "🟡", "label": "Mittel", "css": "text-warning"},
    "niedrig": {"emoji": "🟢", "label": "Niedrig", "css": "text-success"},
}


# Standard-Rubriken die beim Start erstellt werden
DEFAULT_RUBRIKEN = [
    {"name": "Allgemein", "emoji": "💬", "beschreibung": "Allgemeiner Team-Chat"},
    {"name": "Planung", "emoji": "📋", "beschreibung": "Konzertplanung & Organisation"},
    {"name": "Ideen", "emoji": "💡", "beschreibung": "Ideen & Brainstorming"},
    {"name": "Kontakte", "emoji": "📇", "beschreibung": "Diskussionen zu Kontakten & Partnern"},
]
