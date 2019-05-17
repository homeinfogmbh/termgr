/*
    application.js - Terminal Manager application toggleing.

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
    Enables the application.
*/
termgr.enableApplication = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/application', data, headers).then(
        function () {
            alert('Digital Signage Anwendung wurde aktiviert.');
        },
        termgr.checkSession('Digital Signage Anwendung konnte nicht aktiviert werden.')
    );
};


/*
    Disables the application.
*/
termgr.disableApplication = function (system) {
    const payload = {'system': system, 'disable': true};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/application', data, headers).then(
        function () {
            alert('Digital Signage Anwendung wurde deaktiviert.');
        },
        termgr.checkSession('Digital Signage Anwendung konnte nicht deaktiviert werden.')
    );
};


/*
    Initialize manage.html.
*/
function init () {
    const id = JSON.parse(localStorage.getItem('termgr.system'));
    const btnEnable = document.getElementById('enable');
    btnEnable.addEventListener('click', termgr.partial(termgr.enableApplication, id), false);
    const btnDisable = document.getElementById('disable');
    btnDisable.addEventListener('click', termgr.partial(termgr.disableApplication, id), false);
    const systemId = document.getElementById('system');
    systemId.textContent = id;
}


document.addEventListener('DOMContentLoaded', init);
