/*
    dom.js - Terminal Manager DOM library.

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
termgr.dom = {};


/*
    Generates a terminal DOM entry.
*/
termgr.dom.systemEntry = function (system) {
    const deployment = system.deployment;
    let address = 'Keine Adresse';
    let customer = 'Kein Kunde';

    if (deployment != null) {
        address = termgr.addressToString(deployment.address);
        customer = termgr.customerToString(deployment.customer);
    }

    const rowAddress = document.createElement('div');
    rowAddress.setAttribute('class', 'w3-row');
    rowAddress.innerHTML = address;

    const rowCustomer = document.createElement('div');
    rowCustomer.setAttribute('class', 'w3-row');
    rowCustomer.innerHTML = customer;

    const btnBeepIcon = document.createElement('i');
    btnBeepIcon.setAttribute('class', 'fa fa-volume-up termgr-terminal-icon');

    const btnBeep = document.createElement('button');
    btnBeep.setAttribute('class', 'w3-button w3-blue w3-col s2');
    btnBeep.addEventListener('click', termgr.partial(termgr.api.beep, system.id), false);
    btnBeep.setAttribute('title', 'Beep');
    btnBeep.appendChild(btnBeepIcon);

    const btnRebootIcon = document.createElement('i');
    btnRebootIcon.setAttribute('class', 'fa fa-power-off');

    const btnReboot = document.createElement('button');
    btnReboot.setAttribute('class', 'w3-button w3-orange w3-col s2');
    btnReboot.addEventListener('click', termgr.partial(termgr.api.reboot, system.id), false);
    btnReboot.setAttribute('title', 'Reboot');
    btnReboot.appendChild(btnRebootIcon);

    const btnDeployIcon = document.createElement('i');
    btnDeployIcon.setAttribute('class', 'fa fa-wrench');

    const btnDeploy = document.createElement('button');
    btnDeploy.setAttribute('class', 'w3-button w3-teal w3-col s2');
    btnDeploy.setAttribute('data-id', system.id);
    btnDeploy.addEventListener('click', termgr.partial(termgr.manage.deploy, system.id), false);
    btnDeploy.setAttribute('title', 'Verbauen');
    btnDeploy.appendChild(btnDeployIcon);

    const btnEnableApplicationIcon = document.createElement('i');
    btnEnableApplicationIcon.setAttribute('class', 'fa fa-desktop');

    const btnEnableApplication = document.createElement('button');
    btnEnableApplication.setAttribute('class', 'w3-button w3-khaki w3-col s2');
    btnEnableApplication.setAttribute('data-id', system.id);
    btnEnableApplication.addEventListener('click', termgr.partial(termgr.manage.application, system.id), false);
    btnEnableApplication.setAttribute('title', 'Digital Signage Modus umschalten');
    btnEnableApplication.appendChild(btnEnableApplicationIcon);

    const btnSyncIcon = document.createElement('i');
    btnSyncIcon.setAttribute('class', 'fa fa-sync');

    const btnSync = document.createElement('button');
    btnSync.setAttribute('class', 'w3-button w3-grey w3-col s2');
    btnSync.addEventListener('click', termgr.partial(termgr.api.sync, system.id), false);
    btnSync.setAttribute('data-toggle', 'tooltip');
    btnSync.setAttribute('data-placement', 'bottom');
    btnSync.setAttribute('title', 'Synchronisieren');
    btnSync.appendChild(btnSyncIcon);

    const idField = document.createElement('span');
    idField.setAttribute('class', 'w3-col s2');
    idField.innerHTML = '#' + system.id;

    const rowButtons = document.createElement('div');
    rowButtons.setAttribute('class', 'w3-row');
    rowButtons.appendChild(idField);
    rowButtons.appendChild(btnBeep);
    rowButtons.appendChild(btnReboot);
    rowButtons.appendChild(btnEnableApplication);
    rowButtons.appendChild(btnDeploy);
    rowButtons.appendChild(btnSync);

    const columnDescriptionAndButtons = document.createElement('td');
    columnDescriptionAndButtons.appendChild(rowAddress);
    columnDescriptionAndButtons.appendChild(rowCustomer);
    columnDescriptionAndButtons.appendChild(rowButtons);

    const color = (system.id % 2) ? 'w3-light-grey' : 'w3-white';
    const entry = document.createElement('tr');
    entry.setAttribute('class', 'w3-hover-green ' + color);
    entry.appendChild(columnDescriptionAndButtons);

    return entry;
};


