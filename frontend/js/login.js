/*
    login.js - Terminal Manager login handling.

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
termgr.login = {};


/*
    Performs the initial login.
*/
termgr.login.login = function () {
    const account = document.getElementById('account').value;
    const passwd = document.getElementById('passwd').value;
    const storeCredentials = document.getElementById('storeCredentials').checked;

    if (storeCredentials)
        termgr.storage.credentials.set(account, passwd);
    else
        termgr.storage.credentials.clear();

    return termgr.api.login(account, passwd);
};


/*
    Initialize index.html.
*/
termgr.login.init = function () {
    const loginButton = document.getElementById('login');
    loginButton.addEventListener('click', termgr.partial(termgr.login.login), false);
};


document.addEventListener('DOMContentLoaded', termgr.login.init);
