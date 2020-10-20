/*
    cache.js - Terminal Manager local storage caching.

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


var termgr = termgr || {};
termgr.cache = {};


/*
    Account name and password storage.
*/

termgr.cache.credentials = {};

termgr.cache.credentials.set = function (account, passwd) {
    localStorage.setItem('termgr.account', account);
    localStorage.setItem('termgr.passwd', passwd);
};

termgr.cache.credentials.get = function () {
    const account = localStorage.getItem('termgr.account');
    const passwd = localStorage.getItem('termgr.passwd');
    return [account, passwd];
};

termgr.cache.credentials.clear = function () {
    localStorage.removeItem('termgr.account');
    localStorage.removeItem('termgr.passwd');
};


termgr.cache.deployments = new homeinfo.caching.Cache('termgr.deployments', termgr.api.getDeployments);
termgr.cache.systems = new homeinfo.caching.Cache('termgr.systems', termgr.api.getSystems);


/*
    Current system ID handling.
*/
termgr.cache.system = {};

termgr.cache.system.set = function (system) {
    localStorage.setItem('termgr.system', JSON.stringify(system));
};

termgr.cache.system.get = function () {
    const raw = localStorage.getItem('termgr.system');

    if (raw == null)
        return null;

    return JSON.parse(raw);
};

termgr.cache.system.clear = function () {
    localStorage.removeItem('termgr.system');
};


/*
    Clears all storage items.
*/
termgr.cache.clear = function () {
    termgr.cache.credentials.clear();
    termgr.cache.deployments.clear();
    termgr.cache.systems.clear();
    termgr.cache.system.clear();
};
