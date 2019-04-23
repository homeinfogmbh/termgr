/*
    termgr.js - Terminal Manager application toggleing.

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
    Initialize manage.html.
*/
function init () {
    const id = parseInt(termgr.getArg('System'));
    const btnEnable = document.getElementById('enable');
    btnEnable.addEventListener('click', termgr.partial(termgr.enableApplication, id), false);
    const btnDisable = document.getElementById('disable');
    btnDisable.addEventListener('click', termgr.partial(termgr.disableApplication, id), false);
    const systemId = document.getElementById('system');
    systemId.textContent = id;
}


document.addEventListener('DOMContentLoaded', init);
