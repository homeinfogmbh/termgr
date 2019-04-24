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


/*
    Reloads the systems.
*/
function reload () {
    termgr.startLoading();
    return termgr.getSystems().then(termgr.listFilteredSystems).then(termgr.stopLoading);
}


/*
    Initialize manage.html.
*/
function init () {
    termgr.startLoading();
    reload().then(termgr.stopLoading);
    const btnFilter = document.getElementById('filter');
    btnFilter.addEventListener('click', termgr.partial(termgr.listFilteredSystems), false);
    const btnReload = document.getElementById('reload');
    btnReload.addEventListener('click', termgr.partial(reload), false);
}


document.addEventListener('DOMContentLoaded', init);
