/* migration

git checkout 11.0
./odoo-bin --addons-path=addons,../sgimmo -d sgimmo13 -u base */

/* 10 -> 11 */
update res_country set name='kosovo_old' where name like '%Kos%';
delete from ir_model_data where name = 'report_ir_model_overview';
delete from ir_model_data where name = 'ir_module_reference_print';
delete from ir_model_data where name like '%action_print_immeuble%';
delete from ir_model_data where name like '%facture_print%';
delete from ir_model_data where name like '%letter_print%';
delete from ir_model_data where name like '%avis_print%';
delete from ir_ui_view where arch_db like '%notify_email%';
delete from ir_model_data where name like '%reunion_print%';
delete from ir_ui_view where name = 'report.external_layout_header';

/* 
git checkout 12.0
./odoo-bin --addons-path=addons,../sgimmo -d sgimmo13 -u base */
/* 11 -> 12 */
delete from ir_translation;
delete from ir_cron;
update res_users set login='michael' where id=1;
update res_users set login = 'old_portaltemplate' where login like 'portaltemplate';
