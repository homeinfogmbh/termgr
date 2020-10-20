/*
    api.js - Terminal Manager API library.

    (C) 2019-2020 HOMEINFO - Digitale Informationssysteme GmbH

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


var termgr = termgr ||  {};
termgr.api = {};

termgr.api.BASE_URL = 'https://termgr.homeinfo.de';
termgr.api.LOGIN_URL ='https://his.homeinfo.de/session'


/*
  Makes a request returning a promise.
*/
termgr.api.makeRequest = function (method, url, data = null, headers = {}) {
    function parseResponse (response) {
        try {
            return JSON.parse(response);
        } catch (error) {
            return response;
        }
    }

    function executor (resolve, reject) {
        function onload () {
            if (this.status >= 200 && this.status < 300)
                resolve({
                    response: xhr.response,
                    json: parseResponse(xhr.response),
                    status: this.status,
                    statusText: xhr.statusText
                });
            else
                reject({
                    response: xhr.response,
                    json: parseResponse(xhr.response),
                    status: this.status,
                    statusText: xhr.statusText
                });
        }

        function onerror () {
            reject({
                response: xhr.response,
                json: parseResponse(xhr.response),
                status: this.status,
                statusText: xhr.statusText
            });
        }

        const xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.open(method, url);

        for (const header in headers)
            xhr.setRequestHeader(header, headers[header]);

        xhr.onload = onload;
        xhr.onerror = onerror;

        if (data == null)
            xhr.send();
        else
            xhr.send(data);
    }

    return new Promise(executor);
};


/*
    Makes a JSON POST request.
*/
termgr.api.postJSON = function (url, json, headers = {}) {
    headers['Content-Type'] = 'application/json';
    return termgr.api.makeRequest('POST', url, JSON.stringify(json), headers);
}


/*
    Checks whether an error occured due to an expired
    session or displays the given error message otherwise.
*/
termgr.api.checkSession = function (message) {
    return function (response) {
        if (response.status == 401 || response.message == 'Session expired.') {
            alert('Sitzung abgelaufen.');
            window.location = 'index.html';
        } else {
            alert(message);
        }
    };
};


/*
    Performs a HIS SSO login.
*/
termgr.api.login = function (account, passwd) {
    const json = {'account': account, 'passwd': passwd};
    return termgr.api.postJSON(termgr.api.LOGIN_URL, json).then(
        function () {
            window.location = 'list.html';
        },
        function () {
            alert('Ungültiger Benutzername und / oder Passwort.');
        }
    );
};


/*
    Performs a HIS SSO logout.
*/
termgr.api.logout = function () {
    return termgr.api.makeRequest('DELETE', termgr.api.LOGIN_URL + '/!').then(
        function () {
            termgr.storage.clear();
            window.location = 'login.html';
        },
        termgr.api.checkSession('Logout konnte nicht durchgeführt werden.')
    );
};


/*
    Retrieves deployments from the API.
*/
termgr.api.getDeployments = function () {
    return termgr.api.makeRequest('GET', termgr.api.BASE_URL + '/list/deployments').then(
        function (response) {
            const deployments = response.json;
            termgr.storage.deployments.set(deployments);
            return deployments;
        },
        termgr.api.checkSession('Die Liste der Standorte konnte nicht abgefragt werden.')
    );
};


/*
    Retrieves systems from the API.
*/
termgr.api.getSystems = function () {
    return termgr.api.makeRequest('GET', termgr.api.BASE_URL + '/list/systems').then(
        function (response) {
            const systems = response.json;
            termgr.storage.systems.set(systems);
            return systems;
        },
        termgr.api.checkSession('Die Liste der Systeme konnte nicht abgefragt werden.')
    );
};


termgr.api.application = {};


/*
    Enables or disables the application.
*/
termgr.api.application = function (system, state) {
    const stateText = state ? 'aktiviert' : 'deaktiviert';
    const json = {'system': system, 'state': state};
    return termgr.api.postJSON(termgr.api.BASE_URL + '/administer/application', json).then(
        function () {
            alert('Digital Signage Anwendung wurde ' + stateText + '.');
        },
        termgr.api.checkSession('Digital Signage Anwendung konnte nicht ' + stateText + ' werden.')
    );
};


/*
    Deploys a system.
*/
termgr.api.deploy = function (system, deployment, exclusive = false, fitted = false) {
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
    return termgr.api.postJSON(termgr.api.BASE_URL + '/administer/deploy', json).then(
        function () {
            alert(stateTexts.join('\n'));
        },
        termgr.api.checkSession('Das System konnte nicht als verbaut gekennzeichnet werden.')
    );
};


/*
    Deploys a system.
*/
termgr.api.fit = function (system, fitted = true) {
    const stateText = fitted ? 'verbaut' : 'nicht verbaut';
    const json = {'system': system, 'fitted': fitted};
    return termgr.api.postJSON(termgr.api.BASE_URL + '/administer/fit', json).then(
        function () {
            alert('Das System wurde als ' + stateText + ' gekennzeichnet.');
        },
        termgr.api.checkSession('Das System konnte nicht als verbaut gekennzeichnet werden.')
    );
};


/*
    Lets the respective system beep.
*/
termgr.api.beep = function (system) {
    const json = {'system': system};
    return termgr.api.postJSON(termgr.api.BASE_URL + '/administer/beep', json).then(
        function () {
            alert('Das System sollte gepiept haben.');
        },
        termgr.api.checkSession('Das System konnte nicht zum Piepen gebracht werden.')
    );
};


/*
    Reboots the respective system.
*/
termgr.api.reboot = function (system) {
    const json = {'system': system};
    return termgr.api.postJSON(termgr.api.BASE_URL + '/administer/reboot', json).then(
        function () {
            alert('Das System wurde wahrscheinlich neu gestartet.');
        },
        function (response) {
            let message = 'Das System konnte nicht neu gestartet werden.';

            if (response.status == 503)
                message = 'Auf dem System werden aktuell administrative Aufgaben ausgeführt.';

            return termgr.api.checkSession(message)(response);
        }
    );
};


/*
    Synchronizes the respective system.
*/
termgr.api.sync = function (system) {
    const json = {'system': system};
    return termgr.api.postJSON(termgr.api.BASE_URL + '/administer/sync', json).then(
        function () {
            alert('Das System wird demnächst synchronisiert.');
        },
        termgr.api.checkSession('Das System konnte nicht synchronisiert werden.')
    );
};
