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

var termgr = termgr || {};

termgr.BASE_URL = 'https://termgr.homeinfo.de';

termgr.INVALID_CREDENTIALS = function () {
    swal({
        title: 'Fehler.',
        text: 'Ungültiger Benutzername und / oder Passwort.',
        type: 'error'
    });
};

termgr.UNAUTHORIZED = function (what) {
    return function () {
        swal({
            title: 'Fehler.',
            text: 'Sie sind nicht berechtigt, ' + what + '.',
            type: 'error'
        });
    };
};

termgr.customer = null;


/*
    Case-insensitively checks whether a string contains another string.
*/
termgr.containsIgnoreCase = function (haystack, needle) {
    if (! haystack) {
        return false;
    }

    return haystack.toLowerCase().indexOf(needle.toLowerCase()) >= 0;
};


/*
    Returns the user name and password from the respective input fields.
*/
termgr.getCredentials = function () {
    return {'user_name': jQuery('#userName').val(), 'passwd': jQuery('#passwd').val()};
};


/*
    Returns the basic post data for the respective terminal.
*/
termgr.getData = function (tid, cid) {
    const data = termgr.getCredentials();
    data['tid'] = tid;
    data['cid'] = '' + cid;   // Backend needs a string here.
    return data;
};


/*
    Retrieves the customers and their respective terminals
    from the API and invokes the callback function.
*/
termgr.getCustomers = function () {
    const credentials = termgr.getCredentials();

    return jQuery.ajax({
        url: termgr.BASE_URL + '/check/list',
        type: 'POST',
        data: JSON.stringify(credentials),
        contentType: 'application/json'
    }).then(
        function (customers) {
            termgr.customers = customers;
        }, function () {
            swal({
                title: 'Konnte Terminaldaten nicht abfragen.',
                text: 'Bitte kontrollieren Sie Ihren Benutzernamen und Ihr Passwort oder versuchen Sie es später noch ein Mal.',
                type: 'error'
            });

            jQuery('#loader').hide();
        }
    );
};


/*
    Filters the provided terminals by the respective keywords.
*/
termgr.filterTerminals = function* (terminals, cid, keywords) {
    for (let terminal of terminals) {
        let matching = true;

        for (let keyword of keywords) {
            let matchingTid = termgr.containsIgnoreCase('' + terminal.tid, keyword);
            let matchingCid = termgr.containsIgnoreCase('' + cid, keyword);
            let matchingAddress = termgr.containsIgnoreCase(termgr._addressToString(terminal.address), keyword);

            if (! (matchingTid || matchingCid || matchingAddress)) {
                matching = false;
                break;
            }
        }

        if (matching) {
            yield terminal;
        }
    }
};


/*
    Filters the provided customer by the respective keywords.
*/
termgr.filterCustomer = function (customer, keywords) {
    let customerMatch = true;

    for (let keyword of keywords) {
        if (! termgr.containsIgnoreCase(customer.name, keyword)) {
            customerMatch = false;
            break;
        }
    }

    if (customerMatch) {
        return customer;
    }

    const terminals = Array.from(termgr.filterTerminals(customer.terminals, customer.id, keywords));

    if (terminals.length > 0) {
        return {'id': customer.id, 'name': customer.name, 'terminals': terminals};
    }

    return null;
};


/*
    Filters the provided customers by the respective keywords.
*/
termgr.filterCustomers = function (customers, keywords) {
    const filteredCustomers = {};

    for (let cidStr in customers) {
        if (customers.hasOwnProperty(cidStr)) {
            let customer = termgr.filterCustomer(customers[cidStr], keywords);

            if (customer != null) {
                filteredCustomers[cidStr] = customer;
            }
        }
    }

    return filteredCustomers;
};


/*
    Lists the provided customers.
*/
termgr.listCustomers = function (customers) {
    const customerList = document.getElementById('customerList');
    customerList.innerHTML = '';

    for (let cidStr in customers) {
        if (customers.hasOwnProperty(cidStr)) {
            if (customers[cidStr] != null) {
                customerList.appendChild(termgr.customerEntry(customers[cidStr]));
            }
        }
    }
};


