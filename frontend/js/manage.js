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


var termgr = termgr || {};
termgr.manage = {};


/*
    Navigates to the deployment page.
*/
termgr.manage.loadDeployment = function () {
    window.location = 'deploy.html';
};


/*
    Checks the last sync.
*/
termgr.manage.checkLastSync = function (lastSync) {
    lastSync = Date.parse(lastSync);
    const now = new Date();
    const diff = now - lastSync;    // Milliseconds.
    return diff < 3600000;
};


/*
    Initializes the management page.
*/
termgr.manage.init = function () {
    const system = termgr.storage.system.current();
    console.log('DEBUG: ' + JSON.stringify(system));

    const systemId = document.getElementById('system');
    systemId.textContent = system.id;

    const btnEnable = document.getElementById('enable');
    btnEnable.addEventListener('click', termgr.partial(termgr.api.application, system.id, true), false);

    const btnDisable = document.getElementById('disable');
    btnDisable.addEventListener('click', termgr.partial(termgr.api.application, system.id, false), false);

    const btnReboot = document.getElementById('reboot');
    btnReboot.addEventListener('click', termgr.partial(termgr.api.reboot, system.id), false);

    const btnBeep = document.getElementById('beep');
    btnBeep.addEventListener('click', termgr.partial(termgr.api.beep, system.id), false);

    const btnDeploy = document.getElementById('deploy');
    btnDeploy.classList.add(system.deployment == null ? 'w3-red' : 'w3-green');
    btnDeploy.addEventListener('click', termgr.partial(termgr.manage.loadDeployment), false);

    const btnFit = document.getElementById('fit');
    btnFit.classList.add(system.fitted ? 'w3-green' : 'w3-red');
    btnFit.addEventListener('click', termgr.partial(termgr.api.fit, system.id), false);

    const btnSync = document.getElementById('sync');
    btnSync.classList.add(termgr.manage.checkLastSync(system.lastSync) ? 'w3-green' : 'w3-red');
    btnSync.addEventListener('click', termgr.partial(termgr.api.sync, system.id), false);
};


document.addEventListener('DOMContentLoaded', termgr.manage.init);
