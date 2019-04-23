/*
    termgr.js - Terminal Manager deployment management.

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


function deploy (system) {
    const customerSelect = document.getElementById('customer');
    const customer = customerSelect.options[customerSelect.selectedIndex].value;
    const street = document.getElementById('street').value.trim();
    const houseNumber = document.getElementById('houseNumber').value.trim();
    const zipCode = document.getElementById('zipCode').value.trim();
    const city = document.getElementById('city').value.trim();
    const address = {
        street: street,
        houseNumber: houseNumber,
        zipCode: zipCode,
        city: city
    };
    const connectionSelect = document.getElementById('connection');
    const connection = connectionSelect.options[connectionSelect.selectedIndex].value;
    const typeSelect = document.getElementById('type');
    const type = typeSelect.options[typeSelect.selectedIndex].value;
    const weather = document.getElementById('weather').value.trim() || null;
    const annotation = document.getElementById('annotation').value.trim() || null;
    return termgr.deploy(system, customer, address, connection, type, weather, annotation);
}


/*
    Initialize deploy.html.
*/
function init () {
    termgr.startLoading();
    const id = parseInt(termgr.getArg('System'));
    const systemId = document.getElementById('system');
    systemId.textContent = id;
    const getCustomers = termgr.getCustomers().then(
        function (response) {
            termgr.renderCustomers(response.json);
        }
    );
    const getConnections = termgr.getConnections().then(
        function (response) {
            termgr.renderConnections(response.json);
        }
    );
    const getTypes = termgr.getTypes().then(
        function (response) {
            termgr.renderTypes(response.json);
        }
    );
    Promise.all([getCustomers, getConnections, getTypes]).then(termgr.stopLoading);
    const btnDeploy = document.getElementById('deploy');
    btnDeploy.addEventListener('click', termgr.partial(deploy, id), false);
}


document.addEventListener('DOMContentLoaded', init);
