/*
    loader.js - Terminal Manager loading animation.

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
termgr.loader = {};


/*
    Starts loading.
*/
termgr.loader.start = function () {
    const loader = document.getElementById('loader');
    const target = document.getElementById('target');
    target.style.display = 'none';
    loader.style.display = 'block';
};


/*
    Stops loading.
*/
termgr.loader.stop = function () {
    const loader = document.getElementById('loader');
    const target = document.getElementById('target');
    loader.style.display = 'none';
    target.style.display = 'block';
};
