/*
    deploy.mjs - Terminal Manager systems deployment.

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

import { deploymentToString } from 'https://javascript.homeinfo.de/hwdb.mjs';
import { Loader, suppressEvent } from 'https://javascript.homeinfo.de/lib.mjs';
import { deploy, getSystem } from './api.mjs';
import { deployments, system } from './cache.mjs';
import { deploymentToTable } from './dom.mjs';
import { autoFilterDeployments } from './filter.mjs';
import { sortDeployments } from './sort.mjs';


/*
    Renders a system.
*/
function renderSystem (system) {
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
}


/*
    Renders the respective deployments.
*/
function render (deployments) {
    return getSystem().then((system) => {
        renderSystem(system);
        return deployments;
    });
};


/*
    Renders a deployment.
*/
function renderDeployment (deployment) {
    const deploymentDetails = document.getElementById('deploymentDetails');
    deploymentDetails.innerHTML = '';
    deploymentDetails.appendChild(deploymentToTable(deployment));
}


/*
    Shows details of the respective deployment.
*/
function renderDetails (deployments) {
    document.getElementById('system').textContent = system.get();
    const deploymentId = parseInt(document.getElementById('deployments').value);

    for (const deployment of deployments)
        if (deployment.id == deploymentId)
            renderDeployment(deployment);

    return deployments;
};


/*
    Updates details of the selected deployment.
*/
function updateDetails () {
    return deployments.get().then(renderDetails);
};


/*
    Filters, sorts and renders deployments.
*/
function list (force = false) {
    return Loader.wrap(
        deployments.get(force).then(
        autoFilterDeployments).then(
        sortDeployments).then(
        render).then(
        renderDetails)
    );
};


/*
    Deploys a system.
*/
function deploySystem () {
    const deployment = document.getElementById('deployments').value;
    const exclusive = document.getElementById('exclusive').checked;
    const fitted = document.getElementById('fitted').checked;
    return deploy(system.get(), deployment, exclusive, fitted);
};


/*
    Initialize the buttons.
*/
function initButtons () {
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
    btnDeploy.addEventListener('click', suppressEvent(deploySystem), false);

    const deploymentsList = document.getElementById('deployments');
    deploymentsList.addEventListener('change', suppressEvent(updateDetails), false);
}


/*
    Initialize deploy.html.
*/
export function init () {
    list();
    initButtons();
}
