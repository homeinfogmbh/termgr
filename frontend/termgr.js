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

termgr = termgr || {};

termgr.BASE_URL = "https://termgr.homeinfo.de";

termgr.containsIgnoreCase = function (haystack, needle) {
  return haystack.toLowerCase().indexOf(needle.toLowerCase()) >= 0;
}


termgr.getCredentials = function () {
  return {'user_name': $("#userName").val(), 'passwd': $("#passwd").val()};
}


termgr.getCustomers = function (callback) {
  var credentials = termgr.getCredentials();

  $.ajax({
    url: termgr.BASE_URL + '/administer/deploy',
    type: 'POST',
    data: JSON.stringify(credentials),
    success: function (json) {
      callback(json);
    },
    error: function() {
      swal({
        title: 'Konnte Terminaldaten nicht abfragen.',
        text: 'Bitte kontrollieren Sie Ihren Benutzernamen und Ihr Passwort oder versuchen Sie es später noch ein Mal.',
        type: 'error'
      })
    }
  });
}


termgr.filterTerminals = function (terminals, keywords) {
  var filteredTerminals = [];
  var terminal = null;
  var keyword = null;

  for (var i = 0; i < terminals.length; i++) {
    terminal = terminals[i];

    for (var j = 0; j < keywords.length; j++) {
      keyword = keywords[j];

      if (termgr.containsIgnoreCase('' + terminal.tid, keyword)) {
        filteredTerminals.push(terminal);
      } else if (termgr.containsIgnoreCase('' + terminal.cid, keyword)) {
        filteredTerminals.push(terminal);
      } else if (termgr.containsIgnoreCase(terminal.location, keyword)) {
        filteredTerminals.push(terminal);
      }
    }
  }

  return filteredTerminals;
}


termgr.filterCustomer = function (customer, keywords) {
  for (var i = 0; i < keywords.length; i++) {
    if (termgr.containsIgnoreCase(customer.name, keywords[i])) {
      return customer;
    }
  }

  var terminals = termgr.filterTerminals(customer.terminals, keywords);

  if (terminals.length > 0) {
    return {'id': customer.id, 'name': customer.name, 'terminals': terminals};
  }

  return null;
}


termgr.filterCustomers = function (customers, keywords) {
  var customers = [];

  for (var i = 0; i < customers.length; i++) {
    customer = termgr.filterCustomer(customer, keywords);

    if (customer != null) {
      customers.push(customer);
    }
  }

  return customers;
}


termgr.listCustomers = function (customers) {
  var customerList = document.getElementById("customerList");
  customerList.innerHTML = '';
  var filters = getFilters();

  for (cidStr in customers) {
    if (customers.hasOwnProperty(cidStr)) {
      if (customers[cidStr] != null) {
        customerList.appendChild(termgr.customerEntry(customers[cidStr]));
      }
    }
  }
}


termgr.doReboot = function(tid, cid) {
  var data = termgr.getCredentials();
  data['tid'] = tid;
  data['cid'] = cid;

  $.ajax({
    url: termgr.BASE_URL + '/administer/reboot',
    type: 'POST',
    data: JSON.stringify(data),
    success: function (message) {
      swal({
        title: 'OK,',
        html: 'Terminal wurde neu gestartet.',
        type: 'success'
      })
    },
    error: function () {
      swal({
        title: 'Fehler,',
        html: 'Das Terminal konnte nicht neu gestartet werden.',
        type: 'error'
      })
    }
  });
}


termgr.reboot = function (tid, cid) {
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
      termgr.doReboot(tid, cid);
    } else if (result.dismiss === swal.DismissReason.cancel) {
      swal({
        title: 'Abgebrochen.',
        text: 'Das Terminal ' + tid + '.' + cid + ' wird nicht neu gestartet,',
        type: 'error'
      })
    }
  })
}


