/*
    manage.mjs - Terminal Manager systems management.

    (C) 2019-2021 HOMEINFO - Digitale Informationssysteme GmbH

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
import { BASE_URL, application, beep, fit, reboot, sync, getSystem } from './api.mjs';


const ONE_HOUR = 3600000;   // in ms


/*
    Navigates to the deployment page.
*/
function loadDeployment () {
    window.location = 'deploy.html';
}


/*
    Reloads the page.
*/
function reload () {
    window.location = 'manage.html';
}


/*
    Checks the last sync.
*/
function checkLastSync (lastSync) {
    return (new Date() - Date.parse(lastSync)) < ONE_HOUR;
}


/*
    Runs a function with arguments and reloads the page afterwards.
*/
function reloadAfterwards (func, ...args) {
    func(...args).then(reload)
}


/*
    Opens a screenshot in a new tab.
*/
function screenshot (system) {
    window.open(BASE_URL + '/screenshot/' + system, '_blank')
}


/*
    Sets up system-related data.
*/
function setup (system) {
    document.getElementById('system').textContent = system.id;

    const btnEnable = document.getElementById('enable');
    btnEnable.addEventListener('click', suppressEvent(reloadAfterwards, application, system.id, true), false);

    const btnDisable = document.getElementById('disable');
    btnDisable.addEventListener('click', suppressEvent(reloadAfterwards, application, system.id, false), false);

    const btnReboot = document.getElementById('reboot');
    btnReboot.addEventListener('click', suppressEvent(reloadAfterwards, reboot, system.id), false);

    const btnBeep = document.getElementById('beep');
    btnBeep.addEventListener('click', suppressEvent(reloadAfterwards, beep, system.id), false);

    const btnDeploy = document.getElementById('deploy');
    btnDeploy.classList.remove('w3-green', 'w3-red');
    btnDeploy.classList.add(system.deployment == null ? 'w3-red' : 'w3-green');
    btnDeploy.addEventListener('click', suppressEvent(loadDeployment), false);

    const btnFit = document.getElementById('fit');
    btnFit.classList.remove('w3-green', 'w3-red');
    btnFit.classList.add(system.fitted ? 'w3-green' : 'w3-red');
    btnFit.addEventListener('click', suppressEvent(reloadAfterwards, fit, system.id, !system.fitted), false);

    const btnSync = document.getElementById('sync');
    btnSync.classList.remove('w3-green', 'w3-red');
    btnSync.classList.add(checkLastSync(system.lastSync) ? 'w3-green' : 'w3-red');
    btnSync.addEventListener('click', suppressEvent(reloadAfterwards, sync, system.id), false);

    const btnScreenshot = document.getElementById('screenshot');
    btnScreenshot.addEventListener('click', suppressEvent(screenshot, system.id), false);
};


/*
    Initializes the management page.
*/
export function init () {
    getSystem().then(setup);
}
