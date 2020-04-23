#!/bin/bash

dropdb sgimmo13
createdb sgimmo13
psql sgimmo13 < /home/odoo/src/sgimmo/dump.sql
psql -d sgimmo13 -c "update ir_module_module set latest_version='13.0.1.0'  where name like 'base';"