/*
    Filters customers and terminals and lists them.
*/
termgr.listFiltered = function (customers) {
    if (customers == null) {
        customers = termgr.customers;
        jQuery('#customerList').hide();
        jQuery('#loader').show();
    }

    const searchValue = jQuery('#searchField').val();

    if (searchValue.length > 0) {
        const keywords = searchValue.split();

        if (keywords.length > 0) {
            customers = termgr.filterCustomers(customers, keywords);
        }
    }

    termgr.listCustomers(customers);
};


/*
    Lets the respective terminal beep.
*/
termgr.beep = function (tid, cid) {
    const data = termgr.getData(tid, cid);

    jQuery.ajax({
        url: termgr.BASE_URL + '/check/identify',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        error: function () {
            swal({
                title: 'Fehler.',
                text: 'Das Terminal konnte nicht zum Piepen gebracht werden.',
                type: 'error'
            });
        },
        success: function () {
            swal({
                title: 'OK.',
                text: 'Das Terminal sollte gepiept haben.',
                type: 'success'
            });
        },
        statusCode: {
            401: termgr.INVALID_CREDENTIALS
        }
    });
};


/*
    Actually performs a reboot of the respective terminal.
*/
termgr.reboot = function (tid, cid) {
    const data = termgr.getData(tid, cid);

    jQuery.ajax({
        url: termgr.BASE_URL + '/administer/reboot',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        error: function (jqXHR) {
            swal({
                title: 'Das Terminal konnte nicht neu gestartet werden.',
                html: '<pre>' + jqXHR.responseText + '</pre>',
                type: 'error'
            });
        },
        statusCode: {
            200: function () {
                swal({
                    title: 'OK.',
                    text: 'Das Terminal wurde neu gestartet.',
                    type: 'success'
                });
            },
            202: function () {
                swal({
                    title: 'OK.',
                    text: 'Das Terminal wurde wahrscheinlich neu gestartet.',
                    type: 'success'
                });
            },
            401: termgr.INVALID_CREDENTIALS,
            403: termgr.UNAUTHORIZED('dieses Terminal neu zu starten'),
            503: function () {
                swal({
                    title: 'Zur Zeit nicht möglich.',
                    text: 'Auf dem Terminal werden aktuell administrative Aufgaben ausgeführt.',
                    type: 'error'
                });
            }
        }
    });
};


/*
    Reboots a terminal.

    This function will open a popup to
    confirm or abort the actual reboot.
*/
termgr.queryReboot = function (tid, cid) {
    swal({
        title: 'Sind Sie sicher?',
        text: 'Wollen Sie das Terminal ' + tid + '.' + cid + ' wirklich neu starten?',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Ja, neu starten!',
        cancelButtonText: 'Nein, abbrechen!',
        confirmButtonClass: 'btn btn-success',
        cancelButtonClass: 'btn btn-danger',
        closeOnConfirm: false,
        closeOnCancel: true,
        showLoaderOnConfirm: true
    }, function (confirmed) {
        if (confirmed) {
            termgr.reboot(tid, cid);
        }
    });
};


/*
    Actually enables the application.
*/
termgr.enableApplication = function (tid, cid) {
    const data = termgr.getData(tid, cid);

    jQuery.ajax({
        url: termgr.BASE_URL + '/administer/application',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function () {
            swal({
                title: 'OK.',
                text: 'Digital Signage Anwendung wurde aktiviert.',
                type: 'success'
            });
        },
        error: function () {
            swal({
                title: 'Fehler.',
                text: 'Digital Signage Anwendung konnte nicht aktiviert werden.',
                type: 'error'
            });
        },
        statusCode: {
            401: termgr.INVALID_CREDENTIALS,
            403: termgr.UNAUTHORIZED('auf diesem Terminal die Digital Signage Anwendung zu aktivieren')
        }
    });
};


/*
    Actually disables the application.
*/
termgr.disableApplication = function (tid, cid) {
    const data = termgr.getData(tid, cid);
    data['disable'] = true;

    jQuery.ajax({
        url: termgr.BASE_URL + '/administer/application',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function () {
            swal({
                title: 'OK.',
                text: 'Digital Signage Anwendung wurde deaktiviert.',
                type: 'success'
            });
        },
        error: function () {
            swal({
                title: 'Fehler.',
                text: 'Digital Signage Anwendung konnte nicht deaktiviert werden.',
                type: 'error'
            });
        },
        statusCode: {
            401: termgr.INVALID_CREDENTIALS,
            403: termgr.UNAUTHORIZED('auf diesem Terminal die Digital Signage Anwendung zu deaktivieren')
        }
    });
};


