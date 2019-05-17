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
termgr.sort = {};


/*
    Returns a compare function for systems.
*/
termgr.sort.compareSystems = function () {
    const desc = document.getElementById('sortDesc').checked;
    const byId = document.getElementById('sortById').checked;
    const factor = desc ? -1 : 1;

    return function (alice, bob) {
        let value = 0;

        if (byId) {
            if (alice.id > bob.id) {
                value = 1;
            } else if (bob.id > alice.id) {
                value = -1;
            }
        } else {
            const deploymentA = alice.deployment;
            const deploymentB = bob.deployment;

            if (deploymentA == null) {
                if (deploymentB == null) {
                    value = 0;
                }

                value = Infinity;
            } else if (deploymentB == null) {
                value = -Infinity;
            } else {
                const addressA = termgr.addressToString(deploymentA.address);
                const addressB = termgr.addressToString(deploymentB.address);

                if (addressA > addressB) {
                    value = 1;
                } else if (addressB > addressA) {
                    value = -1;
                }
            }
        }

        value = factor * value;
        return value;
    };
};


/*
    Returns a compare functionm for deployments.
*/
termgr.sort.compareDeployments = function () {
    const desc = document.getElementById('sortDesc').checked;
    const byId = document.getElementById('sortById').checked;
    const factor = desc ? -1 : 1;

    return function (alice, bob) {
        let value = 0;

        if (byId) {
            if (alice.id > bob.id) {
                value = 1;
            } else if (bob.id > alice.id) {
                value = -1;
            }
        } else {
            const addressA = termgr.addressToString(alice.address);
            const addressB = termgr.addressToString(bob.address);

            if (addressA > addressB) {
                value = 1;
            } else if (addressB > addressA) {
                value = -1;
            }
        }

        value = factor * value;
        return value;
    };
};


/*
    Sorts the systems.
*/
termgr.sort.systems = function (systems) {
    systems.sort(termgr.sort.compareSystems());
    return systems;
};


/*
    Sorts the deployments.
*/
termgr.sort.deployments = function (deployments) {
    deployments.sort(termgr.sort.compareDeployments());
    return deployments;
};
