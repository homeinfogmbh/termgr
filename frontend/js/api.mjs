/*
    api.mjs - Terminal Manager API library.

    (C) 2019-2021 HOMEINFO - Digitale Informationssysteme GmbH

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Maintainer: Richard Neumann <r dot neumann at homeinfo period de>
*/
'use strict';

import * as session from 'https://javascript.homeinfo.de/his/session.mjs';
import { request } from 'https://javascript.homeinfo.de/his/his.mjs';
import { clear, system } from './cache.mjs';

export const BASE_URL = 'https://termgr.homeinfo.de';
const SESSION_DURATION = 90;
const HEADERS = {'session-duration': SESSION_DURATION};


/*
    Checks whether an error occured due to an expired
    session or displays the given error message otherwise.
*/
function checkSession (message) {
    return function (response) {
        if (response.status == 401 || response.message == 'Session expired.') {
            alert('Sitzung abgelaufen.');
            window.location = 'index.html';
        } else {
            alert(message);
        }
    };
}


/*
    Performs a HIS SSO login.
*/
export function login (account, passwd) {
    return session.login(account, passwd, null, HEADERS).then(
        function () {
            window.location = 'list.html';
        },
        function () {
            alert('Ungültiger Benutzername und / oder Passwort.');
        }
    );
}


/*
    Performs a HIS SSO logout.
*/
export function logout () {
    return session.close().then(
        function () {
            clear();
            window.location = 'index.html';
        },
        checkSession('Logout konnte nicht durchgeführt werden.')
    );
}


/*
    Retrieves deployments from the API.
*/
export function getDeployments () {
    return request.get(BASE_URL + '/list/deployments', null, HEADERS).then(
        response => response.json,
        checkSession('Die Liste der Standorte konnte nicht abgerufen werden.')
    );
}


/*
    Retrieves a specific system from the API.
*/
export function getSystem (id) {
    if (id == null)
        id = system.get();

    if (id == null)
        return Promise.reject('Kein System angegeben.');

    return request.get(BASE_URL + '/list/systems/' + id, null, HEADERS).then(
        response => response.json,
        checkSession('Das angegebene System konnte nicht abgerufen werden.')
    );
}


/*
    Retrieves systems from the API.
*/
export function getSystems () {
    return request.get(BASE_URL + '/list/systems', null, HEADERS).then(
        response => response.json,
        checkSession('Die Liste der Systeme konnte nicht abgerufen werden.')
    );
}


/*
    Enables or disables the application.
*/
export function application (system, state) {
    const stateText = state ? 'aktiviert' : 'deaktiviert';
    const json = {'system': system, 'state': state};
    return request.post(BASE_URL + '/administer/application', json, null, HEADERS).then(
        function () {
            alert('Digital Signage Anwendung wurde ' + stateText + '.');
        },
        checkSession('Digital Signage Anwendung konnte nicht ' + stateText + ' werden.')
    );
}


/*
    Deploys a system.
*/
export function deploy (system, deployment, exclusive = false, fitted = false) {
    const stateTexts = ['Der Standort wurde gesetzt.'];

    if (exclusive)
        stateTexts.push('Andere Systeme wurden vom Standort entfernt.');

    if (fitted)
        stateTexts.push('Das System wurde als verbaut markiert.');

    const json = {
        'system': system,
        'deployment': deployment,
        'exclusive': exclusive,
        'fitted': fitted
    };
    return request.post(BASE_URL + '/administer/deploy', json, null, HEADERS).then(
        function () {
            alert(stateTexts.join('\n'));
        },
        checkSession('Das System konnte nicht als verbaut gekennzeichnet werden.')
    );
}


/*
    Deploys a system.
*/
export function fit (system, fitted = true) {
    const stateText = fitted ? 'verbaut' : 'nicht verbaut';
    const json = {'system': system, 'fitted': fitted};
    return request.post(BASE_URL + '/administer/fit', json, null, HEADERS).then(
        function () {
            alert('Das System wurde als ' + stateText + ' gekennzeichnet.');
        },
        checkSession('Das System konnte nicht als "' + stateText + '" gekennzeichnet werden.')
    );
}


/*
    Lets the respective system beep.
*/
export function beep (system) {
    const json = {'system': system};
    return request.post(BASE_URL + '/administer/beep', json, null, HEADERS).then(
        function () {
            alert('Das System sollte gepiept haben.');
        },
        checkSession('Das System konnte nicht zum Piepen gebracht werden.')
    );
}


/*
    Reboots the respective system.
*/
export function reboot (system) {
    const json = {'system': system};
    return request.post(BASE_URL + '/administer/reboot', json, null, HEADERS).then(
        function () {
            alert('Das System wurde wahrscheinlich neu gestartet.');
        },
        function (response) {
            let message = 'Das System konnte nicht neu gestartet werden.';

            if (response.status == 503)
                message = 'Auf dem System werden aktuell administrative Aufgaben ausgeführt.';

            return checkSession(message)(response);
        }
    );
}


/*
    Synchronizes the respective system.
*/
export function sync (system) {
    const json = {'system': system};
    return request.post(BASE_URL + '/administer/sync', json, null, HEADERS).then(
        function () {
            alert('Das System wird demnächst synchronisiert.');
        },
        checkSession('Das System konnte nicht synchronisiert werden.')
    );
}
