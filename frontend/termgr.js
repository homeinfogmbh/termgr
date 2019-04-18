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

    Requires:
      * jquery.js
      * sweetalert.js
*/
'use strict';

const termgr = {};

termgr.BASE_URL = 'https://termgr.homeinfo.de';

termgr.INVALID_CREDENTIALS = function () {
    alert('Ungültiger Benutzername und / oder Passwort.');
};

termgr.UNAUTHORIZED = function (what) {
    return function () {
        alert('Sie sind nicht berechtigt, ' + what + '.');
    };
};

termgr.SYSTEMS = [];


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
  Makes a request returning a promise.
*/
termgr.makeRequest = function (method, url, data = null, headers = {}) {
    function parseResponse (response) {
        try {
            return JSON.parse(response);
        } catch (error) {
            return response;
        }
    }

    function executor (resolve, reject) {
        function onload () {
            if (this.status >= 200 && this.status < 300) {
                resolve({
                    response: xhr.response,
                    json: parseResponse(xhr.response),
                    status: this.status,
                    statusText: xhr.statusText
                });
            } else {
                reject({
                    response: xhr.response,
                    json: parseResponse(xhr.response),
                    status: this.status,
                    statusText: xhr.statusText
                });
            }
        }

        function onerror () {
            reject({
                response: xhr.response,
                json: parseResponse(xhr.response),
                status: this.status,
                statusText: xhr.statusText
            });
        }

        const xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.open(method, url);

        for (const header in headers) {
            xhr.setRequestHeader(header, headers[header]);
        }

        xhr.onload = onload;
        xhr.onerror = onerror;

        if (data == null) {
            xhr.send();
        } else {
            xhr.send(data);
        }
    }

    return new Promise(executor);
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
termgr.listFilteredSystems = function () {
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
    Actually enables the application.
*/
termgr.enableApplication = function (system) {
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
    Actually disables the application.
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


/*
    Generator function to wrap a function and disable default events.
*/
termgr.partial = function (func, ...args) {
    return function (event) {
        event.preventDefault();
        func(...args);
    };
};


/*
    Generates a terminal DOM entry.
*/
termgr.systemEntry = function (system) {
    const deployment = system.deployment;
    const icon = document.createElement('i');
    icon.setAttribute('class', 'fa fa-tv');

    const columnIcon = document.createElement('td');
    columnIcon.setAttribute('class', 'col-xs-1');
    columnIcon.appendChild(icon);

    let descriptionText = ''+ system.id;

    if (deployment != null) {
        const address = termgr.addressToString(deployment.address);
        descriptionText += '(' + address + ')';
    }

    const description = document.createElement('p');
    description.setAttribute('class', 'termgr-terminal-description');
    description.textContent = descriptionText;

    const columnDescription = document.createElement('td');
    columnDescription.setAttribute('class', 'col-xs-6 termgr-terminal-description');
    columnDescription.appendChild(description);

    const btnBeepIcon = document.createElement('i');
    btnBeepIcon.setAttribute('class', 'fa fa-volume-up termgr-terminal-icon');

    const btnBeep = document.createElement('button');
    btnBeep.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnBeep.setAttribute('type', 'button');
    btnBeep.addEventListener('click', termgr.partial(termgr.beep, system.id), false);
    btnBeep.setAttribute('data-toggle', 'tooltip');
    btnBeep.setAttribute('data-placement', 'bottom');
    btnBeep.setAttribute('title', 'Beep');
    btnBeep.appendChild(btnBeepIcon);

    const btnRebootIcon = document.createElement('i');
    btnRebootIcon.setAttribute('class', 'fa fa-power-off');

    const btnReboot = document.createElement('button');
    btnReboot.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnReboot.setAttribute('type', 'button');
    btnReboot.addEventListener('click', termgr.partial(termgr.queryReboot, system.id), false);
    btnReboot.setAttribute('data-toggle', 'tooltip');
    btnReboot.setAttribute('data-placement', 'bottom');
    btnReboot.setAttribute('title', 'Reboot');
    btnReboot.appendChild(btnRebootIcon);

    const btnDeployIcon = document.createElement('i');
    btnDeployIcon.setAttribute('class', 'fa fa-wrench');

    const btnDeploy = document.createElement('button');
    btnDeploy.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnDeploy.setAttribute('type', 'button');
    btnDeploy.setAttribute('data-toggle', 'modal');
    btnDeploy.setAttribute('data-target', '#deploymentDialog');
    btnDeploy.addEventListener('click', termgr.partial(termgr.toggleDeploy, system.id), false);
    btnDeploy.appendChild(btnDeployIcon);

    const btnApplicationIcon = document.createElement('i');
    btnApplicationIcon.setAttribute('class', 'fa fa-desktop');

    const btnApplication = document.createElement('button');
    btnApplication.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnApplication.setAttribute('type', 'button');
    btnApplication.setAttribute('data-toggle', 'modal');
    btnApplication.setAttribute('data-target', '#applicationDialog');
    btnApplication.addEventListener('click', termgr.partial(termgr.toggleApplication, system.id), false);
    btnApplication.appendChild(btnApplicationIcon);

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
    columnButtons.setAttribute('class', 'col-xs-11');
    columnButtons.appendChild(btnBeep);
    columnButtons.appendChild(btnReboot);
    columnButtons.appendChild(btnApplication);
    columnButtons.appendChild(btnDeploy);
    columnButtons.appendChild(btnSync);

    const rowButtons = document.createElement('tr');
    rowButtons.appendChild(columnButtons);

    const rowDescription = document.createElement('tr');
    rowDescription.appendChild(columnDescription);

    const tableDescriptionAndButtons = document.createElement('table');
    tableDescriptionAndButtons.appendChild(rowDescription);
    tableDescriptionAndButtons.appendChild(rowButtons);

    const columnDescriptionAndButtons = document.createElement('td');
    columnDescriptionAndButtons.appendChild(tableDescriptionAndButtons);

    const entry = document.createElement('tr');
    entry.setAttribute('class', 'row row-centered termgr-terminal-entry');
    entry.appendChild(columnIcon);
    entry.appendChild(columnDescriptionAndButtons);

    return entry;
};


/*
    Performs the initial login.
*/
termgr.login = function (event) {
    event.preventDefault();
    const account = document.getElementById('userName').value;
    const passwd = document.getElementById('passwd').value;
    const payload = {'account': account, 'passwd': passwd};
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', 'https://his.homeinfo.de/session', data, headers).then(
        function () {
            window.location = 'manage.html';
        },
        function () {
            alert('Ungültiger Benutzername und / oder Passwort.');
        }
    );
};


/*
    Initialize index.html.
*/
termgr.initIndex = function () {
    const login = document.getElementById('login');
    login.addEventListener('click', termgr.login, false);
};


/*
    Initialize manage.html.
*/
termgr.initManage = function () {
    termgr.getSystems().then(termgr.listFilteredSystems);
    const filter = document.getElementById('filter');
    filter.addEventListener('click', termgr.listFilteredSystems, false);
};
