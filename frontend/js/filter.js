/*
    filter.js - Terminal Manager systems filtering.

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
    Case-insensitively returns the index of the substring.
*/
termgr.includesIgnoreCase = function (haystack, needle) {
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
    Filters the provided system by the respective keywords.
*/
termgr.filterSystems = function* (systems, keyword) {
    for (const system of systems) {
        // Yield any copy on empty keyword.
        if (keyword == null || keyword == '') {
            yield system;
            continue;
        }

        // Exact ID matching.
        if (keyword.startsWith('#')) {
            let fragments = keyword.split('#');
            let id = parseInt(fragments[1]);

            if (system.id == id) {
                yield system;
            }

            continue;
        }

        let deployment = system.deployment;

        if (deployment == null) {
            continue;
        }

        let cid = '' + deployment.customer.id;

        if (termgr.includesIgnoreCase(cid, keyword)) {
            yield system;
            continue;
        }

        let customerName = deployment.customer.company.name;

        if (termgr.includesIgnoreCase(customerName, keyword)) {
            yield system;
            continue;
        }

        let address = termgr.addressToString(deployment.address);

        if (termgr.includesIgnoreCase(address, keyword)) {
            yield system;
            continue;
        }
    }
};


/*
    Filters systems.
*/
termgr.listFilteredSystems = function () {
    const keyword = document.getElementById('searchField').value;
    const systems = Array.from(termgr.filterSystems(termgr.loadSystems(), keyword));
    termgr.listSystems(systems);
};
