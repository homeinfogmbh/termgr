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


function deploy () {
    const system = JSON.parse(localStorage.getItem('termgr.system'));
    const customerSelect = document.getElementById('customer');
    const customer = customerSelect.options[customerSelect.selectedIndex].value;
    const street = document.getElementById('street').value.trim();
    const houseNumber = document.getElementById('houseNumber').value.trim();
    const zipCode = document.getElementById('zipCode').value.trim();
    const city = document.getElementById('city').value.trim();
    return termgr.deploy(system, customer, street, houseNumber, zipCode, city);
}


/*
    Initialize deploy.html.
*/
function init () {
    termgr.getCustomers().then(termgr.renderCustomers);
    const btnDeploy = document.getElementById('deploy');
    btnDeploy.addEventListener('click', termgr.partial(deploy), false);
}


document.addEventListener('DOMContentLoaded', init);
