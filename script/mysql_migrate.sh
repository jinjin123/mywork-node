cd /app
taboc='order_complain
order_detail
order_discount
order_master
order_meal_detail
order_address
order_marketing_costs'
taberp='hr_attendance
erp_purchase_order
erp_purchase_order_line
field_data_field_product_type
field_data_field_invclasscode
taxonomy_term_data
field_data_field_ordering_inventory_rate
field_data_field_fi_cost_type
field_data_commerce_price
field_data_field_inventory_unit
field_data_field_ordering_unit
field_data_field_spec_text
field_data_field_diff_track
eck_cash_manage
field_data_field_otherincomedate
field_data_field_otherincomemethod
field_data_field_depositreceiveddate
field_data_field_collectionmethod
field_data_field_itemname
field_data_field_otherincomeitem
eck_bundle
field_data_field_depositcustomer
catering_stock
erp_inventory_order_line
erp_inventory_order
hr_jobinfo
hr_wageinfo
eck_product_discard
commerce_product
turnover_estimate
catering_stock_txn
erp_material_group_line
erp_material_group
erp_eodp_status
erp_eodp_pos_status
erp_eodp_pos_records_details
erp_eodp_pos_records
hr_subsidy_fine
hr_personnel_transfer
hr_personnel_changes
hr_otherinfo
hr_monthlyemployeeinfo
hr_jobinfo
hr_dimissioninfo
hr_blacklistinfo
hr_basicinfo
hr_autoid
hr_attendance_raw
hr_attendance_holiday
hr_attendance
hr_agreements_manage
hr_agreementinfo
field_data_field_wagestarget
field_data_field_tcpmh
field_data_field_receiptnum
field_data_field_receiptdate
field_data_field_note
field_data_field_monthly
field_data_field_gas_target
field_data_field_forecast_tc
field_data_field_forecast_s
field_data_field_electricitytarget
field_data_field_discrepancyratetarget
field_data_field_discardedtarget
field_data_field_dietarygoal
field_data_field_depositcheque_date
field_data_field_depositchequebank
field_data_field_depositcheque_account
field_data_field_cuy
field_data_field_cashcommentstarget
field_data_field_budgets
field_data_field_avewagelastmonth
eck_inventory_misc
eck_misc_inventory_config'
tabde='reporting_cache_product
reporting_cache_store
reporting_cache_store_taxonomy
field_data_field_store_state
field_data_field_store_id
commerce_product
field_data_field_product_catetory_basic
taxonomy_term_data'
tabcrm='field_data_field_deposit_no
field_data_field_deposit_store_id
field_data_field_pay_status
field_data_field_deposit_status
field_data_field_deposit_amount
eck_record
field_data_field_deposit_type'
mysql -uroot -pSpark123! -e "stop slave;"
for i in $taboc
do
mysqldump -uroot -pSpark123! -h172.16.103.203 --max_allowed_packet=2048M oc $i > $i.sql
mysql -uroot -pSpark123! oc < $i.sql
done
for i in $taberp
do
mysqldump -uroot -pSpark123! -h172.16.103.203 --max_allowed_packet=2048M erp $i > $i.sql
mysql -uroot -pSpark123! erp < $i.sql
done
for i in $tabde
do
mysqldump -uroot -pSpark123! -h172.16.103.203 --max_allowed_packet=2048M de $i > $i.sql
mysql -uroot -pSpark123! de < $i.sql
done
for i in $tabcrm
do
mysqldump -uroot -pSpark123! -h172.16.103.203 --max_allowed_packet=2048M crm $i > $i.sql
mysql -uroot -pSpark123! crm < $i.sql
done
mysqldump -uroot -pSpark123! -h172.16.103.203 --max_allowed_packet=2048M datacache > datacache.sql
mysql -uroot -pSpark123! datacache < datacache.sql
