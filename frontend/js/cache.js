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


export const deployments = new Cache('termgr.deployments', getDeployments);
export const system = new JSONStorage('termgr.system');     // System ID.
export const systems = new Cache('termgr.systems', getSystems);


/*
    Clears all storage items.
*/
export function clear () {
    deployments.clear();
    system.clear();
    systems.clear();
};
