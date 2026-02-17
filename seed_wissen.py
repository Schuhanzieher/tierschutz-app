"""
Seed-Skript: Fuellt die Wissensdatenbank mit allen Erkenntnissen
aus dem Instagram-Masterplan, Partnergewinnung und Strategie.

Aufruf:
    python3 seed_wissen.py
    python3 seed_wissen.py --force  (ueberschreibt vorhandene)
"""

from app import create_app
from models import db, ProjektNotiz

WISSEN = [
    # ── INSTAGRAM & SOCIAL MEDIA ──────────────────────────
    {
        "titel": "Instagram-Strategie: Die 5 Content-Saeulen",
        "kategorie": "Instagram & Social Media",
        "prioritaet": "hoch",
        "angepinnt": True,
        "inhalt": """SAEULE 1: SCHOCK & AUFKLAERUNG (40% des Contents)
- "Was du nicht sehen sollst" - Reels mit Fakten zur Massentierhaltung
- "1 Minute Wahrheit" - Kurzvideos mit harten Zahlen
- "Vorher/Nachher" - Gerettete Tiere (emotional, positiv)
- Vergleichs-Reels: "Hund vs. Schwein - Wo ist der Unterschied?"

SAEULE 2: VEGAN LEBEN - LEICHT GEMACHT (25%)
- "Vegan in 30 Sekunden" - Schnelle Rezepte
- "Swap it!" - Tierisches -> vegane Alternative
- "Vegan-Mythen zerstoert" - FAQ-Reels

SAEULE 3: COMMUNITY & PARTNER (15%)
- Partner-Vorstellungen
- Behind-the-Scenes vom Konzert
- Kooperations-Ankuendigungen

SAEULE 4: MUSIK & KONZERT (15%)
- Kuenstler-Teasers
- Proberaum-Einblicke
- Countdown-Posts

SAEULE 5: MITMACHEN & CTA (5%)
- Spendenaufrufe
- "Tagge jemanden, der das sehen muss"
- Ehrenamts-Aufrufe"""
    },
    {
        "titel": "Reels-Regeln fuer maximale Viralitaet",
        "kategorie": "Instagram & Social Media",
        "prioritaet": "hoch",
        "angepinnt": True,
        "inhalt": """1. HOOK in den ersten 1,5 Sekunden (WICHTIGSTE REGEL!)
   - Schockierende Aussage / Provokante Frage / Unerwartetes Bild

2. OPTIMALE LAENGE: 15-30 Sekunden (hoechste Completion Rate)

3. TRENDING AUDIO verwenden (Musik aus der Reels-Bibliothek)

4. TEXT-OVERLAYS IMMER (80% schauen ohne Ton!)

5. CTA AM ENDE: "Teile das mit jemandem, der das wissen muss"

6. POSTING-ZEITEN (Deutschland):
   - Mo-Fr: 7-9 / 12-14 / 18-21 Uhr
   - Sa/So: 10-13 / 17-20 Uhr

7. HASHTAG-STRATEGIE (10-15 pro Post):
   Kern: #Tierschutz #Vegan #MusikGegenWeltschmerz #Benefizkonzert #Munkenradio #Tierrechte #GoVegan
   Wechsel: #Massentierhaltung #Veganismus #TierschutzDeutschland #VeganLeben #PlantBased
   Nische: #VeganeDeutschland #TierschutzAktiv #BenefizEvent #MusikFuerTiere

8. ENGAGEMENT-BOOSTER:
   - Erste 30 Min: auf ALLE Kommentare antworten
   - Erste 15 Min: 10-15 relevante Accounts kommentieren
   - Stories mit Umfragen/Quiz die auf den Post verweisen"""
    },
    {
        "titel": "Top 20 virale Video-Ideen",
        "kategorie": "Content-Strategie",
        "prioritaet": "hoch",
        "angepinnt": True,
        "inhalt": """1. "Was passiert in 60 Sekunden in der Tierindustrie" - Zahlen mit Countdown
2. "Ich habe 30 Tage in einem Schlachthof gearbeitet" - Interview-Format
3. "Dein Hund vs. Ein Schwein - Der Intelligenztest"
4. "Was ist in deinem Essen wirklich drin?" - Zutatenlisten aufdecken
5. "Ich habe 1 Woche fuer 3 Euro/Tag vegan gegessen" - Challenge
6. "Die krassesten Tierrettungen 2025/2026" - Compilation
7. "POV: Du bist ein Huhn in der Massentierhaltung"
8. "3 Dinge die die Fleischindustrie versteckt"
9. "Promis die vegan sind (und warum)" - Lewis Hamilton, Billie Eilish etc.
10. "Strassenbefragung: Wuerdest du dein Fleisch selbst schlachten?"
11. "So sieht ein Tag auf einem Gnadenhof aus" - mit Pfotenherz
12. "Veganer Doener vs. Normaler Doener - Blindtest"
13. "Diese Gesetze schuetzen Tiere NICHT"
14. "Milch - Die ganze Wahrheit in 60 Sekunden"
15. "Ich war beim Tiertransport dabei" - Dokumentar-Stil
16. "Meine Familie reagiert auf Tierschutz-Doku"
17. "Jedes Tier das du isst hatte einen Namen"
18. "Was waere wenn Hunde so behandelt werden wie Nutztiere?"
19. "5 vegane Snacks die JEDER kennt (ohne es zu wissen)"
20. "Der wahre Preis deines Schnitzels" - Subventionen, Umweltkosten

BESTE HOOKS (erste 1-3 Sekunden):
- "In den naechsten 60 Sekunden sterben 120.000 Tiere..."
- "Dieses Video sollte eigentlich geloescht werden..."
- "Warum behandeln wir diese Tiere anders?"
- "Die Fleischindustrie will nicht, dass du das siehst..."
- "Was wuerdest du tun, wenn das dein Hund waere?" """
    },
    {
        "titel": "Content-Kalender (Wochenplan)",
        "kategorie": "Instagram & Social Media",
        "prioritaet": "mittel",
        "inhalt": """WOECHENTLICHER CONTENT-PLAN:

MONTAG:    Reel - Schock/Aufklaerung ("Montags-Wahrheit")
DIENSTAG:  Karussell - Fakten & Infografiken
MITTWOCH:  Reel - Vegan-Rezept oder Swap
DONNERSTAG: Story-Serie - Partner-Vorstellung / Behind-the-Scenes
FREITAG:   Reel - Emotionales Video (gerettete Tiere)
SAMSTAG:   Community-Interaktion (Umfragen, Q&A)
SONNTAG:   Reel - Bester Content re-posted oder Musik-Teaser

= 4-5 Feed-Posts + taegliche Stories

WORKFLOW FUER 1 WOCHE IN 2 STUNDEN:
1. Sonntag Abend: 7 Themen festlegen (15 Min)
2. Texte/Captions mit KI vorschreiben (20 Min)
3. Canva: 7 Posts/Reels mit Templates gestalten (45 Min)
4. CapCut: Videos schneiden (30 Min)
5. Alles in Meta Business Suite vorplanen (10 Min)"""
    },
    {
        "titel": "Kanal-Identitaet & Profil-Setup",
        "kategorie": "Instagram & Social Media",
        "prioritaet": "mittel",
        "inhalt": """PROFIL-SETUP:

Name: @munkenradio.tierschutz (oder @musikgegenweltschmerz)

Bio-Formel:
"Musik gegen Weltschmerz | Tierschutz-Benefizkonzert 2028
Gemeinsam fuer die Tiere. Gemeinsam fuer eine bessere Welt.
Infos & Mitmachen: [Link-in-Bio]"

VISUELLE IDENTITAET:
- Hauptfarben: Dunkelgruen (#1a472a) + Warmweiss + Akzent Lila (#764ba2)
- Logo: Pfote + Notenschluessel kombiniert
- Schriftart: Klar, modern, lesbar (Montserrat)
- Einheitliche Templates fuer Reels, Stories, Posts

HIGHLIGHTS (Stories):
- "Ueber uns"
- "Tierschutz"
- "Partner"
- "Rezepte"
- "Konzert 2028" """
    },

    # ── PARTNERGEWINNUNG ──────────────────────────────────
    {
        "titel": "Partner-Outreach: Taeglicher Workflow (20 Min)",
        "kategorie": "Partnergewinnung",
        "prioritaet": "hoch",
        "angepinnt": True,
        "inhalt": """TAEGLICHER WORKFLOW (20 Minuten):

1. 5 Min: 3-5 neue Ziel-Accounts finden (Suche, Explore, Hashtags)
2. 5 Min: Deren Content liken + kommentieren (ERST Beziehung aufbauen!)
3. 10 Min: DMs senden mit personalisierten Vorlagen
4. In der Tierschutz-App eintragen (neuer Kontakt + Aktivitaet)

WICHTIG: Instagram limitiert DMs!
- Max. 20-30 DMs pro Tag an neue Accounts
- Zu viele DMs = Sperre!
- Besser: Erst folgen -> liken -> kommentieren -> nach 2-3 Tagen anschreiben

ZIEL: 10-15 Accounts pro Tag = 300-450 pro Monat"""
    },
    {
        "titel": "Partner-Zielgruppen: Wer soll angeschrieben werden",
        "kategorie": "Partnergewinnung",
        "prioritaet": "hoch",
        "inhalt": """SYSTEMATISCH SUCHEN IN DIESEN KATEGORIEN:

a) Tierschutz-Organisationen (DE):
   - Gnadenhöfe, Tierheime, Tierschutzvereine
   - Aktivismus-Gruppen (Animal Rebellion, Anonymous for the Voiceless)
   - Investigativ-Organisationen (ANINOVA, SOKO Tierschutz)

b) Vegane Influencer (1K-100K Follower = BESTE Kooperationsrate):
   - Vegane Koeche/Koechinnen
   - Vegane Fitness-Creator
   - Vegane Familien-Accounts
   - Vegane Aktivisten

c) Vegane Unternehmen:
   - Food-Startups, Restaurants, Online-Shops
   - Vegane Mode, Kosmetik
   - Abo-Boxen, Apps

d) Musik-Acts mit Tierschutz-Bezug:
   - Vegane Musiker:innen
   - Bands mit sozialem Engagement
   - Lokale Kuenstler aus Leipzig/Sachsen

e) Medien & Presse:
   - Vegane Magazine (VEGAN Magazin, Kochen ohne Knochen)
   - Lokale Medien (LVZ, urbanite)
   - Podcasts (Vegan ist ungesund, The Vegan Babe)"""
    },
    {
        "titel": "DM-Vorlagen fuer Instagram Anschreiben",
        "kategorie": "Partnergewinnung",
        "prioritaet": "hoch",
        "inhalt": """VORLAGE 1 - ERSTANSPRACHE (warm):
Hi [Name]! Wir lieben eure Arbeit bei [Account]!
Wir von @munkenradio.tierschutz organisieren ein Tierschutz-Benefizkonzert 2028 in Leipzig und wuerden uns mega freuen, euch als Partner dabei zu haben!
Habt ihr Lust auf einen kurzen Austausch?

VORLAGE 2 - ERSTANSPRACHE (professionell):
Hallo [Name], wir sind Munkenradio e.V. und planen das Tierschutz-Benefizkonzert 2028 - ein grosses Event fuer den Tierschutz mit Musik, Bildung und Community.
Eure Organisation [Name] passt perfekt zu unserer Vision. Koennten wir uns austauschen?

VORLAGE 3 - FOLLOW-UP:
Hi nochmal! Ich hatte mich letzte Woche gemeldet wegen unserem Benefizkonzert. Falls ihr Fragen habt, bin ich gerne da! Schaut gern mal auf unserem Profil vorbei

VORLAGE 4 - NACH INTERAKTION:
Hey [Name]! Danke fuers Liken/Kommentieren! Eure Inhalte sind richtig stark. Wir organisieren ein Tierschutz-Benefizkonzert 2028 - haettet ihr Lust, Teil davon zu sein?

TIPP: Vorlagen sind auch im Textgenerator der App verfuegbar!"""
    },

    # ── AUTOMATISIERUNG & TOOLS ───────────────────────────
    {
        "titel": "Tools & Software fuer Automatisierung",
        "kategorie": "Automatisierung & Tools",
        "prioritaet": "mittel",
        "inhalt": """CONTENT-ERSTELLUNG:
- Canva Pro (12,99 Euro/Monat): Brand-Kit, Templates, Team-Zugang, Scheduling
- CapCut (kostenlos): Reels schneiden, Auto-Untertitel, Trending-Effekte
- ChatGPT / Claude: Captions, Hashtags, Hooks brainstormen

SCHEDULING:
- Meta Business Suite (KOSTENLOS, empfohlen): Posts vorplanen, Insights, DMs verwalten
- Later (ab 16,67 Euro/Monat): Visueller Kalender, Linkin.bio
- Buffer (kostenlos fuer 3 Kanaele): AI-Assistent, Analytics

PARTNER-MANAGEMENT:
- Unsere Tierschutz-App (bereits vorhanden!): Kontakte, Follow-Ups, Textgenerator
- Google Sheets + Calendar: Ziel-Accounts, Erinnerungen
- Notion (kostenlos): CRM-Board, Kanban

EMPFEHLUNG:
Meta Business Suite (kostenlos) + Canva Pro (Templates) + Unsere App (CRM)

CONTENT-QUELLEN (legal):
- Pexels.com, Unsplash.com (kostenlose Stockvideos/Fotos)
- ANINOVA (Partnerschaft fuer Material)
- Pfotenherz (Drehs auf dem Gnadenhof)
- Canva Stockvideo-Bibliothek
- Our World in Data (CC-Lizenz Grafiken)"""
    },

    # ── WACHSTUMS-STRATEGIE ───────────────────────────────
    {
        "titel": "Wachstums-Meilensteine & Timeline",
        "kategorie": "Instagram & Social Media",
        "prioritaet": "hoch",
        "inhalt": """PHASE 1: AUFBAU (Maerz - August 2026)
Ziel: 500 Follower, 20 neue Partner
- Profil optimieren, Highlights erstellen
- 3-4 Posts/Woche starten
- 10 Accounts/Tag anschreiben
- 5 Kooperationen mit kleinen Accounts
- Content-Vorrat fuer 2 Wochen

PHASE 2: WACHSTUM (September 2026 - Juni 2027)
Ziel: 2.000-5.000 Follower, 50 Partner
- 5 Posts/Woche
- 1 virales Reel/Woche anpeilen
- Instagram Collabs (geteilte Posts)
- Instagram Live mit Partnern
- Bezahlte Werbung testen (5-10 Euro/Tag)

PHASE 3: REICHWEITE (Juli 2027 - Juni 2028)
Ziel: 10.000+ Follower, 100+ Partner
- Taegliche Posts
- Influencer-Kooperationen
- Presse verstaerkt einbinden
- Countdown zum Konzert

PHASE 4: KONZERT-HYPE (Juli - Dezember 2028)
Ziel: Maximale Reichweite, ausverkauft
- Taeglicher Content mit Countdown
- Kuenstler-Teasers, Behind-the-Scenes
- Live-Berichterstattung am Konzerttag"""
    },
    {
        "titel": "KPIs & Erfolgsmessung (woechentlich tracken)",
        "kategorie": "Instagram & Social Media",
        "prioritaet": "mittel",
        "inhalt": """WOECHENTLICH TRACKEN:
- Follower-Wachstum
- Reichweite pro Post
- Engagement-Rate (Likes + Kommentare + Shares / Follower)
- Story-Views
- Profil-Besuche
- Website-Klicks
- Neue Partner-Kontakte
- Antwort-Rate auf DMs

ZIEL-WERTE:
- Engagement-Rate: ueber 5% (unter 1000 Follower)
- Engagement-Rate: ueber 3% (1000-10.000 Follower)
- DM-Antwort-Rate: ueber 30%
- Follower-Wachstum: +10-20% pro Monat (am Anfang)"""
    },

    # ── KONZERT-PLANUNG ───────────────────────────────────
    {
        "titel": "Quick-Start: Die ersten 7 Tage Instagram",
        "kategorie": "Konzert-Planung",
        "prioritaet": "hoch",
        "inhalt": """TAG 1: Profil einrichten
- Bio optimieren, Profilbild (Logo), Highlights erstellen
- Link-in-Bio einrichten

TAG 2: Erste 3 Posts erstellen
- Vorstellungs-Post: "Wer sind wir?"
- Fakten-Karussell: "5 Fakten ueber Massentierhaltung"
- Emotionales Reel: Gerettete Tiere

TAG 3: Netzwerken starten
- 20 relevante Accounts folgen
- 10 Accounts kommentieren (echte, wertvolle Kommentare!)
- 5 DMs an potenzielle Partner

TAG 4: Content-Vorrat aufbauen
- 5 Canva-Templates erstellen
- 3 Reels vorproduzieren
- 3 Hashtag-Sets vorbereiten (je 15 Hashtags)

TAG 5: Erste Kooperation
- Pfotenherz fuer gemeinsamen Post anfragen
- Story-Takeover vorschlagen

TAG 6: Scheduling einrichten
- Meta Business Suite verbinden
- Posts fuer Woche 2 vorplanen

TAG 7: Analyse
- Insights pruefen: Welcher Post lief am besten?
- Wochenplan fuer Woche 2 erstellen"""
    },

    # ── FINANZEN ──────────────────────────────────────────
    {
        "titel": "Kosten-Uebersicht Social Media & Tools",
        "kategorie": "Finanzen & Foerderung",
        "prioritaet": "mittel",
        "inhalt": """KOSTENLOS MACHBAR:
- Instagram selbst
- Meta Business Suite (Scheduling)
- CapCut (Videoschnitt)
- Buffer Basis-Version
- Unsere Tierschutz-App
- Pexels/Unsplash (Material)

EMPFOHLENE INVESTITIONEN:
- Canva Pro: 12,99 Euro/Monat
- Gelegentliche Ads: 50-100 Euro/Monat (beste Reels boosten)
- Ring-Light + Stativ: einmalig ca. 30-50 Euro
- Mikrofon fuer Handy: einmalig ca. 20-30 Euro

GESAMT: ca. 60-160 Euro/Monat
MINIMUM (nur kostenlose Tools): 0 Euro/Monat"""
    },

    # ── VEGANE BEWEGUNG ───────────────────────────────────
    {
        "titel": "Vision: Vegane Master App",
        "kategorie": "Vegane Bewegung",
        "prioritaet": "mittel",
        "inhalt": """ZUKUNFTSVISION: Eine zentrale Plattform die ALLE veganen Communities vereint.

GEPLANTE BEREICHE:
1. Community-Hub - Verzeichnis aller veganen Orgas, Unternehmen, Influencer
2. Event-Kalender - Demos, Festivals, Workshops, Konzerte
3. Vegane Karte - Restaurants, Shops, Gnadenhöfe in der Naehe
4. Wissens-Datenbank - Fakten, Rezepte, FAQ fuer Einsteiger
5. Aktivismus-Tools - Petitionen, Demo-Koordination, Material
6. Social Features - Chat, Gruppen, Vegan-Buddy-Mentoring
7. Marktplatz - Produkte, Jobs, Gutscheine

STATUS: Konzept-Phase. Prompt fuer neue Sitzung erstellt.
DATEI: PROMPT_VEGANE_MASTER_APP.md"""
    },

    # ── ALLGEMEIN ─────────────────────────────────────────
    {
        "titel": "Die 5 goldenen Regeln fuer Instagram-Erfolg",
        "kategorie": "Allgemein",
        "prioritaet": "hoch",
        "angepinnt": True,
        "inhalt": """1. KONSISTENZ SCHLAEGT PERFEKTION
   Lieber 4 gute Posts pro Woche als 1 perfekter pro Monat.

2. HOOK FIRST
   Die ersten 1,5 Sekunden entscheiden ob jemand weiterschaut.
   Investiere 50% deiner Zeit in den Hook.

3. EMOTION VERKAUFT
   Wut, Trauer, Freude, Ueberraschung - Emotionen werden geteilt.
   Fakten allein reichen nicht.

4. BEZIEHUNGEN VOR REICHWEITE
   10 echte Partner bringen mehr als 10.000 passive Follower.
   Investiere in Beziehungen.

5. AUTOMATISIERE WAS GEHT
   Content-Erstellung, Scheduling, Follow-Up-Erinnerungen -
   alles was Zeit frisst, so effizient wie moeglich machen.
   Nutze die App als zentrale Schaltstelle!"""
    },
    {
        "titel": "Technischer Stand: App & Deployment",
        "kategorie": "Allgemein",
        "prioritaet": "niedrig",
        "inhalt": """AKTUELLER TECH-STACK:
- Python/Flask + SQLAlchemy + SQLite
- Bootstrap 5.3.3 + Bootstrap Icons 1.11.3
- Chart.js 4.4.7

FEATURES:
- Kontakt-CRM (33 Kontakte)
- Dashboard mit KPIs und Charts
- Follow-Up-Erinnerungen
- Team-Chat mit Kanaelen
- Textgenerator (6 Vorlagen)
- Wissensdatenbank
- CSV-Export

HOSTING:
- PythonAnywhere (kostenlos): https://schuhanzieher01.pythonanywhere.com
- GitHub: https://github.com/Schuhanzieher/tierschutz-app
- Lokal: /Users/munkenfredrecords/Desktop/Buero/Claude/Tierschutz/tierschutz-app/

UPDATE-WORKFLOW:
1. Lokal aendern
2. git add . && git commit -m "Beschreibung" && git push
3. PythonAnywhere Bash: cd ~/tierschutz-app && git pull
4. Web-Tab: Reload klicken"""
    },
]


def seed():
    app = create_app()
    with app.app_context():
        existing = ProjektNotiz.query.count()
        if existing > 0:
            import sys
            if "--force" not in sys.argv:
                print(f"Wissensdatenbank hat bereits {existing} Eintraege. Uebersprungen.")
                print("Verwende --force um trotzdem zu importieren.")
                return
            else:
                print(f"--force: Loesche {existing} vorhandene Eintraege...")
                ProjektNotiz.query.delete()
                db.session.commit()

        for data in WISSEN:
            notiz = ProjektNotiz(
                titel=data["titel"],
                kategorie=data["kategorie"],
                inhalt=data["inhalt"],
                prioritaet=data.get("prioritaet", "mittel"),
                erstellt_von="Daniel",
                angepinnt=data.get("angepinnt", False),
            )
            db.session.add(notiz)

        db.session.commit()
        print(f"{len(WISSEN)} Wissenseintraege importiert!")
        print("\nAngepinnte Eintraege:")
        for d in WISSEN:
            if d.get("angepinnt"):
                print(f"  - {d['titel']}")


if __name__ == "__main__":
    seed()
