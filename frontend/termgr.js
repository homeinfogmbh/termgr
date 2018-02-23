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
    * sweetalert2.js
*/
"use strict";

var termgr = termgr || {};

termgr.BASE_URL = "https://termgr.homeinfo.de";

termgr.customer = null;


/*
  Case-insensitively checks whether a string contains another string.
*/
termgr.containsIgnoreCase = function (haystack, needle) {
  return haystack.toLowerCase().indexOf(needle.toLowerCase()) >= 0;
}


/*
  Returns the user name and password from the respective input fields.
*/
termgr.getCredentials = function () {
  return {'user_name': $("#userName").val(), 'passwd': $("#passwd").val()};
}


/*
  Returns the basic post data for the respective terminal.
*/
termgr.getData = function (tid, cid) {
  var data = termgr.getCredentials();
  data['tid'] = tid;
  data['cid'] = '' + cid;   // Backend needs a string here.
  return data;
}


/*
  Retrieves the customers and their respective terminals
  from the API and invokes the callback function.
*/
termgr.getCustomers = function (callback) {
  var credentials = termgr.getCredentials();

  $.ajax({
    url: termgr.BASE_URL + '/check/list',
    type: 'POST',
    data: JSON.stringify(credentials),
    success: function (customers) {
      termgr.customers = customers;
      callback(customers);
    },
    error: function() {
      swal({
        title: 'Konnte Terminaldaten nicht abfragen.',
        html: 'Bitte kontrollieren Sie Ihren Benutzernamen und Ihr Passwort<br>oder versuchen Sie es später noch ein Mal.',
        type: 'error'
      });
      $('#loader').hide();
    }
  });
}


/*
  Filters the provided terminals by the respective keywords.
*/
termgr.filterTerminals = function (terminals, keywords) {
  var filteredTerminals = [];

  for (var i = 0; i < terminals.length; i++) {
    var terminal = terminals[i];
    var matching = true;

    for (var j = 0; j < keywords.length; j++) {
      var keyword = keywords[j];
      var matchingTid = termgr.containsIgnoreCase('' + terminal.tid, keyword);
      var matchingCid = termgr.containsIgnoreCase('' + terminal.cid, keyword);
      var matchingLocation = termgr.containsIgnoreCase(terminal.location, keyword);

      if (! (matchingTid || matchingCid || matchingLocation)) {
        matching = false;
        break;
      }
    }

    if (matching) {
      filteredTerminals.push(terminal);
    }
  }

  return filteredTerminals;
}


/*
  Filters the provided customer by the respective keywords.
*/
termgr.filterCustomer = function (customer, keywords) {
  var customerMatch = true;

  for (var i = 0; i < keywords.length; i++) {
    if (! termgr.containsIgnoreCase(customer.name, keywords[i])) {
      customerMatch = false;
      break;
    }
  }

  if (customerMatch) {
    return customer;
  }

  var terminals = termgr.filterTerminals(customer.terminals, keywords);

  if (terminals.length > 0) {
    return {'id': customer.id, 'name': customer.name, 'terminals': terminals};
  }

  return null;
}


/*
  Filters the provided customers by the respective keywords.
*/
termgr.filterCustomers = function (customers, keywords) {
  var filteredCustomers = {};

  for (var cidStr in customers) {
    if (customers.hasOwnProperty(cidStr)) {
      var customer = termgr.filterCustomer(customers[cidStr], keywords);

      if (customer != null) {
        filteredCustomers[cidStr] = customer;
      }
    }
  }

  return filteredCustomers;
}


/*
  Lists the provided customers.
*/
termgr.listCustomers = function (customers) {
  var customerList = document.getElementById("customerList");
  customerList.innerHTML = '';

  for (var cidStr in customers) {
    if (customers.hasOwnProperty(cidStr)) {
      if (customers[cidStr] != null) {
        customerList.appendChild(termgr.customerEntry(customers[cidStr]));
      }
    }
  }

  $('#loader').hide();
  $('#customerList').show();
}


