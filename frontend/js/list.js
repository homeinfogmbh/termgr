/*
    list.js - Terminal Manager systems listing.

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

import { konami } from 'https://javascript.homeinfo.de/konami.js';
import { logout } from './api.js';
import { system, systems } from './cache.js';
import { systemEntry } from './dom.js';
import { autoFilterSystems } from './filter.js';
import { suppressEvent } from './functions.js';
import * as loader from './loader.js';
import { sortSystems } from './sort.js';


/*
    Navigates to the management page.
*/
export function select (systemId) {
    system.set(systemId);
    window.location = 'manage.html';
}


/*
    Renders the respective systems.
*/
function render (systems) {
    const container = document.getElementById('systems');
    container.innerHTML = '';

    for (let i = 0; i < systems.length; i++) {
        let entry = systemEntry(systems[i], i);
        container.appendChild(entry);
    }
}


/*
    Loads, filters, sorts and renders systems.
*/
function list (force = false) {
    loader.start();
    return systems.getValue(force).then(
        autoFilterSystems).then(
        sortSystems).then(
        render).then(
        loader.stop
    );
}


/*
    Initialize list.html.
*/
export function init () {
    list();
    const btnLogout = document.getElementById('logout');
    btnLogout.addEventListener('click', suppressEvent(logout), false);
    const btnFilter = document.getElementById('filter');
    btnFilter.addEventListener('click', suppressEvent(list), false);
    const btnReload = document.getElementById('reload');
    btnReload.addEventListener('click', suppressEvent(list, true), false);
    const radioButtons = [
        document.getElementById('sortAsc'),
        document.getElementById('sortDesc'),
        document.getElementById('sortById'),
        document.getElementById('sortByAddress')
    ];

    for (const radioButton of radioButtons)
        radioButton.addEventListener('change', suppressEvent(list), false);

    // Konami Code easteregg.
    document.addEventListener('keydown', konami);
}
