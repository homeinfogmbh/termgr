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
    Generates a terminal DOM entry.
*/
termgr.systemEntry = function (system) {
    const deployment = system.deployment;
    let address = 'Keine Adresse';

    if (deployment != null) {
        address = termgr.addressToString(deployment.address);
    }

    const description = document.createElement('p');
    description.setAttribute('class', 'termgr-terminal-description');
    description.textContent = address;

    const columnDescription = document.createElement('div');
    columnDescription.setAttribute('class', 'w3-col s12');
    columnDescription.appendChild(description);

    const rowDescription = document.createElement('div');
    rowDescription.setAttribute('class', 'w3-row');
    rowDescription.appendChild(columnDescription);

    const btnBeepIcon = document.createElement('i');
    btnBeepIcon.setAttribute('class', 'fa fa-volume-up termgr-terminal-icon');

    const btnBeep = document.createElement('button');
    btnBeep.setAttribute('class', 'w3-button w3-blue w3-col s2');
    btnBeep.addEventListener('click', termgr.partial(termgr.beep, system.id), false);
    btnBeep.setAttribute('title', 'Beep');
    btnBeep.appendChild(btnBeepIcon);

    const btnRebootIcon = document.createElement('i');
    btnRebootIcon.setAttribute('class', 'fa fa-power-off');

    const btnReboot = document.createElement('button');
    btnReboot.setAttribute('class', 'w3-button w3-orange w3-col s2');
    btnReboot.addEventListener('click', termgr.partial(termgr.reboot, system.id), false);
    btnReboot.setAttribute('title', 'Reboot');
    btnReboot.appendChild(btnRebootIcon);

    const btnDeployIcon = document.createElement('i');
    btnDeployIcon.setAttribute('class', 'fa fa-wrench');

    const btnDeploy = document.createElement('button');
    btnDeploy.setAttribute('class', 'w3-button w3-teal w3-col s2');
    btnDeploy.setAttribute('data-id', system.id);
    btnDeploy.addEventListener('click', termgr.deploySystem);
    btnReboot.setAttribute('title', 'Verbauen');
    btnDeploy.appendChild(btnDeployIcon);

    const btnEnableApplicationIcon = document.createElement('i');
    btnEnableApplicationIcon.setAttribute('class', 'fa fa-desktop');

    const btnEnableApplication = document.createElement('button');
    btnEnableApplication.setAttribute('class', 'w3-button w3-khaki w3-col s2');
    btnEnableApplication.setAttribute('data-id', system.id);
    btnEnableApplication.addEventListener('click', termgr.toggleApplication);
    btnReboot.setAttribute('title', 'Digital Signage Modus umschalten');
    btnEnableApplication.appendChild(btnEnableApplicationIcon);

    const btnSyncIcon = document.createElement('i');
    btnSyncIcon.setAttribute('class', 'fa fa-sync');

    const btnSync = document.createElement('button');
    btnSync.setAttribute('class', 'w3-button w3-grey w3-col s2');
    btnSync.addEventListener('click', termgr.partial(termgr.sync, system.id), false);
    btnSync.setAttribute('data-toggle', 'tooltip');
    btnSync.setAttribute('data-placement', 'bottom');
    btnSync.setAttribute('title', 'Synchronisieren');
    btnSync.appendChild(btnSyncIcon);

    const idField = document.createElement('span');
    idField.setAttribute('class', 'w3-col s2');
    idField.textContent = '#' + system.id;

    const rowButtons = document.createElement('div');
    rowButtons.setAttribute('class', 'w3-row');
    rowButtons.appendChild(idField);
    rowButtons.appendChild(btnBeep);
    rowButtons.appendChild(btnReboot);
    rowButtons.appendChild(btnEnableApplication);
    rowButtons.appendChild(btnDeploy);
    rowButtons.appendChild(btnSync);

    const columnDescriptionAndButtons = document.createElement('td');
    columnDescriptionAndButtons.appendChild(rowDescription);
    columnDescriptionAndButtons.appendChild(rowButtons);

    const color = (system.id % 2) ? 'w3-light-grey' : 'w3-white';
    const entry = document.createElement('tr');
    entry.setAttribute('class', 'w3-hover-green ' + color);
    entry.appendChild(columnDescriptionAndButtons);

    return entry;
};
