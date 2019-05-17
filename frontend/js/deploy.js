/*
    deploy.js - Terminal Manager systems deployment.

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
    Deploys a system.
*/
termgr.deploy = function (system, deployment, exclusive = false) {
    const payload = {
        system: system,
        deployment: deployment,
        exclusive: exclusive
    };
    const data = JSON.stringify(payload);
    const headers = {'Content-Type': 'application/json'};
    return termgr.makeRequest('POST', termgr.BASE_URL + '/administer/deploy', data, headers).then(
        function () {
            alert('Das System wurde als verbaut gekennzeichnet.');
        },
        termgr.checkSession('Das System konnte nicht als verbaut gekennzeichnet werden.')
    );
};


/*
    Reloads the systems.
*/
function reload () {
    termgr.startLoading();
    return termgr.getDeployments().then(filter).then(showDetails).then(termgr.stopLoading);
}


/*
    Filters, sorts and renders systems.
*/
function filter (deployments) {
    if (deployments == null) {
        termgr.startLoading();
        deployments = termgr.loadDeployments();
    }

    deployments = termgr.filteredDeployments(deployments);
    deployments = termgr.sortedDeployments(deployments);
    termgr.renderDeployments(deployments);
    showDetails();
    termgr.stopLoading();
}


/*
    Deploys a system.
*/
function deploy (system) {
    const deployment = document.getElementById('deployments').value;
    const exclusive = document.getElementById('exclusive').checked;
    termgr.deploy(system, deployment, exclusive);
}


/*
    Shows details of the respective deployment.
*/
function showDetails () {
    const deployments = termgr.loadDeployments();
    const deploymentId = parseInt(document.getElementById('deployments').value);
    let deployment;

    for (deployment of deployments) {
        if (deployment.id == deploymentId) {
            break;
        }
    }

    const deploymentDetails = document.getElementById('deploymentDetails');
    const table = termgr.deploymentToTable(deployment);
    deploymentDetails.innerHTML = '';
    deploymentDetails.appendChild(table);
}


/*
    Initialize manage.html.
*/
function init () {
    termgr.startLoading();
    const system = JSON.parse(localStorage.getItem('termgr.system'));
    const deployments = termgr.loadDeployments();

    if (deployments == null) {
        reload().then(termgr.stopLoading);
    } else {
        filter(deployments);
    }

    const btnFilter = document.getElementById('filter');
    btnFilter.addEventListener('click', termgr.partial(filter), false);
    const btnReload = document.getElementById('reload');
    btnReload.addEventListener('click', termgr.partial(reload), false);
    const radioButtons = [
        document.getElementById('sortAsc'),
        document.getElementById('sortDesc'),
        document.getElementById('sortById'),
        document.getElementById('sortByAddress')
    ];

    for (const radioButton of radioButtons) {
        radioButton.addEventListener('change', termgr.partial(filter), false);
    }

    const btnDeploy = document.getElementById('deploy');
    btnDeploy.addEventListener('click', termgr.partial(deploy, system), false);
    const deploymentsList = document.getElementById('deployments');
    deploymentsList.addEventListener('change', termgr.partial(showDetails), false);
    const systemId = document.getElementById('system');
    systemId.textContent = system;
}


document.addEventListener('DOMContentLoaded', init);
