/*
    functions.js - Terminal Manager functions library.

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


var termgr = termgr || {};


/*
    Starts loading.
*/
termgr.startLoading = function () {
    const loader = document.getElementById('loader');
    const target = document.getElementById('target');
    target.style.display = 'none';
    loader.style.display = 'block';
};


/*
    Stops loading.
*/
termgr.stopLoading = function () {
    const loader = document.getElementById('loader');
    const target = document.getElementById('target');
    loader.style.display = 'none';
    target.style.display = 'block';
};


/*
    Stores the systems in local storage.
*/
termgr.storeSystems = function (systems) {
    return localStorage.setItem('termgr.systems', JSON.stringify(systems));
};


/*
    Loads the systems from local storage.
*/
termgr.loadSystems = function () {
    const raw = localStorage.getItem('termgr.systems');

    if (raw == null) {
        return [];
    }

    return JSON.parse(raw);
};


/*
    Performs a login.
*/
termgr.login = function (account, passwd) {
    const payload = {'account': account, 'passwd': passwd};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', 'https://his.homeinfo.de/session', data, headers).then(
        function () {
            window.location = 'manage.html';
        },
        function () {
            alert('Ungültiger Benutzername und / oder Passwort.');
        }
    );
};


/*
    Retrieves systems from the API.
*/
termgr.getSystems = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list/systems').then(
        function (response) {
            termgr.storeSystems(response.json);
        },
        termgr.checkSession('Die Liste der Systeme konnte nicht abgefragt werden.')
    );
};


/*
    Retrieves customers from the backend,
    which the current user is allowed to deploy to.
*/
termgr.getCustomers = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list/customers').catch(
        termgr.checkSession('Die Liste der Kunden konnte nicht abgefragt werden.')
    );
};


/*
    Retrieves connections from the backend.
*/
termgr.getConnections = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list/connections').catch(
        termgr.checkSession('Die Liste der Internetverbindungen konnte nicht abgefragt werden.')
    );
};


/*
    Retrieves types from the backend.
*/
termgr.getTypes = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list/types').catch(
        termgr.checkSession('Die Liste der Terminal-Typen konnte nicht abgefragt werden.')
    );
};


/*
    Lists the respective systems.
*/
termgr.listSystems = function (systems) {
    const container = document.getElementById('systems');
    container.innerHTML = '';

    for (const system of systems) {
        let entry = termgr.systemEntry(system);
        container.appendChild(entry);
    }
};


/*
    Renders the respective customers.
*/
termgr.renderCustomers = function (customers) {
    const select = document.getElementById('customer');
    select.innerHTML = '';

    for (const customer of customers) {
        let option = document.createElement('option');
        option.setAttribute('value', customer.id);
        option.textContent = customer.company.name;
        select.appendChild(option);
    }
};


/*
    Renders the respective connections.
*/
termgr.renderConnections = function (connections) {
    const select = document.getElementById('connection');
    select.innerHTML = '';

    for (const connection of connections) {
        let option = document.createElement('option');
        option.setAttribute('value', connection);
        option.textContent = connection;
        select.appendChild(option);
    }
};


/*
    Renders the respective types.
*/
termgr.renderTypes = function (types) {
    const select = document.getElementById('type');
    select.innerHTML = '';

    for (const type of types) {
        let option = document.createElement('option');
        option.setAttribute('value', type);
        option.textContent = type;
        select.appendChild(option);
    }
};


/*
    Function to wrap a function and disable default events.
*/
termgr.partial = function (func, ...args) {
    return function (event) {
        if (event != null) {
            event.preventDefault();
        }

        return func(...args);
    };
};


/*
    Lets the respective system beep.
*/
termgr.beep = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/beep', data, headers).then(
        function () {
            alert('Das System sollte gepiept haben.');
        },
        termgr.checkSession('Das System konnte nicht zum Piepen gebracht werden.')
    );
};


/*
    Actually performs a reboot of the respective system.
*/
termgr.reboot = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/reboot', data, headers).then(
        function () {
            alert('Das System wurde wahrscheinlich neu gestartet.');
        },
        function (response) {
            let message = 'Das System konnte nicht neu gestartet werden.';

            if (response.status == 503) {
                message = 'Auf dem System werden aktuell administrative Aufgaben ausgeführt.';
            }

            return termgr.checkSession(message)(response);
        }
    );
};


/*
    Navigates to the toggle application page.
*/
termgr.toggleApplication = function (id) {
    localStorage.setItem('termgr.system', JSON.stringify(id));
    window.location = 'application.html';
};


/*
    Enables the application.
*/
termgr.enableApplication = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/application', data, headers).then(
        function () {
            alert('Digital Signage Anwendung wurde aktiviert.');
        },
        termgr.checkSession('Digital Signage Anwendung konnte nicht aktiviert werden.')
    );
};


/*
    Disables the application.
*/
termgr.disableApplication = function (system) {
    const payload = {'system': system, 'disable': true};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/application', data, headers).then(
        function () {
            alert('Digital Signage Anwendung wurde deaktiviert.');
        },
        termgr.checkSession('Digital Signage Anwendung konnte nicht deaktiviert werden.')
    );
};


/*
    Synchronizes the respective system.
*/
termgr.sync = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/sync', data, headers).then(
        function () {
            alert('Das System wurde synchronisiert.');
        },
        termgr.checkSession('Das System konnte nicht synchronisiert werden.')
    );
};



/*
    Opens the deploying view.
*/
termgr.deploySystem = function (id) {
    localStorage.setItem('termgr.system', JSON.stringify(id));
    window.location = 'deploy.html';
};


/*
    Deploys a system.
*/
termgr.deploy = function (system, customer, address, connection, type, weather, annotation) {
    const payload = {
        system: system,
        customer: customer,
        address: address,
        connection: connection,
        type: type,
        weather: weather,
        annotation: annotation
    };
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/deploy', data, headers).then(
        function () {
            alert('Das System wurde als verbaut gekennzeichnet.');
        },
        termgr.checkSession('Das System konnte nicht als verbaut gekennzeichnet werden.')
    );
};