/*
  Filters customers and terminals and lists them.
*/
termgr.listFiltered = function (customers) {
  if (customers == null) {
    var customers = termgr.customers;
  }

  var searchValue = $('#searchField').val();

  if (searchValue.length > 0) {
    var keywords = searchValue.split();

    if (keywords.length > 0) {
      customers = termgr.filterCustomers(customers, keywords);
    }
  }

  termgr.listCustomers(customers);
}


/*
  Lets the respecive terminal beep.
*/
termgr.beep = function (tid, cid) {
  var data = termgr.getData(tid, cid);

  $.ajax({
    url: termgr.BASE_URL + '/check/identify',
    type: 'POST',
    data: JSON.stringify(data),
    error: function (jqXHR, textStatus, errorThrown) {
      swal({
        title: 'Fehler.',
        text: 'Das Terminal konnte nicht zum Piepen gebracht werden.',
        type: 'error'
      })
    },
    success: function () {
      swal({
        title: 'OK.',
        text: 'Das Terminal sollte gepiept haben.',
        type: 'success'
      })
    }
  });
}


/*
  Actually performs a reboot of the respective terminal.
*/
termgr.reboot = function(tid, cid) {
  var data = termgr.getData(tid, cid);

  $.ajax({
    url: termgr.BASE_URL + '/administer/reboot',
    type: 'POST',
    data: JSON.stringify(data),
    error: function (jqXHR, textStatus, errorThrown) {
      swal({
        title: 'Das Terminal konnte nicht neu gestartet werden.',
        html: '<pre>' + jqXHR.responseText + '</pre>',
        type: 'error'
      })
    },
    statusCode: {
      200: function () {
        swal({
          title: 'OK.',
          text: 'Das Terminal wurde neu gestartet.',
          type: 'success'
        })
      },
      202: function () {
        swal({
          title: 'OK.',
          text: 'Das Terminal wurde wahrscheinlich neu gestartet.',
          type: 'success'
        })
      },
      403: function () {
        swal({
          title: 'Fehler.',
          text: 'Sie sind nicht berechtigt, dieses Terminal neu zu starten.',
          type: 'error'
        })
      },
      503: function () {
        swal({
          title: 'Zur Zeit nicht möglich.',
          text: 'Auf dem Terminal werden aktuell administrative Aufgaben ausgeführt.',
          type: 'error'
        })
      }
    }
  });
}


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
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Ja, neu starten!',
    cancelButtonText: 'Nein, abbrechen!',
    confirmButtonClass: 'btn btn-success',
    cancelButtonClass: 'btn btn-danger',
    buttonsStyling: false,
    reverseButtons: true
  }).then((result) => {
    if (result.value) {
      termgr.reboot(tid, cid);
    } else if (result.dismiss === swal.DismissReason.cancel) {
      swal({
        title: 'Abgebrochen.',
        text: 'Das Terminal ' + tid + '.' + cid + ' wird nicht neu gestartet.',
        type: 'error'
      })
    }
  })
}


/*
  Actually enables the application.
*/
termgr.enableApplication = function(tid, cid) {
  var data = termgr.getData(tid, cid);

  $.ajax({
    url: termgr.BASE_URL + '/administer/application',
    type: 'POST',
    data: JSON.stringify(data),
    success: function () {
      swal({
        title: 'OK.',
        text: 'Application wurde aktiviert.',
        type: 'success'
      })
    },
    error: function () {
      swal({
        title: 'Fehler.',
        text: 'Application konnte nicht aktiviert werden.',
        type: 'error'
      })
    },
    statusCode: {
      403: function () {
        swal({
          title: 'Fehler.',
          text: 'Sie sind nicht berechtigt, auf diesem Terminal die Application zu aktivieren.',
          type: 'error'
        })
      }
    }
  });
}


/*
  Actually disables the application.
*/
termgr.disableApplication = function(tid, cid) {
  var data = termgr.getData(tid, cid);
  data['disable'] = true;

  $.ajax({
    url: termgr.BASE_URL + '/administer/application',
    type: 'POST',
    data: JSON.stringify(data),
    success: function () {
      swal({
        title: 'OK.',
        text: 'Application wurde deaktiviert.',
        type: 'success'
      })
    },
    error: function () {
      swal({
        title: 'Fehler.',
        text: 'Application konnte nicht deaktiviert werden.',
        type: 'error'
      })
    },
    statusCode: {
      403: function () {
        swal({
          title: 'Fehler.',
          text: 'Sie sind nicht berechtigt, auf diesem Terminal die Application zu deaktivieren.',
          type: 'error'
        })
      }
    }
  });
}


