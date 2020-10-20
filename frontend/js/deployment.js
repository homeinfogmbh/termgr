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


var termgr = termgr || {};
termgr.deployment = {};


/*
    Renders the respective deployments.
*/
termgr.deployment.render = function (deployments) {
    return termgr.api.getSystem().then(
        function (system) {
            const select = document.getElementById('deployments');
            select.innerHTML = '';

            for (const deployment of deployments) {
                let option = document.createElement('option');
                option.value = '' + deployment.id;
                option.textContent = termgr.deploymentToString(deployment);
                select.appendChild(option);
            }

            if (system.deployment)
                select.value = '' + system.deployment.id;
        }
    );
};


/*
    Shows details of the respective deployment.
*/
termgr.deployment.renderDetails = function () {
    const deployments = termgr.storage.deployments.get();
    const deploymentId = parseInt(document.getElementById('deployments').value);
    let deployment;

    for (deployment of deployments) {
        if (deployment.id == deploymentId)
            break;
    }

    const deploymentDetails = document.getElementById('deploymentDetails');
    const table = termgr.dom.deploymentToTable(deployment);
    deploymentDetails.innerHTML = '';
    deploymentDetails.appendChild(table);
};


/*
    Filters, sorts and renders systems.
*/
termgr.deployment.list = function (deployments) {
    if (deployments == null)
        deployments = termgr.storage.deployments.get();

    deployments = termgr.filter.deployments(deployments);
    deployments = termgr.sort.deployments(deployments);
    return termgr.deployment.render(deployments).then(
        termgr.deployment.renderDetails).then(
        termgr.loader.stop);
};


/*
    Reloads the systems.
*/
termgr.deployment.reload = function () {
    termgr.loader.start();
    return termgr.api.getDeployments().then(termgr.deployment.list);
};


/*
    Deploys a system.
*/
termgr.deployment.deploy = function (system) {
    const deployment = document.getElementById('deployments').value;
    const exclusive = document.getElementById('exclusive').checked;
    const fitted = document.getElementById('fitted').checked;
    return termgr.api.deploy(system, deployment, exclusive, fitted);
};


/*
    Initialize deploy.html.
*/
termgr.deployment.init = function () {
    termgr.loader.start();
    const system = termgr.storage.system.get();
    const deployments = termgr.storage.deployments.get();

    if (deployments == null)
        termgr.deployment.reload();
    else
        termgr.deployment.list(deployments);

    const btnLogout = document.getElementById('logout');
    btnLogout.addEventListener('click', termgr.partial(termgr.api.logout), false);
    const btnFilter = document.getElementById('filter');
    btnFilter.addEventListener('click', termgr.partial(termgr.deployment.list), false);
    const btnReload = document.getElementById('reload');
    btnReload.addEventListener('click', termgr.partial(termgr.deployment.reload), false);
    const radioButtons = [
        document.getElementById('sortAsc'),
        document.getElementById('sortDesc'),
        document.getElementById('sortById'),
        document.getElementById('sortByAddress')
    ];

    for (const radioButton of radioButtons)
        radioButton.addEventListener('change', termgr.partial(termgr.deployment.list), false);

    const btnDeploy = document.getElementById('deploy');
    btnDeploy.addEventListener('click', termgr.partial(termgr.deployment.deploy, system), false);
    const deploymentsList = document.getElementById('deployments');
    deploymentsList.addEventListener('change', termgr.partial(termgr.deployment.renderDetails), false);
    const systemId = document.getElementById('system');
    systemId.textContent = system;
};


document.addEventListener('DOMContentLoaded', termgr.deployment.init);