termgr.Client = function (userName, passwd) {
  this.userName = userName;
  this.passwd = passwd

  this.getData = function (terminal) {
    var data = {'user_name': userName, 'passwd': passwd};

    if (terminal != null) {
      data['cid'] = terminal.cid;
      data['tid'] = terminal.tid;
    }

    return data;
  }

  this.deploy = function(terminal, success, error, undeploy) {
    var data = this.getData(terminal);

    if (undeploy) {
      data['undeploy'] = true;
    }

    $.ajax({
      url: termgr.BASE_URL + '/administer/deploy',
      type: 'POST',
      data: JSON.stringify(data),
      success: success,
      error: error
    });
  }

  this.undeploy = function(terminal, success, error) {
    this.deploy(terminal, success, error, true);
  }

  this.enableApplication = function(terminal, success, error, disable) {
    var data = this.getData(terminal);

    if (disable) {
      data['disable'] = true;
    }

    $.ajax({
      url: termgr.BASE_URL + '/administer/application',
      type: 'POST',
      data: JSON.stringify(data),
      success: success,
      error: error
    });
  }

  this.disableApplication = function(terminal, success, error) {
    this.enableApplication(terminal, success, error, true);
  }
}


termgr.Terminal = function(json) {
  for (var prop in json) {
    if (json.hasOwnProperty(prop)) {
        this[prop] = json[prop];
    }
  }

  this.getId = function() {
    return this.tid + '.' + this.customer.cid;
  }

  this.getDescription = function() {
    return
  }
}


termgr.terminalEntry = function(terminal) {
  var icon = document.createElement('i');
  icon.setAttribute('class', 'fa fa-television');

  var columnIcon = document.createElement('div');
  columnIcon.setAttribute('class', 'col-m-1');
  columnIcon.appendChild(icon);

  var btnBeepIcon = document.createElement('i');
  btnBeepIcon.setAttribute('class', 'fa fa-volume-up');

  var btnBeep = document.createElement('button');
  btnBeep.setAttribute('class', 'btn btn-success');
  btnBeep.setAttribute('type', 'button');
  btnBeep.setAttribute('onclick', 'termgr.beep(' + terminal.customer.id + ', ' + terminal.tid + ');');
  btnBeep.appendChild(btnBeepIcon);

  var btnRebootIcon = document.createElement('i');
  btnRebootIcon.setAttribute('class', 'fa fa-power-off');

  var btnReboot = document.createElement('button');
  btnReboot.setAttribute('class', 'btn btn-success');
  btnReboot.setAttribute('type', 'button');
  btnReboot.setAttribute('onclick', 'termgr.reboot(' + terminal.customer.id + ', ' + terminal.tid + ');');
  btnReboot.appendChild(btnRebootIcon);

  var btnApplicationIcon = document.createElement('i');
  btnApplicationIcon.setAttribute('class', 'fa fa-desktop');

  var btnApplication = document.createElement('button');
  btnApplication.setAttribute('class', 'btn btn-success');
  btnApplication.setAttribute('type', 'button');
  btnApplication.setAttribute('onclick', 'termgr.application(' + terminal.customer.id + ', ' + terminal.tid + ');');
  btnApplication.appendChild(btnApplicationIcon);

  var btnSyncIcon = document.createElement('i');
  btnSyncIcon.setAttribute('class', 'fa fa-sync');

  var btnSync = document.createElement('button');
  btnSync.setAttribute('class', 'btn btn-success');
  btnSync.setAttribute('type', 'button');
  btnSync.setAttribute('onclick', 'termgr.sync(' + terminal.customer.id + ', ' + terminal.tid + ');');
  btnSync.appendChild(btnSyncIcon);

  var columnButtons = document.createElement('div');
  columnButtons.setAttribute('class', 'col-m-5');
  columnButtons.appendChild(btnBeep);
  columnButtons.appendChild(btnReboot);
  columnButtons.appendChild(btnApplication);
  columnButtons.appendChild(btnSync);

  var description = document.createElement('p');
  description.innerHTML = terminal.getDescription();

  var columnDescription = document.createElement('div');
  columnDescription.setAttribute('class', 'col-m-6');
  columnDescription.appendChild(description);

  var entry = document.createElement('div');
  entry.setAttribute('class', 'row');
  entry.appendChild(columnIcon);
  entry.appendChild(columnButtons);
  entry.appendChild(columnDescription);

  return entry;
}


termgr.customerEntry = function (customer) {
  var caption = document.createElement('p');
  caption.innerHTML = customer.name;

  var terminals = document.createElement('div');

  for (var i = 0; i < customer.terminals.length; i++) {
    terminals.appendChild(termgr.terminalEntry(customer.terminals[i]));
  }

  var entry = document.createElement('div');
  entry.setAttribute('class', 'row');
  entry.appendChild(caption);
  entry.appendChild(terminals);

  return entry;
}


termgr.main = function () {
  
