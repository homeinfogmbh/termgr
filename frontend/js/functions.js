/*
    functions.js - Terminal Manager functions library.

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


/*
    Starts loading.
*/
termgr.startLoading = function () {
    const loader = document.getElementById('loader');
    const target = document.getElementById('target');
    target.style.display = 'none';
    loader.style.display = 'block';
};


/*
    Stops loading.
*/
termgr.stopLoading = function () {
    const loader = document.getElementById('loader');
    const target = document.getElementById('target');
    loader.style.display = 'none';
    target.style.display = 'block';
};


/*
    Returns the respective address as a one-line string.
*/
termgr.addressToString = function (address) {
    return address.street + ' ' + address.houseNumber + ', ' + address.zipCode + ' ' + address.city;
};


/*
    Returns the respective customer as a one-line string.
*/
termgr.customerToString = function (customer) {
    return customer.company.name  + ' (' + customer.id + ')';
};


/*
    Returns the respective deployment as a one-line string.
*/
termgr.deploymentToString = function (deployment) {
    return deployment.id + ': ' + termgr.addressToString(deployment.address);
};


/*
    Renders the respective systems.
*/
termgr.renderSystems = function (systems) {
    const container = document.getElementById('systems');
    container.innerHTML = '';

    for (const system of systems) {
        let entry = termgr.systemEntry(system);
        container.appendChild(entry);
    }
};


/*
    Renders the respective deployments.
*/
termgr.renderDeployments = function (deployments) {
    const select = document.getElementById('deployments');
    select.innerHTML = '';

    for (const deployment of deployments) {
        let option = document.createElement('option');
        option.value = '' + deployment.id;
        option.textContent = termgr.deploymentToString(deployment);
        select.appendChild(option);
    }
};


/*
    Renders the respective customers.
*/
termgr.renderCustomers = function (customers) {
    const select = document.getElementById('customer');
    select.innerHTML = '';

    for (const customer of customers) {
        let option = document.createElement('option');
        option.setAttribute('value', customer.id);
        option.textContent = customer.company.name;
        select.appendChild(option);
    }
};


/*
    Renders the respective connections.
*/
termgr.renderConnections = function (connections) {
    const select = document.getElementById('connection');
    select.innerHTML = '';

    for (const connection of connections) {
        let option = document.createElement('option');
        option.setAttribute('value', connection);
        option.textContent = connection;
        select.appendChild(option);
    }
};


/*
    Renders the respective types.
*/
termgr.renderTypes = function (types) {
    const select = document.getElementById('type');
    select.innerHTML = '';

    for (const type of types) {
        let option = document.createElement('option');
        option.setAttribute('value', type);
        option.textContent = type;
        select.appendChild(option);
    }
};


/*
    Function to wrap a function and disable default events.
*/
termgr.partial = function (func, ...args) {
    return function (event) {
        if (event != null) {
            event.preventDefault();
        }

        return func(...args);
    };
};
