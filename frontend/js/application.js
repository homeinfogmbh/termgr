/*
    application.js - Terminal Manager application toggleing.

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
termgr.application = {};


/*
    Initialize manage.html.
*/
termgr.application.init = function () {
    const system = termgr.storage.system.get();
    const systemId = document.getElementById('system');
    systemId.textContent = system;
    const btnEnable = document.getElementById('enable');
    btnEnable.addEventListener('click', termgr.partial(termgr.api.application, system, true), false);
    const btnDisable = document.getElementById('disable');
    btnDisable.addEventListener('click', termgr.partial(termgr.api.application, system, false), false);
};


document.addEventListener('DOMContentLoaded', termgr.application.init);
