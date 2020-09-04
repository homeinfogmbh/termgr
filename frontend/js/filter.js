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
termgr.filter = {};


/*
    Case-insensitively returns the index of the substring.
*/
termgr.filter.includesIgnoreCase = function (haystack, needle) {
    if (! haystack)
        return false;

    return haystack.toLowerCase().includes(needle.toLowerCase());
};


/*
    Matches a deployment.
*/
termgr.filter.matchDeployment = function (deployment, keyword) {
    const cid = '' + deployment.customer.id;

    if (termgr.filter.includesIgnoreCase(cid, keyword))
        return true;

    const customerName = deployment.customer.company.name;

    if (termgr.filter.includesIgnoreCase(customerName, keyword))
        return true;

    const address = termgr.addressToString(deployment.address);

    if (termgr.filter.includesIgnoreCase(address, keyword))
        return true;

    return false;
};

/*
    Filters the provided systems by the respective keyword.
*/
termgr.filter._systems = function* (systems, keyword) {
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

            if (system.id == id)
                yield system;

            continue;
        }

        let deployment = system.deployment;

        if (deployment == null)
            continue;

        if (termgr.filter.matchDeployment(deployment, keyword)) {
            yield system;
            continue;
        }
    }
};


/*
    Filters the provided depoloyments by the respective keyword.
*/
termgr.filter._deployments = function* (deployments, keyword) {
    for (const deployment of deployments) {
        // Yield any copy on empty keyword.
        if (keyword == null || keyword == '') {
            yield deployment;
            continue;
        }

        // Exact ID matching.
        if (keyword.startsWith('#')) {
            let fragments = keyword.split('#');
            let id = parseInt(fragments[1]);

            if (deployment.id == id)
                yield deployment;

            continue;
        }

        if (termgr.filter.matchDeployment(deployment, keyword)) {
            yield deployment;
            continue;
        }
    }
};


/*
    Filters systems.
*/
termgr.filter.systems = function (systems) {
    const keyword = document.getElementById('searchField').value;
    systems = termgr.filter._systems(systems, keyword);
    return Array.from(systems);
};


/*
    Filters deployments.
*/
termgr.filter.deployments = function (deployments) {
    const keyword = document.getElementById('searchField').value;
    deployments = termgr.filter._deployments(deployments, keyword);
    return Array.from(deployments);
};
