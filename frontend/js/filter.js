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


termgr.FILTER_PATHS = [
    ['id'],
    ['deployment', 'customer', 'id'],
    ['deployment', 'customer', 'company', 'name'],
    ['deployment', 'address'],
];


/*
    Case-insensitively returns the index of the substring.
*/
termgr.indexOf = function (haystack, needle) {
    if (! haystack) {
        return false;
    }

    return haystack.toLowerCase().indexOf(needle.toLowerCase());
};


/*
    Returns the respective address as a one-line string.
*/
termgr.addressToString = function (address) {
    if (typeof address == 'string') {
        return address;
    }

    return address.street + ' ' + address.houseNumber + ', ' + address.zipCode + ' ' + address.city;
};


/*
    Highlights a substring.
*/
termgr.highlight = function (string, index, length) {
    const head = string.substring(0, index);
    const match = string.substr(index, length);
    const tail = string.substring(index + length, string.length);
    return head + '<b>' + match + '</b>' + tail;
};


/*
    Matches a search path on an object.
*/
termgr.matchPath = function (obj, path, keyword) {
    let parent, node;

    for (node of path) {
        parent = obj;
        obj = obj[node];

        if (obj == null) {
            return false;
        }
    }

    const string = '' + obj;
    const index = termgr.indexOf(string, keyword);

    if (index >= 0) {
        parent[node] = termgr.highlight(string, index, keyword.length);
        return true;
    }

    return false;
};


/*
    Filters the provided system by the respective keywords.
*/
termgr.filterSystems = function* (systems, keyword) {
    for (const system of systems) {
        let match = false;
        let copy = JSON.parse(JSON.stringify(system));

        // Prepare address as string.
        if (copy.deployment != null) {
            copy.deployment.address = termgr.addressToString(copy.deployment.address);
        }

        for (const path of termgr.FILTER_PATHS) {
            match = match | termgr.matchPath(copy, path, keyword);
        }

        if (match) {
            yield copy;
        }
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

    let systems = termgr.loadSystems();

    if (keywords != null) {
        systems = Array.from(termgr.filterSystems(systems, keywords));
        termgr.listSystems(systems);
    } else {
        termgr.listSystems(systems);
    }
};