/*
    Deploys the respective terminal.
*/
termgr.deploy = function (tid, cid) {
    const data = termgr.getData(tid, cid);

    jQuery.ajax({
        url: termgr.BASE_URL + '/administer/deploy',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function () {
            swal({
                title: 'OK.',
                text: 'Terminal wurde als "verbaut" markiert.',
                type: 'success'
            });
        },
        error: function () {
            swal({
                title: 'Fehler.',
                text: 'Das Terminal konnte nicht als "verbaut" markiert werden.',
                type: 'error'
            });
        },
        statusCode: {
            401: termgr.INVALID_CREDENTIALS,
            403: termgr.UNAUTHORIZED('dieses Terminal als "verbaut" zu markieren')
        }
    });
};


/*
    Un-deploys the respective terminal.
*/
termgr.undeploy = function (tid, cid) {
    const data = termgr.getData(tid, cid);
    data['undeploy'] = true;

    jQuery.ajax({
        url: termgr.BASE_URL + '/administer/deploy',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function () {
            swal({
                title: 'OK.',
                text: 'Terminal wurde als "nicht verbaut" markiert.',
                type: 'success'
            });
        },
        error: function () {
            swal({
                title: 'Fehler.',
                text: 'Das Terminal konnte nicht als "nicht verbaut" markiert werden.',
                type: 'error'
            });
        },
        statusCode: {
            401: termgr.INVALID_CREDENTIALS,
            403: termgr.UNAUTHORIZED('dieses Terminal als "nicht verbaut" zu markieren')
        }
    });
};


/*
    Synchronizes the respective terminal.
*/
termgr.sync = function (tid, cid) {
    const data = termgr.getData(tid, cid);

    jQuery.ajax({
        url: termgr.BASE_URL + '/administer/sync',
        type: 'POST',
        data: JSON.stringify(data),
        contentType: 'application/json',
        success: function () {
            swal({
                title: 'OK.',
                text: 'Terminal wurde synchronisiert.',
                type: 'success'
            });
        },
        error: function () {
            swal({
                title: 'Fehler.',
                text: 'Das Terminal konnte nicht synchronisiert werden.',
                type: 'error'
            });
        },
        statusCode: {
            401: termgr.INVALID_CREDENTIALS,
            403: termgr.UNAUTHORIZED('dieses Terminal zu synchronisieren')
        }
    });
};


/*
    Returns the respective address as a one-line string.
*/
termgr._addressToString = function (address) {
    return address.street + ' ' + address.houseNumber + ', ' + address.zipCode + ' ' + address.city;
};