/*
  Deploys the respective terminal.
*/
termgr.deploy = function(tid, cid) {
  var data = termgr.getData(tid, cid);

  $.ajax({
    url: termgr.BASE_URL + '/administer/deploy',
    type: 'POST',
    data: JSON.stringify(data),
    success: function () {
      swal({
        title: 'OK.',
        text: 'Terminal wurde als "verbaut" markiert.',
        type: 'success'
      })
    },
    error: function () {
      swal({
        title: 'Fehler.',
        text: 'Das Terminal konnte nicht als "verbaut" markiert werden.',
        type: 'error'
      })
    },
    statusCode: {
      403: function () {
        swal({
          title: 'Fehler.',
          text: 'Sie sind nicht berechtigt, dieses Terminal als "verbaut" zu markieren.',
          type: 'error'
        })
      }
    }
  });
}


/*
  Un-deploys the respective terminal.
*/
termgr.undeploy = function(tid, cid) {
  var data = termgr.getData(tid, cid);

  if (undeploy) {
    data['undeploy'] = true;
  }

  $.ajax({
    url: termgr.BASE_URL + '/administer/deploy',
    type: 'POST',
    data: JSON.stringify(data),
    success: function () {
      swal({
        title: 'OK.',
        text: 'Terminal wurde als "nicht verbaut" markiert.',
        type: 'success'
      })
    },
    error: function () {
      swal({
        title: 'Fehler.',
        text: 'Das Terminal konnte nicht als "nicht verbaut" markiert werden.',
        type: 'error'
      })
    },
    statusCode: {
      403: function () {
        swal({
          title: 'Fehler.',
          text: 'Sie sind nicht berechtigt, dieses Terminal als "nicht verbaut" zu markieren.',
          type: 'error'
        })
      }
    }
  });
}


/*
  Generates a terminal DOM entry.
*/
termgr.terminalEntry = function(terminal) {
  var icon = document.createElement('i');
  icon.setAttribute('class', 'fa fa-tv');

  var columnIcon = document.createElement('td');
  columnIcon.setAttribute('class', 'col-xs-1');
  columnIcon.appendChild(icon);

  var description = document.createElement('p');
  description.setAttribute('class', 'termgr-terminal-description');
  description.innerHTML = terminal.location + ' (' + terminal.tid + '.' + terminal.cid + ')';

  var columnDescription = document.createElement('td');
  columnDescription.setAttribute('class', 'col-xs-6 termgr-terminal-description');
  columnDescription.appendChild(description);

  var btnBeepIcon = document.createElement('i');
  btnBeepIcon.setAttribute('class', 'fa fa-volume-up termgr-terminal-icon');

  var btnBeep = document.createElement('button');
  btnBeep.setAttribute('class', 'btn btn-success termgr-terminal-action');
  btnBeep.setAttribute('type', 'button');
  btnBeep.setAttribute('onclick', 'termgr.beep(' + terminal.tid + ', ' + terminal.cid + ');');
  btnBeep.appendChild(btnBeepIcon);

  var btnRebootIcon = document.createElement('i');
  btnRebootIcon.setAttribute('class', 'fa fa-power-off');

  var btnReboot = document.createElement('button');
  btnReboot.setAttribute('class', 'btn btn-success termgr-terminal-action');
  btnReboot.setAttribute('type', 'button');
  btnReboot.setAttribute('onclick', 'termgr.queryReboot(' + terminal.tid + ', ' + terminal.cid + ');');
  btnReboot.appendChild(btnRebootIcon);

  var btnApplicationIcon = document.createElement('i');
  btnApplicationIcon.setAttribute('class', 'fa fa-desktop');

  var btnApplication = document.createElement('button');
  btnApplication.setAttribute('class', 'btn btn-success termgr-terminal-action');
  btnApplication.setAttribute('type', 'button');
  //btnApplication.setAttribute('onclick', 'termgr.showApplicationDialog(' + terminal.tid + ', ' + terminal.cid + ');');
  btnApplication.setAttribute('data-toggle', 'modal');
  btnApplication.setAttribute('data-target', '#applicationDialog');
  btnApplication.setAttribute('data-whatever', terminal.tid + '.' + terminal.cid);
  btnApplication.appendChild(btnApplicationIcon);

  var btnSyncIcon = document.createElement('i');
  btnSyncIcon.setAttribute('class', 'fa fa-sync');

  var btnSync = document.createElement('button');
  btnSync.setAttribute('class', 'btn btn-success termgr-terminal-action');
  btnSync.setAttribute('type', 'button');
  btnSync.setAttribute('onclick', 'termgr.sync(' + terminal.tid + ', ' + terminal.cid + ');');
  btnSync.appendChild(btnSyncIcon);

  var columnButtons = document.createElement('td');
  columnButtons.setAttribute('class', 'col-xs-11');
  columnButtons.appendChild(btnBeep);
  columnButtons.appendChild(btnReboot);
  columnButtons.appendChild(btnApplication);
  columnButtons.appendChild(btnSync);

  var rowButtons = document.createElement('tr');
  rowButtons.appendChild(columnButtons);

  var rowDescription = document.createElement('tr');
  rowDescription.appendChild(columnDescription);

  var tableDescriptionAndButtons = document.createElement('table');
  tableDescriptionAndButtons.appendChild(rowDescription);
  tableDescriptionAndButtons.appendChild(rowButtons);

  var columnDescriptionAndButtons = document.createElement('td');
  columnDescriptionAndButtons.appendChild(tableDescriptionAndButtons);

  var entry = document.createElement('tr');
  entry.setAttribute('class', 'row row-centered termgr-terminal-entry');
  entry.appendChild(columnIcon);
  entry.appendChild(columnDescriptionAndButtons);

  return entry;
}


