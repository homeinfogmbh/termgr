/*
    idmap.mjs - Terminal Manager ID mapping.

    (C) 2021 HOMEINFO - Digitale Informationssysteme GmbH

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

import { suppressEvent } from 'https://javascript.homeinfo.de/lib.mjs';
import * as api from './api.mjs';


/*
    Navigates to the listing page.
*/
function list () {
    window.location = 'list.html';
}


/*
    Map old TID+CID to new system ID.
*/
function map () {
    const tid = document.getElementById('tid').value;
    const cid = document.getElementById('cid').value;
    const systemId = document.getElementById('systemId');
    systemId.value = '';
    api.idmap(tid, cid).then(function (json) {
        systemId.value = json.system;
    });
}


/*
    Initialize index.html.
*/
export function init () {
    const btnList = document.getElementById('btnList');
    btnList.addEventListener('click', suppressEvent(list), false);
    const btnMap = document.getElementById('btnMap');
    btnMap.addEventListener('click', suppressEvent(map), false);
}
