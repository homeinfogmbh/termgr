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
    Case-insensitively checks whether a string contains another string.
*/
termgr.containsIgnoreCase = function (haystack, needle) {
    if (! haystack) {
        return false;
    }

    return haystack.toLowerCase().includes(needle.toLowerCase());
};


/*
    Returns the respective address as a one-line string.
*/
termgr.addressToString = function (address) {
    return address.street + ' ' + address.houseNumber + ', ' + address.zipCode + ' ' + address.city;
};


/*
    Retrieves systems from the API.
*/
termgr.getSystems = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list/systems').then(
        function (response) {
            localStorage.setItem('termgr.systems', JSON.stringify(response.json));
        },
        termgr.checkSession('Die Liste der Systeme konnte nicht abgefragt werden.')
    );
};


/*
    Retrieves customers from the backend,
    which the current user is allowed to deploy to.
*/
termgr.getCustomers = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list/customers').then(
        function (response) {
            localStorage.setItem('termgr.customers', JSON.stringify(response.json));
        },
        termgr.checkSession('Die Liste der Kunden konnte nicht abgefragt werden.')
    );
};

/*
    Filters the provided system by the respective keywords.
*/
termgr.filterSystems = function* (systems, keywords) {
    for (const system of systems) {
        let deployment = system.deployment;

        for (const keyword of keywords) {
            // System ID.
            if (termgr.containsIgnoreCase('' + system.id, keyword)) {
                yield system;
                break;
            }

            if (deployment != null) {
                // Customer ID.
                if (termgr.containsIgnoreCase('' + deployment.customer.id, keyword)) {
                    yield system;
                    break;
                }

                // Customer name.
                if (termgr.containsIgnoreCase(deployment.customer.company.name, keyword)) {
                    yield system;
                    break;
                }

                let address = termgr.addressToString(deployment.address);

                // Address.
                if (termgr.containsIgnoreCase(address, keyword)) {
                    yield system;
                    break;
                }
            }
        }
    }
};


/*
    Lists the respective systems.
*/
termgr.listSystems = function (systems) {
    const container = document.getElementById('systems');
    container.innerHTML = '';

    for (const system of systems) {
        let entry = termgr.systemEntry(system);
        container.appendChild(entry);
    }
};


/*
    Renders the respective customers.
*/
termgr.renderCustomers = function () {
    const select = document.getElementById('customer');
    select.innerHTML = '';
    const customers = JSON.parse(localStorage.getItem('termgr.customers'));

    for (const customer of customers) {
        let option = document.createElement('option');
        option.setAttribute('value', customer.id);
        option.textContent = customer.company.name;
        select.appendChild(option);
    }
};


/*
    Filters systems.
*/
termgr.listFilteredSystems = function () {
    const searchValue = document.getElementById('searchField').value;
    let keywords = null;

    if (searchValue.length > 0) {
        keywords = searchValue.split();
    }

    let systems = JSON.parse(localStorage.getItem('termgr.systems'));

    if (keywords != null) {
        systems = Array.from(termgr.filterSystems(systems, keywords));
        termgr.listSystems(systems);
    } else {
        termgr.listSystems(systems);
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


/*
    Lets the respective system beep.
*/
termgr.beep = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/beep', data, headers).then(
        function () {
            alert('Das System sollte gepiept haben.');
        },
        termgr.checkSession('Das System konnte nicht zum Piepen gebracht werden.')
    );
};


/*
    Actually performs a reboot of the respective system.
*/
termgr.reboot = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/reboot', data, headers).then(
        function () {
            alert('Das System wurde wahrscheinlich neu gestartet.');
        },
        function (response) {
            let message = 'Das System konnte nicht neu gestartet werden.';

            if (response.status == 503) {
                message = 'Auf dem System werden aktuell administrative Aufgaben ausgeführt.';
            }

            return termgr.checkSession(message)(response);
        }
    );
};


/*
    Enables the application.
*/
termgr.enableApplication = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/application', data, headers).then(
        function () {
            alert('Digital Signage Anwendung wurde aktiviert.');
        },
        termgr.checkSession('Digital Signage Anwendung konnte nicht aktiviert werden.')
    );
};


/*
    Disables the application.
*/
termgr.disableApplication = function (system) {
    const payload = {'system': system, 'disable': true};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/application', data, headers).then(
        function () {
            alert('Digital Signage Anwendung wurde deaktiviert.');
        },
        termgr.checkSession('Digital Signage Anwendung konnte nicht deaktiviert werden.')
    );
};


/*
    Synchronizes the respective system.
*/
termgr.sync = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/sync', data, headers).then(
        function () {
            alert('Das System wurde synchronisiert.');
        },
        termgr.checkSession('Das System konnte nicht synchronisiert werden.')
    );
};


/*
    Deploys a system.
*/
termgr.deploy = function (system, customer, street, houseNumber, zipCode, city) {
    const payload = {
        system: system,
        customer: customer,
        address: {
            street: street,
            houseNumber: houseNumber,
            zipCode: zipCode,
            city: city
        }
    };
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/deploy', data, headers).then(
        function () {
            alert('Das System wurde als verbaut gekennzeichnet.');
        },
        termgr.checkSession('Das System konnte nicht als verbaut gekennzeichnet werden.')
    );
};
