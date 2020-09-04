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
termgr.manage = {};


/*
    Navigates to the toggle application page.
*/
termgr.manage.application = function (system) {
    termgr.storage.system.set(system);
    window.location = 'application.html';
};


/*
    Opens the deploying view.
*/
termgr.manage.deploy = function (system) {
    termgr.storage.system.set(system);
    window.location = 'deploy.html';
};


/*
    Reloads the systems.
*/
termgr.manage.reload = function () {
    termgr.loader.start();
    return termgr.api.getSystems().then(termgr.manage.list).then(termgr.loader.stop);
};


/*
    Renders the respective systems.
*/
termgr.manage.render = function (systems) {
    const container = document.getElementById('systems');
    container.innerHTML = '';

    for (const system of systems) {
        let entry = termgr.dom.systemEntry(system);
        container.appendChild(entry);
    }
};


/*
    Filters, sorts and renders systems.
*/
termgr.manage.list = function (systems) {
    if (systems == null) {
        termgr.loader.start();
        systems = termgr.storage.systems.get();
    }

    systems = termgr.filter.systems(systems);
    systems = termgr.sort.systems(systems);
    termgr.manage.render(systems);
    termgr.loader.stop();
};


/*
    Initialize manage.html.
*/
termgr.manage.init = function () {
    termgr.loader.start();
    termgr.manage.reload().then(termgr.loader.stop);
    const btnFilter = document.getElementById('filter');
    btnFilter.addEventListener('click', termgr.partial(termgr.manage.list), false);
    const btnReload = document.getElementById('reload');
    btnReload.addEventListener('click', termgr.partial(termgr.manage.reload), false);
    const radioButtons = [
        document.getElementById('sortAsc'),
        document.getElementById('sortDesc'),
        document.getElementById('sortById'),
        document.getElementById('sortByAddress')
    ];

    for (const radioButton of radioButtons)
        radioButton.addEventListener('change', termgr.partial(termgr.manage.list), false);
};


document.addEventListener('DOMContentLoaded', termgr.manage.init);
