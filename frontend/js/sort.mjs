/*
    filter.mjs - Terminal Manager systems filtering.

    (C) 2019-2021 HOMEINFO - Digitale Informationssysteme GmbH

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

import { addressToString } from 'https://javascript.homeinfo.de/mdb.mjs';


/*
    Returns a compare function for systems.
*/
function compareSystems (desc, byId) {
    const factor = desc ? -1 : 1;

    if (byId)
        return function (alice, bob) {
            if (alice.id > bob.id)
                return factor;

            if (bob.id > alice.id)
                return -factor;

            return 0
        };

    return function (alice, bob) {
        const deploymentA = alice.deployment;
        const deploymentB = bob.deployment;

        if (deploymentA == null) {
            if (deploymentB == null)
                return 0;

            return Infinity * factor;
        }

        if (deploymentB == null)
            return -Infinity * factor;

        const addressA = addressToString(deploymentA.address);
        const addressB = addressToString(deploymentB.address);

        if (addressA > addressB)
            return factor;

        if (addressB > addressA)
            return -factor;

        return 0;
    };
}


/*
    Returns a compare functionm for deployments.
*/
function compareDeployments (desc, byId) {
    const factor = desc ? -1 : 1;

    return function (alice, bob) {
        let value = 0;

        if (byId) {
            if (alice.id > bob.id)
                value = 1;
            else if (bob.id > alice.id)
                value = -1;
        } else {
            const addressA = addressToString(alice.address);
            const addressB = addressToString(bob.address);

            if (addressA > addressB)
                value = 1;
            else if (addressB > addressA)
                value = -1;
        }

        value = factor * value;
        return value;
    };
}


/*
    Reads the sorting settings from the respective checkboxes.
*/
function getSettings () {
    const desc = document.getElementById('sortDesc').checked;
    const byId = document.getElementById('sortById').checked;
    return [desc, byId];
}


/*
    Sorts the systems.
*/
export function sortSystems (systems) {
    systems.sort(compareSystems(...getSettings()));
    return systems;
}


/*
    Sorts the deployments.
*/
export function sortDeployments (deployments) {
    deployments.sort(compareDeployments(...getSettings()));
    return deployments;
}
