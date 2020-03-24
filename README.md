# lernhelfer-api
Dieses Repository enthält das Backend für unsere App [Lernhelfer](https://github.com/Lernhelfer/lernhelfer-app).
Ziel der App ist es, trotz der durch Corona bedingten landesweiten Schulschließungen die Schüler weiterhin beim Lösen ihrer Schulaufgaben zu helfen.
Unsere App bietet eine Plattform, bei der der Kontakt zwischen Schüler und lernhelfenden Personen vermittelt wird.
[Weiterlesen](https://devpost.com/software/1_019_d_interaktiveschuelerunterstuetzung)

# Technische Realisation
In Python wird ein Flask Service aufgesetzt, der die Enpunkte der API anbietet.
Das ganze ist bereits dockerisiert, um ein einfaches Deployment auf einem Server zu gewährleisten.

# RESTful API
Die App kann per RESTful API mit der Datenbank kommunizieren.
Eine Definition aller Endpunkte findet man in der [API Dokumentation](api.md).

# POSTGRE
Als Datenbank kommt eine Postgre Instanz zum Einsatz. 
Ein Tabellenschema ist unter [/database/create_tables.sql](./database/create_tables.sql) zu finden
