# termgr
Stand: 2026-11-24, geprüft gegen Commit fe85d68

## Zweck
Server-seitiges Backend zur Verwaltung von Terminals (Digital-Signage-Systemen
und deren Deployments). Stellt HTTP-Endpoints bereit, über die autorisierte
Techniker/Admins Systeme einrichten, deployen, konfigurieren und fernsteuern.
Gegenstück zum Geräte-Agenten `digsigctl`: termgr kennt die zentrale Zuordnung
System→Standort→URL und stößt darüber Aktionen auf den Geräten an.

## Stack & Einstiegspunkte
Python 3, Flask über das Homeinfo-`his`-Framework (`his.Application`), als WSGI
ausgeliefert. ORM: Peewee (via `peeweeplus`, MySQL-Datenbank `termgr`).
Python-Package `termgr` (installiert per `setup.py`, `setuptools_scm`-Versionierung).

WSGI-Einstiegspunkt: `termgr/wsgi/__init__.py` bündelt `ROUTES`/`APPLICATION`
aus den Submodulen `administer`, `ddbaccounts`, `dephist`, `listing`, `setup`.
Console-Scripts (`setup.py`): `dephist` (Deployment-Historie),
`reload-terminals` = `termgr.wireguard:update_peers`, `toggle-ddb-install-account`.

## Schnittstellen
### Konsumiert
- **Fremde DB-Tabellen** (Homeinfo-Bibliotheken, gemeinsame MySQL-Instanz):
  `hwdb` (System, Deployment, ApplicationMode, WireGuard-Netz/-Server),
  `his` (Account/Auth), `mdb` (Address, Company, Customer),
  `hipster` (Queue — für Sync-Aufträge).
- **Geräte-Agent `digsigctl`** auf den Systemen: `hwdb.System` ruft dessen
  HTTP-RPC auf (`apply_url`, `reboot`, `beep`, `application`, restart web browser).
  ⚠️ ANNAHME: Der konkrete HTTP-Call liegt in `hwdb`, nicht in diesem Repo.
- **WireGuard:** `wgtools` + `sudo /usr/bin/wg`; verwaltet Peers der Systeme.
- **E-Mail:** `emaillib.Mailer` (SMTP), Benachrichtigung der Admins bei Deployments.
- **Konfiguration:** `termgr.conf` (via `configlib`) — SMTP, WireGuard-Devname,
  Admin-Verteiler, Notify-Texte. ⚠️ ANNAHME: enthält Zugangsdaten, liegt außerhalb
  des Repos (nicht eingecheckt).
- **ACLs:** `termacls` (Decorators `sysadmin`, `depadmin`, `deploy` in
  `wsgi/common`).

### Bietet an
- **Eigene DB-Tabelle:** `deployment_history` (Model `DeploymentHistory`) —
  protokolliert Techniker, System, alten/neuen Standort, Zeitstempel.
- **HTTP-Endpoints** (Auth via `@authenticated` + `@authorized("termgr")`):
  - `/administer/*` (POST): `deploy`, `fit`, `application`, `reboot`, `sync`,
    `beep`, `serial-number`, `testing`, `warranty`, `ddbos`, `processing`,
    `lpt-address/<deployment>`, `url/<deployment>`, `send-url/<system>`,
    `restart-web-browser`, `isvirtual`, `model`; sowie
    `GET /administer/get-url` (liefert `{ "url": ... }` — von digsigctl konsumiert).
  - `/setup/*`: `POST info`, `POST finalize`, `POST system`, `PATCH system`.
  - `/list/*` (GET): `customers` (Kunden mit Systemanzahl:
    `{"customers": [{"id", "abbreviation", "company": {"name"}, "systems"}], "systems"}`,
    äußeres `systems` = alle verwaltbaren Systeme, auch ohne Standort),
    `deployments`, `systems`, `systems/<ident>`.
  - zusätzlich Routen aus `ddbaccounts` und `dephist`.
- **Console-Scripts / Wartung:** `reload-terminals` schreibt WireGuard-Peers neu,
  `dephist`, `toggle-ddb-install-account`.

## Deployment / Laufzeit
WSGI-Anwendung (`APPLICATION` in `termgr/wsgi`), betrieben unter
`termgr.homeinfo.de`. Installation über `make install` (`setup.py install`),
XSD-Bindings über `make bindings` (`pyxbgen` aus `doc/terminals.xsd`).
⚠️ ANNAHME: Ausgeliefert per mod_wsgi/uwsgi hinter dem `his`-Stack; genauer
Webserver/Service-Setup nicht aus dem Repo ersichtlich (vermutlich zentral
in `homeinfo-architektur` bzw. Server-Konfiguration).

## Ersetzbarkeit
Kopplungsgrad: **hoch**. termgr ist tief in den gemeinsamen Homeinfo-Stack
integriert: Auth/HIS, `hwdb`-Datenmodell, geteilte MySQL-Instanz, WireGuard,
ACLs und eine ganze Reihe interner Bibliotheken. Ein Ersatz müsste dasselbe
Datenmodell, dieselben Endpoints (insb. `get-url` für digsigctl) und die
HIS-Authentifizierung nachbilden. Isoliert austauschbar ist praktisch nur die
eigene Tabelle `deployment_history`.

## Weitere Doku
- `README.md` (Kurzbeschreibung: Terminal-Management-Backend).
- `doc/terminals.xsd` (XML-Schema, Basis der pyxb-Bindings).
- Gegenstück-Repo (Geräte-Agent): https://github.com/homeinfogmbh/digsigctl
- ⚠️ ANNAHME: Zentrales Repo `homeinfo-architektur` (Ordner `komponenten/`) noch
  nicht geprüft — dort ggf. übergeordnete Doku ergänzen/verlinken.
