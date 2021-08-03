--liquibase formatted sql

--changeset postgres:change_varchar_columns_to_text_columns context:schema splitStatements:false rollbackSplitStatements:false
--comment: BA-578 Chnage columns of type VARCHAR to columns of type TEXT


-- af     | analysis          
-- af     | effect            
-- af     | fitted_values     
-- af     | job               
-- af     | job_data          
-- af     | job_stat_factor   
-- af     | model_stat        
-- af     | prediction        
-- af     | property          
-- af     | property_acl      
-- af     | property_config   
-- af     | property_meta     
-- af     | property_rule     
-- af     | property_ui       
-- af     | request           
-- af     | request_entry     
-- af     | request_parameter 
-- af     | task              
-- af     | variance          

ALTER TABLE af.analysis
    ALTER COLUMN name TYPE text,
    ALTER COLUMN deacription TYPE text,
    ALTER COLUMN status TYPE text,
    ALTER COLUMN creator_id TYPE text,
    ALTER COLUMN modifier_id TYPE text;
