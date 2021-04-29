/*
    dom.mjs - Terminal Manager DOM library.

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
import { addressToString, customerToString } from 'https://javascript.homeinfo.de/mdb.mjs';
import { select } from './list.mjs';


/*
    Returns a buffer column.
*/
function getBufferCol () {
    const colBuffer = document.createElement('div');
    colBuffer.classList.add('w3-col');
    colBuffer.classList.add('m1');
    colBuffer.classList.add('s2');
    colBuffer.innerHTML = '&nbsp;';
    return colBuffer;
}


/*
    Generates a terminal DOM entry.
*/
export function systemEntry (system, index) {
    const deployment = system.deployment;
    let address = 'Keine Adresse';
    let customer = 'Kein Kunde';

    if (deployment != null) {
        address = addressToString(deployment.address);
        customer = customerToString(deployment.customer, true);
    }

    const colId = document.createElement('div');
    colId.classList.add('w3-col');
    colId.classList.add('m1');
    colId.classList.add('s2');
    colId.textContent = '#' + system.id;

    const colAddress = document.createElement('div');
    colAddress.classList.add('w3-col');
    colAddress.classList.add('m3');
    colAddress.classList.add('s10');
    colAddress.textContent = address;

    const colCustomer = document.createElement('div');
    colCustomer.classList.add('w3-col');
    colCustomer.classList.add('m4');
    colCustomer.classList.add('s10');
    colCustomer.textContent = customer;

    const colConfigured = document.createElement('div');
    colConfigured.classList.add('w3-col');
    colConfigured.classList.add('m2');
    colConfigured.classList.add('s10');
    colConfigured.textContent = 'Programmiert: ' + (system.configured || 'N/A');

    const color = (index % 2) ? 'w3-light-grey' : 'w3-white';
    const entry = document.createElement('div');
    entry.classList.add('w3-row');
    entry.classList.add('w3-hover-green');
    entry.classList.add(color);
    entry.appendChild(colId);
    entry.appendChild(colAddress);
    entry.appendChild(getBufferCol());
    entry.appendChild(colCustomer);
    entry.appendChild(getBufferCol());
    entry.appendChild(colConfigured);
    entry.addEventListener('click', suppressEvent(select, system.id), false);

    return entry;
}


/*
    Converts a deployment into a table.
*/
export function deploymentToTable (deployment) {
    const table = document.createElement('table');
    table.classList.add('w3-table-all');
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
    valueCustomer.textContent = customerToString(deployment.customer);
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
    valueAddress.textContent = addressToString(deployment.address);
    rowAddress.appendChild(valueAddress);
    table.appendChild(rowAddress);
    // Local Public Transport Address.
    const rowLPTAddress = document.createElement('tr');
    const headerLPTAddress = document.createElement('th');
    headerLPTAddress.textContent = 'ÖPNV Adresse';
    rowLPTAddress.appendChild(headerLPTAddress);
    const valueLPTAddress = document.createElement('td');
    valueLPTAddress.textContent = (deployment.lpt_address == null) ? 'N/A' : addressToString(deployment.lpt_address);
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
    headerTimestamp.textContent = 'Erstellungsdatum';
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
}
