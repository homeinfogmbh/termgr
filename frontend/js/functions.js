/*
    functions.js - Terminal Manager functions library.

    (C) 2019-2020 HOMEINFO - Digitale Informationssysteme GmbH

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

/*
    Returns the respective address as a one-line string.
    TODO: Migrate to mdb.
*/
export function addressToString (address) {
    return address.street + ' ' + address.houseNumber + ', ' + address.zipCode + ' ' + address.city;
}


/*
    Returns the respective customer as a one-line string.
    TODO: Migrate to mdb.
*/
export function customerToString (customer) {
    return customer.company.name  + ' (' + customer.id + ')';
}


/*
    Returns the respective deployment as a one-line string.
    TODO: Migrate to hwdb.
*/
export function deploymentToString (deployment) {
    return deployment.id + ': ' + addressToString(deployment.address);
}


/*
    Wraps a function and disables the default event.
*/
export function suppressEvent (func, ...args) {
    return function (event) {
        if (event != null)
            event.preventDefault();

        return func(...args);
    };
}
