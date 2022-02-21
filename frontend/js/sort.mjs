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


function compareNullable (desc) {
    const factor = desc ? -1 : 1;

    return function (alice, bob) {
        if (alice == null) {
            if (bob == null)
                return 0;

            return Infinity * factor;
        }

        if (bob == null)
            return -Infinity * factor;

        return null;
    };
};


function compareValues (desc) {
    const factor = desc ? -1 : 1;

    return function (alice, bob) {
        if (alice > bob)
            return factor;

        if (bob > alice)
            return -factor;

        return 0;
    };
};


/*
    Returns a compare function for systems.
*/
function compareSystems (desc, byId) {
    if (byId)
        return function (alice, bob) {
            return compareValues(desc)(alice.id, bob.id);
        };

    return function (alice, bob) {
        const deploymentA = alice.deployment;
        const deploymentB = bob.deployment;
        const nullComp = compareNullable(deploymentA, deploymentB);

        if (nullComp != null)
            return nullComp;

        return compareValues(desc)(
            addressToString(deploymentA.address),
            addressToString(deploymentB.address)
        );
    };
}


/*
    Returns a compare function for deployments.
*/
function compareDeployments (desc, byId) {
    if (byId)
        return function (alice, bob) {
            return compareValues(desc)(alice.id, bob.id);
        };

    return function (alice, bob) {
        return compareValues(desc)(
            addressToString(alice.address),
            addressToString(bob.address)
        );
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
