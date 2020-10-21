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

import { Cache } from 'https://javascript.homeinfo.de/caching.js';
import { getDeployments, getSystems } from './api.js';


/*
    Account name and password storage.
*/

export const credentials = {
    set: function (account, passwd) {
        localStorage.setItem('termgr.account', account);
        localStorage.setItem('termgr.passwd', passwd);
    },
    get: function () {
        const account = localStorage.getItem('termgr.account');
        const passwd = localStorage.getItem('termgr.passwd');
        return [account, passwd];
    },
    clear: function () {
        localStorage.removeItem('termgr.account');
        localStorage.removeItem('termgr.passwd');
    }
};


export const deployments = new Cache('termgr.deployments', getDeployments);
export const systems = new Cache('termgr.systems', getSystems);


/*
    Current system ID handling.
*/
export const system = {
    set: function (system) {
        localStorage.setItem('termgr.system', JSON.stringify(system));
    },
    get: function () {
        const raw = localStorage.getItem('termgr.system');

        if (raw == null)
            return null;

        return JSON.parse(raw);
    },
    clear: function () {
        localStorage.removeItem('termgr.system');
    }
};


/*
    Clears all storage items.
*/
export function clear () {
    credentials.clear();
    deployments.clear();
    systems.clear();
    system.clear();
};
