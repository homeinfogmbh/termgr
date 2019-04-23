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


let termgr = termgr || {};


/*
    Generates a terminal DOM entry.
*/
termgr.systemEntry = function (system) {
    const deployment = system.deployment;
    const icon = document.createElement('i');
    icon.setAttribute('class', 'fa fa-tv');

    const columnIcon = document.createElement('td');
    columnIcon.appendChild(icon);

    let descriptionText = ''+ system.id;

    if (deployment != null) {
        const address = termgr.addressToString(deployment.address);
        descriptionText += ' (' + address + ')';
    }

    const description = document.createElement('p');
    description.setAttribute('class', 'termgr-terminal-description');
    description.textContent = descriptionText;

    const columnDescription = document.createElement('td');
    columnDescription.appendChild(description);

    const btnBeepIcon = document.createElement('i');
    btnBeepIcon.setAttribute('class', 'fa fa-volume-up termgr-terminal-icon');

    const btnBeep = document.createElement('button');
    btnBeep.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnBeep.setAttribute('type', 'button');
    btnBeep.addEventListener('click', termgr.partial(termgr.beep, system.id), false);
    btnBeep.setAttribute('title', 'Beep');
    btnBeep.appendChild(btnBeepIcon);

    const btnRebootIcon = document.createElement('i');
    btnRebootIcon.setAttribute('class', 'fa fa-power-off');

    const btnReboot = document.createElement('button');
    btnReboot.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnReboot.setAttribute('type', 'button');
    btnReboot.addEventListener('click', termgr.partial(termgr.queryReboot, system.id), false);
    btnReboot.setAttribute('title', 'Reboot');
    btnReboot.appendChild(btnRebootIcon);

    const btnDeployIcon = document.createElement('i');
    btnDeployIcon.setAttribute('class', 'fa fa-wrench');

    const btnDeploy = document.createElement('button');
    btnDeploy.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnDeploy.setAttribute('type', 'button');
    btnDeploy.setAttribute('data-id', system.id);
    btnDeploy.addEventListener('click', termgr.deploySystem);
    btnDeploy.appendChild(btnDeployIcon);

    const btnEnableApplicationIcon = document.createElement('i');
    btnEnableApplicationIcon.setAttribute('class', 'fa fa-desktop');

    const btnEnableApplication = document.createElement('button');
    btnEnableApplication.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnEnableApplication.setAttribute('type', 'button');
    btnEnableApplication.setAttribute('data-id', system.id);
    btnEnableApplication.addEventListener('click', termgr.toggleApplication);
    btnEnableApplication.appendChild(btnEnableApplicationIcon);

    const btnSyncIcon = document.createElement('i');
    btnSyncIcon.setAttribute('class', 'fa fa-sync');

    const btnSync = document.createElement('button');
    btnSync.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnSync.setAttribute('type', 'button');
    btnSync.addEventListener('click', termgr.partial(termgr.sync, system.id), false);
    btnSync.setAttribute('data-toggle', 'tooltip');
    btnSync.setAttribute('data-placement', 'bottom');
    btnSync.setAttribute('title', 'Synchronize');
    btnSync.appendChild(btnSyncIcon);

    const columnButtons = document.createElement('td');
    columnButtons.appendChild(btnBeep);
    columnButtons.appendChild(btnReboot);
    columnButtons.appendChild(btnEnableApplication);
    columnButtons.appendChild(btnDeploy);
    columnButtons.appendChild(btnSync);

    const rowButtons = document.createElement('tr');
    rowButtons.appendChild(columnButtons);

    const rowDescription = document.createElement('tr');
    rowDescription.appendChild(columnDescription);

    const tableDescriptionAndButtons = document.createElement('div');
    tableDescriptionAndButtons.appendChild(rowDescription);
    tableDescriptionAndButtons.appendChild(rowButtons);

    const columnDescriptionAndButtons = document.createElement('td');
    columnDescriptionAndButtons.appendChild(tableDescriptionAndButtons);

    const entry = document.createElement('table');
    entry.setAttribute('class', 'w3-striped');
    entry.appendChild(columnIcon);
    entry.appendChild(columnDescriptionAndButtons);

    return entry;
};
