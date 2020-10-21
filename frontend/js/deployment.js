/*
    deploy.js - Terminal Manager systems deployment.

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

import { deploymentToString } from 'https://javascript.homeinfo.de/hwdb.js';
import { deploy, getSystem } from './api.js';
import { deployments, system } from './cache.js';
import { deploymentToTable } from './dom.js';
import { autoFilterDeployments } from './filter.js';
import { suppressEvent } from './functions.js';
import * as loader from './loader.js';
import { sortDeployments } from './sort.js';


/*
    Renders the respective deployments.
*/
function render (deployments) {
    return getSystem().then(
        function (system) {
            const select = document.getElementById('deployments');
            select.innerHTML = '';

            for (const deployment of deployments) {
                let option = document.createElement('option');
                option.value = '' + deployment.id;
                option.textContent = deploymentToString(deployment);
                select.appendChild(option);
            }

            if (system.deployment)
                select.value = '' + system.deployment.id;

            return deployments;
        }
    );
};


/*
    Shows details of the respective deployment.
*/
function renderDetails (deployments) {
    const deploymentId = parseInt(document.getElementById('deployments').value);
    let deployment;

    for (deployment of deployments) {
        if (deployment.id == deploymentId)
            break;
    }

    const deploymentDetails = document.getElementById('deploymentDetails');
    const table = deploymentToTable(deployment);
    deploymentDetails.innerHTML = '';
    deploymentDetails.appendChild(table);
    return deployments;
};


/*
    Updates details of the selected deployment.
*/
function updateDetails () {
    return deployments.getValue().then(renderDetails);
};


/*
    Filters, sorts and renders deployments.
*/
function list (force = false) {
    loader.start();
    return deployments.getValue(force).then(
        autoFilterDeployments).then(
        sortDeployments).then(
        render).then(
        renderDetails).then(
        loader.stop
    );
};


/*
    Deploys a system.
*/
function deploySystem (system) {
    const deployment = document.getElementById('deployments').value;
    const exclusive = document.getElementById('exclusive').checked;
    const fitted = document.getElementById('fitted').checked;
    return deploy(system, deployment, exclusive, fitted);
};


/*
    Initialize deploy.html.
*/
export function init () {
    const systemId = system.get();

    const systemIdField = document.getElementById('system');
    systemIdField.textContent = systemId;

    list();

    const btnLogout = document.getElementById('logout');
    btnLogout.addEventListener('click', suppressEvent(logout), false);

    const btnFilter = document.getElementById('filter');
    btnFilter.addEventListener('click', suppressEvent(list), false);

    const btnReload = document.getElementById('reload');
    btnReload.addEventListener('click', suppressEvent(list, true), false);

    const radioButtons = [
        document.getElementById('sortAsc'),
        document.getElementById('sortDesc'),
        document.getElementById('sortById'),
        document.getElementById('sortByAddress')
    ];

    for (const radioButton of radioButtons)
        radioButton.addEventListener('change', suppressEvent(list), false);

    const btnDeploy = document.getElementById('deploy');
    btnDeploy.addEventListener('click', suppressEvent(deploySystem, system), false);

    const deploymentsList = document.getElementById('deployments');
    deploymentsList.addEventListener('change', suppressEvent(updateDetails), false);
}
