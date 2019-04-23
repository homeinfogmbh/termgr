/*
    termgr.js - Terminal Manager front end JavaScript library.

    (C) 2018 HOMEINFO - Digitale Informationssysteme GmbH

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
    Performs the initial login.
*/
termgr.login = function (event) {
    event.preventDefault();
    const account = document.getElementById('userName').value;
    const passwd = document.getElementById('passwd').value;
    const payload = {'account': account, 'passwd': passwd};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', 'https://his.homeinfo.de/session', data, headers).then(
        function () {
            window.location = 'manage.html';
        },
        function () {
            alert('Ungültiger Benutzername und / oder Passwort.');
        }
    );
};


/*
    Initialize index.html.
*/
function init () {
    const loginButton = document.getElementById('login');
    loginButton.addEventListener('click', termgr.login, false);
}


document.addEventListener('DOMContentLoaded', init);
