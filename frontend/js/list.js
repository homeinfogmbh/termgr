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


var termgr = termgr || {};
termgr.list = {};


/*
    Navigates to the management page.
*/
termgr.list.select = function (system) {
    termgr.cache.system.set(system);
    window.location = 'manage.html';
};


/*
    Renders the respective systems.
*/
termgr.list.render = function (systems) {
    const container = document.getElementById('systems');
    container.innerHTML = '';

    for (let i = 0; i < systems.length; i++) {
        let entry = termgr.dom.systemEntry(systems[i], i);
        container.appendChild(entry);
    }
};


/*
    Loads, filters, sorts and renders systems.
*/
termgr.list.list = function (force = false) {
    termgr.loader.start();
    return termgr.cache.systems.getValue(force).then(
        termgr.filter.systems).then(
        termgr.sort.systems).then(
        termgr.list.render).then(
        termgr.loader.stop
    );
};


/*
    Initialize list.html.
*/
termgr.list.init = function () {
    termgr.list.list();
    const btnLogout = document.getElementById('logout');
    btnLogout.addEventListener('click', termgr.partial(termgr.api.logout), false);
    const btnFilter = document.getElementById('filter');
    btnFilter.addEventListener('click', termgr.partial(termgr.list.list), false);
    const btnReload = document.getElementById('reload');
    btnReload.addEventListener('click', termgr.partial(termgr.list.list, true), false);
    const radioButtons = [
        document.getElementById('sortAsc'),
        document.getElementById('sortDesc'),
        document.getElementById('sortById'),
        document.getElementById('sortByAddress')
    ];

    for (const radioButton of radioButtons)
        radioButton.addEventListener('change', termgr.partial(termgr.list.list), false);
};


document.addEventListener('DOMContentLoaded', termgr.list.init);
