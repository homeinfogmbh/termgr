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


termgr.cache.update = function (cache) {
    return function (value) {
        const now = new Date();
        const json = {'timestamp': now.toString(), 'value': value};
        const raw = JSON.stringify(json);
        localStorage.setItem(cache.key, raw);
        return json;
    };
};


/*
    JSON data cache.
*/
termgr.cache.Cache = class {
    constructor (key, refreshFunction, lifetime = 3600000) {
        this.key = key;
        this.refreshFunction = refreshFunction;
        this.lifetime = lifetime;
    }

    get value () {
        return this.getValue();
    }

    get timestamp () {
        return this.getTimestamp();
    }

    refresh () {
        return this.refreshFunction().then(termgr.cache.update(this));
    }

    load (force = false) {
        if (force) {
            this.log('Forcing load.');
            return this.refresh();
        }

        const raw = localStorage.getItem(this.key);

        if (raw == null) {
            this.log('Empty cache.');
            return this.refresh();
        }

        let json;

        try {
            json = JSON.parse(raw);
        } catch (error) {
            this.log('Invalid cache content.');
            return this.refresh();
        }

        const timestamp = Date.parse(json['timestamp']);
        const now = new Date();

        if ((now - timestamp) < this.lifetime) {
            this.log('Cache miss.');
            return this.refresh();
        }

        return Promise.resolve(json);
    }

    getValue (force = false) {
        return this.load(force).then(json => json['value']);
    }

    getTimestamp (force = false) {
        return this.load(force).then(json => json['timestamp']);
    }

    clear () {
        localStorage.removeItem(this.key);
    }

    log (message, prefix = '[INFO]') {
        console.log(prefix + ' cache "' + this.key + '": ' + message);
    }
};


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


termgr.cache.deployments = new termgr.cache.Cache('termgr.deployments', termgr.api.getDeployments);
termgr.cache.systems = new termgr.cache.Cache('termgr.systems', termgr.api.getSystems);


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