/*
  Generates a customer DOM entry.
*/
termgr.customerEntry = function (customer) {
  var caption = document.createElement('h3');
  caption.innerHTML = customer.name + ' (' + customer.id + ')';

  var captionContainer = document.createElement('span');
  captionContainer.setAttribute('onclick', '$("#terminals_' + customer.id + '").toggle();');
  captionContainer.appendChild(caption);

  var terminals = document.createElement('table');
  terminals.setAttribute('id', 'terminals_' + customer.id);
  terminals.setAttribute('class', 'termgr-customer-terminals');
  terminals.setAttribute('style', 'display:none;');

  for (var i = 0; i < customer.terminals.length; i++) {
    terminals.appendChild(termgr.terminalEntry(customer.terminals[i]));
  }

  var entry = document.createElement('div');
  entry.setAttribute('class', 'row row-centered termgr-customer-entry');
  entry.appendChild(captionContainer);
  entry.appendChild(terminals);

  return entry;
}


/*
  Prepares the application control dialog.
*/
termgr.prepareApplicationDialog = function (event) {
  // Button that triggered the modal.
  var button = $(event.relatedTarget);
  // Extract info from data-* attributes and convert to string.
  var terminalId = '' + button.data('whatever');
  var [tid, cid] = terminalId.split('.');
  var modal = $(this)

  var terminalIdField = modal.find('#terminalId');
  terminalIdField.text(terminalId);

  var disableButton = modal.find('#disableApplication');
  disableButton.unbind('click');
  disableButton.click(function () {
    termgr.disableApplication(tid, cid);
    $('#applicationDialog').modal('hide');
  });

  var enableButton = modal.find('#enableApplication');
  enableButton.unbind('click');
  enableButton.click(function () {
    termgr.enableApplication(tid, cid);
    $('#applicationDialog').modal('hide');
  });
}

/*
  Performs the initial login.
*/
termgr.login = function () {
  $('#customerList').hide();
  $('#loader').show();
  termgr.getCustomers(termgr.listFiltered);
}


termgr.init = function () {
  $('#applicationDialog').on('show.bs.modal', termgr.prepareApplicationDialog);
}


$(document).ready(termgr.init)
