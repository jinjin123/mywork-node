#!/bin/bash
de='actions                                                                                                                                                                                   
audit_log   
users_roles                                                                                                                                                                                   
variable                                                                                                                                                                                      
views_data_export                                                                                                                                                                             
views_data_export_object_cache                                                                                                                                                                
views_display                                                                                                                                                                                 
views_view                                                                                                                                                                                    
wysiwyg                                                                                                                                                                                       
wysiwyg_user                                                                                                                                                                                  
zkf_store_select_address_relation                                                                                                                                                             
zkf_store_select_category                                                                                                                                                                     
zkf_store_select_circle_relation                                                                                                                                                              
zkf_store_select_market_relation                                                                                                                                                              
zkf_store_select_store                                                                                                                                                                        
zkf_store_select_tag_relation'                                                                                                                                                                
for i in $de                                                                                                                                                                                  
do                                                                                                                                                                                            
        mysql -uroot -pSpark123! -e "use de; drop table $i;"                                                                                                                                  
done 
