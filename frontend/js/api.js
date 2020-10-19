/*
    api.js - Terminal Manager API library.

    (C) 2019 HOMEINFO - Digitale Informationssysteme GmbH

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
    Function to make a request and display an error message on error.
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
    Performs a login.
*/
termgr.api.login = function (account, passwd) {
    const payload = {'account': account, 'passwd': passwd};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.api.makeRequest('POST', 'https://his.homeinfo.de/session', data, headers).then(
        function () {
            window.location = 'manage.html';
        },
        function () {
            alert('Ungültiger Benutzername und / oder Passwort.');
        }
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
    const payload = {'system': system, 'state': state};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    const stateText = state ? 'aktiviert' : 'deaktiviert';
    return termgr.api.makeRequest('POST', termgr.api.BASE_URL + '/administer/application', data, headers).then(
        function () {
            alert('Digital Signage Anwendung wurde ' + stateText + '.');
        },
        termgr.api.checkSession('Digital Signage Anwendung konnte nicht ' + stateText + ' werden.')
    );
};


/*
    Deploys a system.
*/
termgr.api.deploy = function (system, deployment, exclusive = false) {
    const payload = {
        system: system,
        deployment: deployment,
        exclusive: exclusive
    };
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.api.makeRequest('POST', termgr.api.BASE_URL + '/administer/deploy', data, headers).then(
        function () {
            alert('Das System wurde als verbaut gekennzeichnet.');
        },
        termgr.api.checkSession('Das System konnte nicht als verbaut gekennzeichnet werden.')
    );
};


/*
    Lets the respective system beep.
*/
termgr.api.beep = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.api.makeRequest('POST', termgr.api.BASE_URL + '/administer/beep', data, headers).then(
        function () {
            alert('Das System sollte gepiept haben.');
        },
        termgr.api.checkSession('Das System konnte nicht zum Piepen gebracht werden.')
    );
};


/*
    Actually performs a reboot of the respective system.
*/
termgr.api.reboot = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.api.makeRequest('POST', termgr.api.BASE_URL + '/administer/reboot', data, headers).then(
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
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.api.makeRequest('POST', termgr.api.BASE_URL + '/administer/sync', data, headers).then(
        function () {
            alert('Das System wird demnächst synchronisiert.');
        },
        termgr.api.checkSession('Das System konnte nicht synchronisiert werden.')
    );
};
