/*
    manage.js - Terminal Manager systems listing.

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
termgr.toggleApplication = function (system) {
    termgr.storage.system.set(system);
    window.location = 'application.html';
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
            alert('Das System wird demnächst synchronisiert.');
        },
        termgr.checkSession('Das System konnte nicht synchronisiert werden.')
    );
};


/*
    Opens the deploying view.
*/
termgr.deploySystem = function (system) {
    termgr.storage.system.set(system);
    window.location = 'deploy.html';
};


/*
    Reloads the systems.
*/
termgr.reloadSystems = function () {
    termgr.startLoading();
    return termgr.getSystems().then(termgr.listSystems).then(termgr.stopLoading);
};


/*
    Filters, sorts and renders systems.
*/
termgr.listSystems = function (systems) {
    if (systems == null) {
        termgr.startLoading();
        systems = termgr.storage.systems.load();
    }

    systems = termgr.filteredSystems(systems);
    systems = termgr.sortedSystems(systems);
    termgr.renderSystems(systems);
    termgr.stopLoading();
};


/*
    Initialize manage.html.
*/
function init () {
    termgr.startLoading();
    termgr.reloadSystems().then(termgr.stopLoading);
    const btnFilter = document.getElementById('filter');
    btnFilter.addEventListener('click', termgr.partial(termgr.listSystems), false);
    const btnReload = document.getElementById('reload');
    btnReload.addEventListener('click', termgr.partial(termgr.reloadSystems), false);
    const radioButtons = [
        document.getElementById('sortAsc'),
        document.getElementById('sortDesc'),
        document.getElementById('sortById'),
        document.getElementById('sortByAddress')
    ];

    for (const radioButton of radioButtons) {
        radioButton.addEventListener('change', termgr.partial(termgr.listSystems), false);
    }
}


document.addEventListener('DOMContentLoaded', init);
