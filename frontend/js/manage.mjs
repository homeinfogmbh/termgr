/*
    manage.js - Terminal Manager systems management.

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

import { suppressEvent } from 'https://javascript.homeinfo.de/lib.mjs';
import { application, beep, fit, reboot, sync, getSystem } from './api.mjs';


/*
    Navigates to the deployment page.
*/
function loadDeployment () {
    window.location = 'deploy.html';
}


/*
    Checks the last sync.
*/
function checkLastSync (lastSync) {
    lastSync = Date.parse(lastSync);
    const now = new Date();
    const diff = now - lastSync;    // Milliseconds.
    return diff < 3600000;
}


/*
    Sets up system-related data.
*/
function setup (system) {
    const systemId = document.getElementById('system');
    systemId.textContent = system.id;

    const btnEnable = document.getElementById('enable');
    btnEnable.addEventListener('click', suppressEvent(application, system.id, true), false);

    const btnDisable = document.getElementById('disable');
    btnDisable.addEventListener('click', suppressEvent(application, system.id, false), false);

    const btnReboot = document.getElementById('reboot');
    btnReboot.addEventListener('click', suppressEvent(reboot, system.id), false);

    const btnBeep = document.getElementById('beep');
    btnBeep.addEventListener('click', suppressEvent(beep, system.id), false);

    const btnDeploy = document.getElementById('deploy');
    btnDeploy.classList.add(system.deployment == null ? 'w3-red' : 'w3-green');
    btnDeploy.addEventListener('click', suppressEvent(loadDeployment), false);

    const btnFit = document.getElementById('fit');
    btnFit.classList.add(system.fitted ? 'w3-green' : 'w3-red');
    btnFit.addEventListener('click', suppressEvent(fit, system.id), false);

    const btnSync = document.getElementById('sync');
    btnSync.classList.add(checkLastSync(system.lastSync) ? 'w3-green' : 'w3-red');
    btnSync.addEventListener('click', suppressEvent(sync, system.id), false);
};


/*
    Initializes the management page.
*/
export function init () {
    getSystem().then(setup);
}
