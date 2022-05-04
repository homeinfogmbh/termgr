/*
    list.mjs - Terminal Manager systems listing.

    (C) 2019-2021 HOMEINFO - Digitale Informationssysteme GmbH

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

import * as konami from 'https://javascript.homeinfo.de/konami.mjs';
import { Loader, enumerate, suppressEvent } from 'https://javascript.homeinfo.de/lib.mjs';
import { logout } from './api.mjs';
import { system, systems } from './cache.mjs';
import { systemEntry } from './dom.mjs';
import { autoFilterSystems } from './filter.mjs';
import { sortSystems } from './sort.mjs';


/*
    Initialize list.html.
*/
export function init () {
    list();
    document.getElementById('filter').addEventListener(
        'click', suppressEvent(list), false
    );
    document.getElementById('reload').addEventListener(
        'click', suppressEvent(list, true), false
    );
    document.getElementById('logout').addEventListener(
        'click', suppressEvent(logout), false
    );
    document.getElementById('idmap').addEventListener(
        'click', suppressEvent(idmap), false
    );

    for (const radioButton of getRadioButtons())
        radioButton.addEventListener('change', suppressEvent(list), false);

    konami.init();  // Konami Code easter egg.
}


/*
    Navigates to the management page.
*/
export function select (systemId) {
    system.set(systemId);
    window.location = 'manage.html';
}


/*
    Navigates to the ID mapper page.
*/
function idmap () {
    window.location = 'idmap.html';
}


/*
    Renders the respective systems.
*/
function render (systems) {
    const container = document.getElementById('systems');
    container.innerHTML = '';
    let index, system;

    for ([index, system] of enumerate(systems))
        container.appendChild(systemEntry(system, index));
}


/*
    Loads, filters, sorts and renders systems.
*/
function list (force = false) {
    return Loader.wrap(
        systems.get(force).then(
        autoFilterSystems).then(
        sortSystems).then(
        render)
    );
}


/*
    Return a list of radio buttons.
*/
function getRadioButtons () {
    return [
        document.getElementById('sortAsc'),
        document.getElementById('sortDesc'),
        document.getElementById('sortById'),
        document.getElementById('sortByAddress')
    ];
}
