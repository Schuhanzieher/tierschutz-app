import csv
import io
from datetime import date, datetime

from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    Response,
    url_for,
)
from models import (
    db,
    Contact,
    ActivityLog,
    ChatMessage,
    STATUS_MAP,
    STATUS_CYCLE,
    KATEGORIEN,
    AKTIVITAETS_TYPEN,
    ORGA_MITGLIEDER,
    TEXT_VORLAGEN,
)


def register_routes(app):

    # ── Dashboard ──────────────────────────────────────────────

    @app.route("/")
    def index():
        total = Contact.query.count()

        # Zahlen pro Kategorie
        kat_counts = (
            db.session.query(Contact.kategorie, db.func.count(Contact.id))
            .group_by(Contact.kategorie)
            .all()
        )

        # Zahlen pro Status
        status_counts = (
            db.session.query(Contact.status, db.func.count(Contact.id))
            .group_by(Contact.status)
            .all()
        )
        status_dict = {code: count for code, count in status_counts}

        # Letzte Aktivitaeten
        recent_activities = (
            ActivityLog.query
            .order_by(ActivityLog.created_at.desc())
            .limit(10)
            .all()
        )

        # Gesamtzahl Aktivitaeten
        total_activities = ActivityLog.query.count()

        # Kontaktwege zaehlen
        kontaktweg_counts = (
            db.session.query(Contact.kontaktweg, db.func.count(Contact.id))
            .filter(Contact.kontaktweg.isnot(None))
            .group_by(Contact.kontaktweg)
            .all()
        )

        # Naechste Schritte (offene Todos)
        open_todos = (
            Contact.query
            .filter(Contact.naechster_schritt.isnot(None))
            .filter(Contact.naechster_schritt != "")
            .order_by(Contact.letzter_kontakt.asc().nullsfirst())
            .limit(5)
            .all()
        )

        return render_template(
            "index.html",
            total=total,
            kat_counts=kat_counts,
            status_counts=status_counts,
            status_dict=status_dict,
            recent_activities=recent_activities,
            total_activities=total_activities,
            kontaktweg_counts=kontaktweg_counts,
            open_todos=open_todos,
            status_map=STATUS_MAP,
            kategorien=KATEGORIEN,
        )

    # ── Kontaktliste ───────────────────────────────────────────

    @app.route("/kontakte")
    def contact_list():
        query = Contact.query

        # Filter: Kategorie
        kat = request.args.get("kategorie", "")
        if kat:
            query = query.filter(Contact.kategorie == kat)

        # Filter: Status
        status = request.args.get("status", "")
        if status:
            query = query.filter(Contact.status == status)

        # Sortierung
        sort = request.args.get("sort", "name")
        if sort == "status":
            query = query.order_by(Contact.status, Contact.name_organisation)
        elif sort == "kategorie":
            query = query.order_by(Contact.kategorie, Contact.name_organisation)
        elif sort == "letzter_kontakt":
            query = query.order_by(Contact.letzter_kontakt.desc().nullslast(), Contact.name_organisation)
        else:
            query = query.order_by(Contact.name_organisation)

        contacts = query.all()

        return render_template(
            "contacts/list.html",
            contacts=contacts,
            kategorien=KATEGORIEN,
            status_map=STATUS_MAP,
            current_kat=kat,
            current_status=status,
            current_sort=sort,
        )

    # ── Kontakt erstellen ──────────────────────────────────────

    @app.route("/kontakte/neu", methods=["GET", "POST"])
    def contact_create():
        if request.method == "POST":
            kontakt = Contact(
                kategorie=request.form.get("kategorie", "").strip(),
                name_organisation=request.form.get("name_organisation", "").strip(),
                kontaktperson=request.form.get("kontaktperson", "").strip() or None,
                rolle=request.form.get("rolle", "").strip() or None,
                status=request.form.get("status", "gelb"),
                kontaktweg=request.form.get("kontaktweg", "").strip() or None,
                kontaktdaten=request.form.get("kontaktdaten", "").strip() or None,
                letzter_kontakt=_parse_date(request.form.get("letzter_kontakt", "")),
                naechster_schritt=request.form.get("naechster_schritt", "").strip() or None,
                zustaendig=request.form.get("zustaendig", "").strip() or "Daniel",
                notizen=request.form.get("notizen", "").strip() or None,
            )

            if not kontakt.name_organisation:
                flash("Name / Organisation ist erforderlich.", "error")
                return render_template(
                    "contacts/form.html",
                    contact=kontakt,
                    kategorien=KATEGORIEN,
                    status_map=STATUS_MAP,
                    is_edit=False,
                )

            if not kontakt.kategorie:
                flash("Kategorie ist erforderlich.", "error")
                return render_template(
                    "contacts/form.html",
                    contact=kontakt,
                    kategorien=KATEGORIEN,
                    status_map=STATUS_MAP,
                    is_edit=False,
                )

            db.session.add(kontakt)
            db.session.commit()
            flash(f"{kontakt.name_organisation} wurde angelegt.", "success")
            return redirect(url_for("contact_detail", id=kontakt.id))

        return render_template(
            "contacts/form.html",
            contact=None,
            kategorien=KATEGORIEN,
            status_map=STATUS_MAP,
            is_edit=False,
        )

    # ── Kontakt-Detail ─────────────────────────────────────────

    @app.route("/kontakte/<int:id>")
    def contact_detail(id):
        contact = Contact.query.get_or_404(id)
        activities = contact.activities.order_by(ActivityLog.datum.desc()).all()
        return render_template(
            "contacts/detail.html",
            contact=contact,
            activities=activities,
            aktivitaets_typen=AKTIVITAETS_TYPEN,
        )

    # ── Kontakt bearbeiten ─────────────────────────────────────

    @app.route("/kontakte/<int:id>/bearbeiten", methods=["GET", "POST"])
    def contact_edit(id):
        contact = Contact.query.get_or_404(id)

        if request.method == "POST":
            contact.kategorie = request.form.get("kategorie", "").strip()
            contact.name_organisation = request.form.get("name_organisation", "").strip()
            contact.kontaktperson = request.form.get("kontaktperson", "").strip() or None
            contact.rolle = request.form.get("rolle", "").strip() or None
            contact.status = request.form.get("status", "gelb")
            contact.kontaktweg = request.form.get("kontaktweg", "").strip() or None
            contact.kontaktdaten = request.form.get("kontaktdaten", "").strip() or None
            contact.letzter_kontakt = _parse_date(request.form.get("letzter_kontakt", ""))
            contact.naechster_schritt = request.form.get("naechster_schritt", "").strip() or None
            contact.zustaendig = request.form.get("zustaendig", "").strip() or "Daniel"
            contact.notizen = request.form.get("notizen", "").strip() or None

            if not contact.name_organisation:
                flash("Name / Organisation ist erforderlich.", "error")
                return render_template(
                    "contacts/form.html",
                    contact=contact,
                    kategorien=KATEGORIEN,
                    status_map=STATUS_MAP,
                    is_edit=True,
                )

            db.session.commit()
            flash(f"{contact.name_organisation} wurde aktualisiert.", "success")
            return redirect(url_for("contact_detail", id=contact.id))

        return render_template(
            "contacts/form.html",
            contact=contact,
            kategorien=KATEGORIEN,
            status_map=STATUS_MAP,
            is_edit=True,
        )

    # ── Status-Toggle ──────────────────────────────────────────

    @app.route("/kontakte/<int:id>/status", methods=["POST"])
    def contact_status_update(id):
        contact = Contact.query.get_or_404(id)
        contact.status = contact.next_status()
        db.session.commit()

        # Zurueck zur vorherigen Seite
        referrer = request.referrer or url_for("contact_list")
        return redirect(referrer)

    # ── Aktivitaet hinzufuegen ─────────────────────────────────

    @app.route("/kontakte/<int:id>/aktivitaet", methods=["POST"])
    def contact_add_activity(id):
        contact = Contact.query.get_or_404(id)

        datum = _parse_date(request.form.get("datum", "")) or date.today()
        typ = request.form.get("typ", "").strip() or None
        beschreibung = request.form.get("beschreibung", "").strip() or None

        activity = ActivityLog(
            contact_id=contact.id,
            datum=datum,
            typ=typ,
            beschreibung=beschreibung,
        )
        db.session.add(activity)

        # Letzten Kontakt aktualisieren, wenn das Datum neuer ist
        if contact.letzter_kontakt is None or datum > contact.letzter_kontakt:
            contact.letzter_kontakt = datum

        db.session.commit()
        flash("Aktivit\u00e4t wurde hinzugef\u00fcgt.", "success")
        return redirect(url_for("contact_detail", id=contact.id))

    # ── Kontakt loeschen ───────────────────────────────────────

    @app.route("/kontakte/<int:id>/loeschen", methods=["POST"])
    def contact_delete(id):
        contact = Contact.query.get_or_404(id)
        name = contact.name_organisation

        # Zuerst Aktivitaeten loeschen
        ActivityLog.query.filter_by(contact_id=contact.id).delete()
        db.session.delete(contact)
        db.session.commit()

        flash(f"{name} wurde gel\u00f6scht.", "success")
        return redirect(url_for("contact_list"))

    # ── CSV-Export ─────────────────────────────────────────────

    @app.route("/export")
    def export_csv():
        contacts = Contact.query.order_by(Contact.kategorie, Contact.name_organisation).all()

        output = io.StringIO()
        writer = csv.writer(output, delimiter=";")

        # Header
        writer.writerow([
            "Kategorie", "Name / Organisation", "Kontaktperson",
            "Rolle / Bezug", "Status", "Kontaktweg", "Kontaktdaten",
            "Letzter Kontakt", "N\u00e4chster Schritt", "Zust\u00e4ndig", "Notizen",
        ])

        for c in contacts:
            writer.writerow([
                c.kategorie,
                c.name_organisation,
                c.kontaktperson or "",
                c.rolle or "",
                c.status_emoji() + " " + c.status_label(),
                c.kontaktweg or "",
                c.kontaktdaten or "",
                c.letzter_kontakt.strftime("%d.%m.%Y") if c.letzter_kontakt else "",
                c.naechster_schritt or "",
                c.zustaendig or "",
                c.notizen or "",
            ])

        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=kontakte_export_{date.today().isoformat()}.csv"
            },
        )

    # ── Chat ──────────────────────────────────────────────────

    @app.route("/chat")
    def chat():
        messages = ChatMessage.query.order_by(ChatMessage.created_at.asc()).all()
        return render_template(
            "chat.html",
            messages=messages,
            mitglieder=ORGA_MITGLIEDER,
        )

    @app.route("/chat/senden", methods=["POST"])
    def chat_send():
        absender = request.form.get("absender", "").strip()
        nachricht = request.form.get("nachricht", "").strip()

        if not absender or not nachricht:
            flash("Absender und Nachricht sind erforderlich.", "error")
            return redirect(url_for("chat"))

        msg = ChatMessage(absender=absender, nachricht=nachricht)
        db.session.add(msg)
        db.session.commit()

        return redirect(url_for("chat"))

    @app.route("/chat/api")
    def chat_api():
        """JSON-Endpunkt fuer Chat-Polling."""
        after_id = request.args.get("after", 0, type=int)
        messages = (
            ChatMessage.query
            .filter(ChatMessage.id > after_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )
        return {
            "messages": [
                {
                    "id": m.id,
                    "absender": m.absender,
                    "nachricht": m.nachricht,
                    "zeit": m.created_at.strftime("%d.%m.%Y %H:%M"),
                }
                for m in messages
            ]
        }

    # ── Text-Generator ────────────────────────────────────────

    @app.route("/textgenerator")
    def textgenerator():
        return render_template(
            "textgenerator.html",
            vorlagen=TEXT_VORLAGEN,
            mitglieder=ORGA_MITGLIEDER,
            kontakte=Contact.query.order_by(Contact.name_organisation).all(),
        )

    @app.route("/textgenerator/generieren", methods=["POST"])
    def textgenerator_generate():
        vorlage_key = request.form.get("vorlage", "")
        vorlage = TEXT_VORLAGEN.get(vorlage_key)

        if not vorlage:
            flash("Unbekannte Vorlage.", "error")
            return redirect(url_for("textgenerator"))

        # Platzhalter aus Formular sammeln
        template_text = vorlage["template"]
        felder = {
            "name": request.form.get("name", "").strip(),
            "anrede": request.form.get("anrede", "").strip(),
            "organisation": request.form.get("organisation", "").strip(),
            "absender": request.form.get("absender", "").strip() or "Daniel",
            "details": request.form.get("details", "").strip(),
            "email": request.form.get("email", "").strip(),
            "ort": request.form.get("ort", "").strip(),
            "datum": request.form.get("datum", "").strip() or date.today().strftime("%d.%m.%Y"),
            "extra_hashtags": request.form.get("extra_hashtags", "").strip(),
        }

        # Platzhalter ersetzen (fehlende bleiben leer)
        result = template_text
        for key, value in felder.items():
            result = result.replace("{" + key + "}", value)

        return render_template(
            "textgenerator.html",
            vorlagen=TEXT_VORLAGEN,
            mitglieder=ORGA_MITGLIEDER,
            kontakte=Contact.query.order_by(Contact.name_organisation).all(),
            generated_text=result,
            selected_vorlage=vorlage_key,
            felder=felder,
        )

    # ── Hilfsfunktionen ────────────────────────────────────────

    def _parse_date(date_str):
        if not date_str:
            return None
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return None
