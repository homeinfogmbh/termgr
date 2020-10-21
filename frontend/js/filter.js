/*
    filter.js - Terminal Manager systems filtering.

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

import { addressToString } from 'https://javascript.homeinfo.de/mdb.js';


/*
    Case-insensitively returns the index of the substring.
*/
function includesIgnoreCase (haystack, needle) {
    if (! haystack)
        return false;

    return haystack.toLowerCase().includes(needle.toLowerCase());
}


/*
    Matches a deployment.
*/
function matchDeployment (deployment, keyword) {
    const cid = '' + deployment.customer.id;

    if (includesIgnoreCase(cid, keyword))
        return true;

    const customerName = deployment.customer.company.name;

    if (includesIgnoreCase(customerName, keyword))
        return true;

    const address = addressToString(deployment.address);

    if (includesIgnoreCase(address, keyword))
        return true;

    return false;
}


/*
    Extracts the ID from a filter keyword.
*/
function extractId (keyword) {
    let fragments = null;

    if (keyword.startsWith('#')) {
        fragments = keyword.split('#');
        return parseInt(fragments[1]);
    }

    if (keyword.endsWith('!')) {
        fragments = keyword.split('!');
        return parseInt(fragments[0]);
    }

    return null;
}


/*
    Filters the provided systems by the respective keyword.
*/
function *filterSystems (systems, keyword) {
    const id = extractId(keyword);

    for (const system of systems) {
        // Yield any copy on empty keyword.
        if (keyword == null || keyword == '') {
            yield system;
            continue;
        }

        // Exact ID matching.
        if (id != null && id != NaN) {
            if (system.id == id)
                yield system;

            continue;
        }

        let deployment = system.deployment;

        if (deployment == null)
            continue;

        if (matchDeployment(deployment, keyword))
            yield system;
    }
}


/*
    Filters the provided depoloyments by the respective keyword.
*/
function *filterDeployments (deployments, keyword) {
    const id = extractId(keyword);

    for (const deployment of deployments) {
        // Yield any deployment on empty keyword.
        if (keyword == null || keyword == '') {
            yield deployment;
            continue;
        }

        // Exact ID matching.
        if (id != null && id != NaN) {
            if (deployment.id == id)
                yield deployment;

            continue;
        }

        if (matchDeployment(deployment, keyword))
            yield deployment;
    }
}


/*
    Returns the filter keyword.
*/
function getKeyword (id = 'searchField') {
    return document.getElementById(id).value.trim();
}


/*
    Filters systems.
*/
export function autoFilterSystems (systems) {
    systems = filterSystems(systems, getKeyword());
    return Array.from(systems);
}


/*
    Filters deployments.
*/
export function autoFilterDeployments (deployments) {
    deployments = filterDeployments(deployments, getKeyword());
    return Array.from(deployments);
}