/*
    Generates a terminal DOM entry.
*/
termgr.terminalEntry = function (terminal, cid) {
    const icon = document.createElement('i');
    icon.setAttribute('class', 'fa fa-tv');

    const columnIcon = document.createElement('td');
    columnIcon.setAttribute('class', 'col-xs-1');
    columnIcon.appendChild(icon);

    const description = document.createElement('p');
    description.setAttribute('class', 'termgr-terminal-description');
    description.textContent = termgr._addressToString(terminal.address) + ' (' + terminal.tid + '.' + cid + ')';

    const columnDescription = document.createElement('td');
    columnDescription.setAttribute('class', 'col-xs-6 termgr-terminal-description');
    columnDescription.appendChild(description);

    const btnBeepIcon = document.createElement('i');
    btnBeepIcon.setAttribute('class', 'fa fa-volume-up termgr-terminal-icon');

    const btnBeep = document.createElement('button');
    btnBeep.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnBeep.setAttribute('type', 'button');
    btnBeep.setAttribute('onclick', 'termgr.beep(' + terminal.tid + ', ' + cid + ');');
    btnBeep.setAttribute('data-toggle', 'tooltip');
    btnBeep.setAttribute('data-placement', 'bottom');
    btnBeep.setAttribute('title', 'Beep');
    btnBeep.appendChild(btnBeepIcon);

    const btnRebootIcon = document.createElement('i');
    btnRebootIcon.setAttribute('class', 'fa fa-power-off');

    const btnReboot = document.createElement('button');
    btnReboot.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnReboot.setAttribute('type', 'button');
    btnReboot.setAttribute('onclick', 'termgr.queryReboot(' + terminal.tid + ', ' + cid + ');');
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
    btnDeploy.setAttribute('data-whatever', terminal.tid + '.' + cid);
    btnDeploy.appendChild(btnDeployIcon);

    const btnApplicationIcon = document.createElement('i');
    btnApplicationIcon.setAttribute('class', 'fa fa-desktop');

    const btnApplication = document.createElement('button');
    btnApplication.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnApplication.setAttribute('type', 'button');
    btnApplication.setAttribute('data-toggle', 'modal');
    btnApplication.setAttribute('data-target', '#applicationDialog');
    btnApplication.setAttribute('data-whatever', terminal.tid + '.' + cid);
    btnApplication.appendChild(btnApplicationIcon);

    const btnSyncIcon = document.createElement('i');
    btnSyncIcon.setAttribute('class', 'fa fa-sync');

    const btnSync = document.createElement('button');
    btnSync.setAttribute('class', 'btn btn-success termgr-terminal-action');
    btnSync.setAttribute('type', 'button');
    btnSync.setAttribute('onclick', 'termgr.sync(' + terminal.tid + ', ' + cid + ');');
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
    Generates a customer DOM entry.
*/
termgr.customerEntry = function (customer) {
    const caption = document.createElement('h3');
    caption.setAttribute('class', 'termgr-customer-caption');
    caption.innerHTML = customer.name + ' (' + customer.id + ')';

    const captionContainer = document.createElement('span');
    captionContainer.setAttribute('onclick', 'jQuery("#terminals_' + customer.id + '").toggle();');
    captionContainer.appendChild(caption);

    const terminals = document.createElement('table');
    terminals.setAttribute('id', 'terminals_' + customer.id);
    terminals.setAttribute('class', 'termgr-customer-terminals');
    terminals.setAttribute('style', 'display:none;');

    for (let terminal of customer.terminals) {
        terminals.appendChild(termgr.terminalEntry(terminal, customer.id));
    }

    const entry = document.createElement('div');
    entry.setAttribute('class', 'row row-centered termgr-customer-entry');
    entry.appendChild(captionContainer);
    entry.appendChild(terminals);

    return entry;
};


/*
    Prepares the respective dialog.
*/
termgr.initDialog = function (negativeAction, positiveAction) {
    return function (event) {
        // Button that triggered the modal.
        const button = jQuery(event.relatedTarget);
        // Extract info from data-* attributes and convert to string.
        const terminalId = '' + button.data('whatever');
        const [tid, cid] = terminalId.split('.');
        const modal = jQuery(this)
        modal.find('#terminalId').text(terminalId);

        const negativeActionButton = modal.find('#negativeAction');
        negativeActionButton.unbind('click');
        negativeActionButton.click(function () {
            negativeAction(tid, cid);
            modal.modal('hide');
        });

        const positiveActionButton = modal.find('#positiveAction');
        positiveActionButton.unbind('click');
        positiveActionButton.click(function () {
            positiveAction(tid, cid);
            modal.modal('hide');
        });
    };
};


/*
    Performs the initial login.
*/
termgr.login = function () {
    jQuery('#customerList').hide();
    jQuery('#loader').show();
    termgr.getCustomers().then(termgr.listFiltered);
};


/*
    Hides the loader.
*/
termgr.hideLoader = function () {
    jQuery('#loader').hide();
    jQuery('#customerList').show();
};


/*
    Runs on document.ready().
*/
termgr.init = function () {
    jQuery('#applicationDialog').on('show.bs.modal', termgr.initDialog(termgr.disableApplication, termgr.enableApplication));
    jQuery('#deploymentDialog').on('show.bs.modal', termgr.initDialog(termgr.undeploy, termgr.deploy));
    const observer = new MutationObserver(termgr.hideLoader);
    const targetNode = document.getElementById('customerList');
    const config = {attributes: false, childList: true};
    observer.observe(targetNode, config);
};


jQuery(document).ready(termgr.init)
