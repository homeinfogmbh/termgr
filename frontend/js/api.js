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


var termgr = termgr || {};


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
    Retrieves deployments from the API.
*/
termgr.getDeployments = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list/deployments').then(
        function (response) {
            const deployments = response.json;
            termgr.storeDeployments(deployments);
            return deployments;
        },
        termgr.checkSession('Die Liste der Standorte konnte nicht abgefragt werden.')
    );
};


/*
    Retrieves systems from the API.
*/
termgr.getSystems = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list/systems').then(
        function (response) {
            const systems = response.json;
            termgr.storeSystems(systems);
            return systems;
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