/*
    Converts a deployment into a table.
*/
termgr.dom.deploymentToTable = function (deployment) {
    const table = document.createElement('table');
    table.setAttribute('class', 'w3-table-all');
    // ID.
    const rowId = document.createElement('tr');
    const headerId = document.createElement('th');
    headerId.textContent = 'ID';
    rowId.appendChild(headerId);
    const valueId = document.createElement('td');
    valueId.textContent = '' + deployment.id;
    rowId.appendChild(valueId);
    table.appendChild(rowId);
    // Customer.
    const rowCustomer = document.createElement('tr');
    const headerCustomer = document.createElement('th');
    headerCustomer.textContent = 'Kunde';
    rowCustomer.appendChild(headerCustomer);
    const valueCustomer = document.createElement('td');
    valueCustomer.textContent = termgr.customerToString(deployment.customer);
    rowCustomer.appendChild(valueCustomer);
    table.appendChild(rowCustomer);
    // Type.
    const rowType = document.createElement('tr');
    const headerType = document.createElement('th');
    headerType.textContent = 'Typ';
    rowType.appendChild(headerType);
    const valueType = document.createElement('td');
    valueType.textContent = deployment.type;
    rowType.appendChild(valueType);
    table.appendChild(rowType);
    // Connection.
    const rowConnection = document.createElement('tr');
    const headerConnection = document.createElement('th');
    headerConnection.textContent = 'Internetanbindung';
    rowConnection.appendChild(headerConnection);
    const valueConnection = document.createElement('td');
    valueConnection.textContent = deployment.connection;
    rowConnection.appendChild(valueConnection);
    table.appendChild(rowConnection);
    // Address.
    const rowAddress = document.createElement('tr');
    const headerAddress = document.createElement('th');
    headerAddress.textContent = 'Adresse';
    rowAddress.appendChild(headerAddress);
    const valueAddress = document.createElement('td');
    valueAddress.textContent = termgr.addressToString(deployment.address);
    rowAddress.appendChild(valueAddress);
    table.appendChild(rowAddress);
    // Local Public Transport Address.
    const rowLPTAddress = document.createElement('tr');
    const headerLPTAddress = document.createElement('th');
    headerLPTAddress.textContent = 'ÖPNV Adresse';
    rowLPTAddress.appendChild(headerLPTAddress);
    const valueLPTAddress = document.createElement('td');
    valueLPTAddress.textContent = (deployment.lpt_address == null) ? 'N/A' : termgr.addressToString(deployment.lpt_address);
    rowLPTAddress.appendChild(valueLPTAddress);
    table.appendChild(rowLPTAddress);
    // Weather.
    const rowWeather = document.createElement('tr');
    const headerWeather = document.createElement('th');
    headerWeather.textContent = 'Wetter';
    rowWeather.appendChild(headerWeather);
    const valueWeather = document.createElement('td');
    valueWeather.textContent = deployment.weather || 'N/A';
    rowWeather.appendChild(valueWeather);
    table.appendChild(rowWeather);
    // Scheduled.
    const rowScheduled = document.createElement('tr');
    const headerScheduled = document.createElement('th');
    headerScheduled.textContent = 'Stichtag';
    rowScheduled.appendChild(headerScheduled);
    const valueScheduled = document.createElement('td');
    valueScheduled.textContent = deployment.scheduled || 'N/A';
    rowScheduled.appendChild(valueScheduled);
    table.appendChild(rowScheduled);
    // Annotation.
    const rowAnnotation = document.createElement('tr');
    const headerAnnotation = document.createElement('th');
    headerAnnotation.textContent = 'Anmerkung';
    rowAnnotation.appendChild(headerAnnotation);
    const valueAnnotation = document.createElement('td');
    valueAnnotation.textContent = deployment.annotation || 'N/A';
    rowAnnotation.appendChild(valueAnnotation);
    table.appendChild(rowAnnotation);
    // Testing.
    const rowTesting = document.createElement('tr');
    const headerTesting = document.createElement('th');
    headerTesting.textContent = 'Testgerät';
    rowTesting.appendChild(headerTesting);
    const valueTesting = document.createElement('td');
    valueTesting.textContent = deployment.testing ? 'Ja' : 'Nein';
    rowTesting.appendChild(valueTesting);
    table.appendChild(rowTesting);
    // Timestamp.
    const rowTimestamp = document.createElement('tr');
    const headerTimestamp = document.createElement('th');
    headerTimestamp.textContent = 'Zeitstempel';
    rowTimestamp.appendChild(headerTimestamp);
    const valueTimestamp = document.createElement('td');
    valueTimestamp.textContent = deployment.timestamp || 'N/A';
    rowTimestamp.appendChild(valueTimestamp);
    table.appendChild(rowTimestamp);
    // Systems.
    const rowSystems = document.createElement('tr');
    const headerSystems = document.createElement('th');
    headerSystems.textContent = 'Systeme';
    rowSystems.appendChild(headerSystems);
    const valueSystems = document.createElement('td');
    valueSystems.textContent = deployment.systems.join(', ') || 'N/A';
    rowSystems.appendChild(valueSystems);
    table.appendChild(rowSystems);
    return table;
};
