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


termgr.INVALID_CREDENTIALS = function () {
    alert('Ungültiger Benutzername und / oder Passwort.');
};


termgr.UNAUTHORIZED = function (what) {
    return function () {
        alert('Sie sind nicht berechtigt, ' + what + '.');
    };
};


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
    Retrieves the customers and their respective terminals
    from the API and invokes the callback function.
*/
termgr.getSystems = function () {
    return termgr.makeRequest('GET', termgr.BASE_URL + '/list').then(
        function (response) {
            termgr.SYSTEMS = response.json;
        }, function () {
            alert('Bitte kontrollieren Sie Ihren Benutzernamen und Ihr Passwort oder versuchen Sie es später noch ein Mal.');
        }
    );
};


/*
    Filters the provided terminals by the respective keywords.
*/
termgr.filterSystems = function* (systems, keywords) {
    for (const system of systems) {
        let deployment = system.deployment;

        for (const keyword of keywords) {
            if (termgr.containsIgnoreCase('' + system.id, keyword)) {
                yield system;
                break;
            }

            if (deployment != null) {
                if (termgr.containsIgnoreCase('' + deployment.id, keyword)) {
                    yield system;
                    break;
                }

                let address = termgr.addressToString(deployment.address);

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
    Filters customers and terminals and lists them.
*/
termgr.listFilteredSystems = function (event) {
    if (event != null) {
        event.preventDefault();
    }

    const searchValue = document.getElementById('searchField').value;
    let keywords = null;

    if (searchValue.length > 0) {
        keywords = searchValue.split();
    }

    if (keywords != null) {
        const systems = Array.from(termgr.filterSystems(termgr.SYSTEMS, keywords));
        termgr.listSystems(systems);
    } else {
        termgr.listSystems(termgr.SYSTEMS);
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
    Lets the respective terminal beep.
*/
termgr.beep = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/beep', data, headers).then(
        function () {
            alert('Das Terminal sollte gepiept haben.');
        },
        function () {
            alert('Das Terminal konnte nicht zum Piepen gebracht werden.');
        }
    );
};


/*
    Actually performs a reboot of the respective terminal.
*/
termgr.reboot = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/reboot', data, headers).then(
        function () {
            alert('Das Terminal wurde wahrscheinlich neu gestartet.');
        },
        function (response) {
            let message = 'Das Terminal konnte nicht neu gestartet werden.';

            if (response.status == 503) {
                message = 'Auf dem Terminal werden aktuell administrative Aufgaben ausgeführt.';
            }

            alert(message);
        }
    );
};


/*
    Enables the application.
*/
termgr.toggleApplication = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/application', data, headers).then(
        function () {
            alert('Digital Signage Anwendung wurde aktiviert.');
        },
        function () {
            alert('Digital Signage Anwendung konnte nicht aktiviert werden.');
        }
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
        function () {
            alert('Digital Signage Anwendung konnte nicht deaktiviert werden.');
        }
    );
};


/*
    Opens the deploying view.
*/
termgr.deploySystem = function (event) {
    const id = event.target.getAttribute('data-id');
    window.location = 'deploy.html?id=' + id;
};


/*
    Deploys the respective terminal.
*/
termgr.deploy = function (system, address) {
    const payload = {'system': system, 'address': address};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/deploy', data, headers).then(
        function () {
            alert('Terminal wurde als "verbaut" markiert.');
        },
        function () {
            alert('Das Terminal konnte nicht als "verbaut" markiert werden.');
        }
    );
};


/*
    Synchronizes the respective terminal.
*/
termgr.sync = function (system) {
    const payload = {'system': system};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/sync', data, headers).then(
        function () {
            alert('Terminal wurde synchronisiert.');
        },
        function () {
            alert('Das Terminal konnte nicht synchronisiert werden.');
        }
    );
};
