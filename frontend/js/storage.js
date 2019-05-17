/*
    storage.js - Terminal Manager local storage handling.

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
    Stores account name and password.
*/
termgr.storeCredentials = function (account, passwd) {
    localStorage.setItem('termgr.account', account);
    localStorage.setItem('termgr.passwd', passwd);
};


/*
    Returns account name and password from local storage.
*/
termgr.getCredentials = function () {
    const account = localStorage.getItem('termgr.account');
    const passwd = localStorage.getItem('termgr.passwd');
    return [account, passwd];
};


/*
    Removes account name and password from local storage.
*/
termgr.clearCredentials = function () {
    localStorage.removeItem('termgr.account');
    localStorage.removeItem('termgr.passwd');
};


/*
    Stores the deployments in local storage.
*/
termgr.storeDeployments = function (deployments) {
    deployments = Array.from(deployments);
    const json = JSON.stringify(deployments);
    return localStorage.setItem('termgr.deployments', json);
};


/*
    Loads the deployments from local storage.
*/
termgr.loadDeployments = function () {
    const raw = localStorage.getItem('termgr.deployments');

    if (raw == null) {
        return [];
    }

    return JSON.parse(raw);
};


/*
    Stores the systems in local storage.
*/
termgr.storeSystems = function (systems) {
    systems = Array.from(systems);
    const json = JSON.stringify(systems);
    return localStorage.setItem('termgr.systems', json);
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
