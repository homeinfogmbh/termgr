/*
    autologin.js - Terminal Manager automatic login.

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
termgr.autologin = {};


/*
    Initialize index.html.
*/
termgr.autologin.init = function () {
    const [account, passwd] = termgr.cache.credentials.get();

    if (account == null || passwd == null) {
        window.location = 'login.html';
    } else {
        termgr.api.login(account, passwd).then(
            function () {
                window.location = 'list.html';
            },
            function () {
                window.location = 'login.html';
            }
        );
    }
};


document.addEventListener('DOMContentLoaded', termgr.autologin.init);
