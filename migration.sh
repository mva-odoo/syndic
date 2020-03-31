#!/bin/bash

odoo 11.0
/home/odoo/src/odoo/odoo-bin --addons-path=addons,../sgimmo -d sgimmo13 -u all --stop-after-init
odoo 12.0
/home/odoo/src/odoo/odoo-bin --addons-path=addons,../sgimmo -d sgimmo13 -u all --stop-after-init
odoo 13.0
/home/odoo/src/odoo/odoo-bin --addons-path=addons,../sgimmo -d sgimmo13 -u all --stop-after-init
