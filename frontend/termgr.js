/*
  termgr.js - Terminal Manager front end JavaScript library.

  (C) 2018 HOMEINFO - Digitale Informationssysteme GmbH

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

  Requires:
    * jquery.js
    * sweetalert.js
*/
"use strict";

termgr = termgr || {};

termgr.Terminal = function(json) {
  for (var prop in json) {
    if (json.hasOwnProperty(prop)) {
        this[prop] = json[prop];
    }
  }

  this.getId = function() {
    return this.tid + '.' + this.customer.cid;
  }
}

termgr.TerminalEntry = function(terminal) {

}
