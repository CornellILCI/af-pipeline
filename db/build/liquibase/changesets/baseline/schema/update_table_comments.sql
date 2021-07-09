-- Deploy analyticalframework: to pg

--liquibase formatted sql

--changeset postgres:update_table_comments context:schema splitStatements:false rollbackSplitStatements:false
--comment: update_table_comments



ALTER TABLE af.analysis 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.analysis 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.job 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.job 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.property 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.property 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.property_acl 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.property_acl 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.property_config 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.property_config 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.property_meta 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.property_meta 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.property_rule 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.property_rule 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.property_ui 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.property_ui 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.request 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.request 
 ALTER COLUMN is_void SET DEFAULT false;

ALTER TABLE af.request_entry 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.request_parameter 
 ALTER COLUMN creation_timestamp SET DEFAULT now();

ALTER TABLE af.request_parameter 
 ALTER COLUMN is_void SET DEFAULT false;

COMMENT ON TABLE af.job
	IS 'Work unit for computation in the analysis. One analysis can have more than one job'
;

COMMENT ON TABLE af.property
	IS 'Single element of configuration for an analysis or a design (e.g. model, prediction, error, etc)'
;

COMMENT ON TABLE af.property_acl
	IS 'Access Control List'
;

COMMENT ON TABLE af.property_config
	IS 'Provides context to use the properties (e.g. defines the required properties for a design, defines the elements of a catalogs or the output elements of a request)'
;

COMMENT ON TABLE af.property_meta
	IS 'Stores additional information of a property'
;

COMMENT ON TABLE af.property_rule
	IS 'Defines custom validation rules for a property value (e.g. defines if a property is required based on the value of another property) The property rule is associated to the property_config.'
;

COMMENT ON TABLE af.property_ui
	IS 'Defines the behavior of a user interface component when its associated to a property'
;

COMMENT ON TABLE af.request
	IS 'Stores the requests to execute a function of the analytical framework.'
;

COMMENT ON TABLE af.request_entry
	IS 'Entries of a request'
;

COMMENT ON TABLE af.request_parameter
	IS 'Parameter of the request that are provided to the AEO (Analysis Execute Object).'
;

COMMENT ON COLUMN af.analysis.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.analysis.creator_id
	IS ''
;

COMMENT ON COLUMN af.analysis.description
	IS 'Description of the analysis'
;

COMMENT ON COLUMN af.analysis.is_void
	IS ''
;

COMMENT ON COLUMN af.analysis.name
	IS 'Name of the analysis'
;

COMMENT ON COLUMN af.analysis.prediction_id
	IS 'Id of the type of the prediction used in the analysis (Property table)'
;

COMMENT ON COLUMN af.analysis.status
	IS 'Status of the analysis ()'
;

COMMENT ON COLUMN af.analysis.tenant_id
	IS ''
;

COMMENT ON COLUMN af.job.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.job.creator_id
	IS ''
;

COMMENT ON COLUMN af.job.is_void
	IS ''
;

COMMENT ON COLUMN af.job.name
	IS 'Name of the job'
;

COMMENT ON COLUMN af.job.output_path
	IS 'Path where the results of the job are saved.'
;

COMMENT ON COLUMN af.job.size
	IS 'Size'
;

COMMENT ON COLUMN af.job.status
	IS 'Status of the job'
;

COMMENT ON COLUMN af.job.status_message
	IS 'Message delivered to the client about the status.'
;

COMMENT ON COLUMN af.job.tenant_id
	IS ''
;

COMMENT ON COLUMN af.job.time_end
	IS 'Timestamp when the job was finalized.'
;

COMMENT ON COLUMN af.job.time_start
	IS 'Timestamp when the job was initiated.'
;

COMMENT ON COLUMN af.property.code
	IS 'Identifier of the property within its context, the context is found in the property_config table'
;

COMMENT ON COLUMN af.property.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.property.creator_id
	IS ''
;

COMMENT ON COLUMN af.property.data_type
	IS 'Data type of the property (e.g. csv, character varying, integer, etc.)'
;

COMMENT ON COLUMN af.property.description
	IS 'Detail of the purpose/function of a property.'
;

COMMENT ON COLUMN af.property.is_void
	IS ''
;

COMMENT ON COLUMN af.property.label
	IS 'Label displayed to the client'
;

COMMENT ON COLUMN af.property.name
	IS 'Name of the property'
;

COMMENT ON COLUMN af.property.tenant_id
	IS ''
;

COMMENT ON COLUMN af.property.type
	IS 'Classifier of properties within it s context (e.g. catalog_item, catalog_root)'
;

COMMENT ON COLUMN af.property_acl.breeding_program_id
	IS 'Breeding program with access to the property.'
;

COMMENT ON COLUMN af.property_acl.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.property_acl.creator_id
	IS ''
;

COMMENT ON COLUMN af.property_acl.is_void
	IS ''
;

COMMENT ON COLUMN af.property_acl.phase_id
	IS 'Identifier of the phase with access to a certain property.'
;

COMMENT ON COLUMN af.property_acl.property_item_id
	IS 'identifier of the property to be filtered.'
;

COMMENT ON COLUMN af.property_acl.tenant_id
	IS ''
;

COMMENT ON COLUMN af.property_config.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.property_config.creator_id
	IS ''
;

COMMENT ON COLUMN af.property_config.is_layout_variable
	IS 'Specifies if a property is required to generate a layout in randomizations.'
;

COMMENT ON COLUMN af.property_config.is_required
	IS 'Specify in the property is a required parameter for a design.'
;

COMMENT ON COLUMN af.property_config.is_void
	IS ''
;

COMMENT ON COLUMN af.property_config.order_number
	IS 'Defines an arbitrary order for configuration properties.'
;

COMMENT ON COLUMN af.property_config.tenant_id
	IS ''
;

COMMENT ON COLUMN af.property_meta.code
	IS 'Code of the property'
;

COMMENT ON COLUMN af.property_meta.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.property_meta.creator_id
	IS ''
;

COMMENT ON COLUMN af.property_meta.is_void
	IS ''
;

COMMENT ON COLUMN af.property_meta.tenant_id
	IS ''
;

COMMENT ON COLUMN af.property_meta.value
	IS 'Value of the property metadata'
;

COMMENT ON COLUMN af.property_rule.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.property_rule.creator_id
	IS ''
;

COMMENT ON COLUMN af.property_rule.expression
	IS 'Definition of the rule to be applied.'
;

COMMENT ON COLUMN af.property_rule."group"
	IS 'Allows to group several rules as a singular composite rule.'
;

COMMENT ON COLUMN af.property_rule.is_void
	IS ''
;

COMMENT ON COLUMN af.property_rule.tenant_id
	IS ''
;

COMMENT ON COLUMN af.property_rule.type
	IS 'Classifier of the rule (e.g. required if, allow value, etc.)'
;

COMMENT ON COLUMN af.property_ui.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.property_ui.creator_id
	IS ''
;

COMMENT ON COLUMN af.property_ui."default"
	IS 'Default value of a property.'
;

COMMENT ON COLUMN af.property_ui.is_catalogue
	IS 'Defines if the property is displayed in the user interface as a select list.'
;

COMMENT ON COLUMN af.property_ui.is_disabled
	IS 'Defines if the property is disabled fro the user.'
;

COMMENT ON COLUMN af.property_ui.is_multiple
	IS 'Defines if the property has more than one value (e.g define multiple error values for a single request)'
;

COMMENT ON COLUMN af.property_ui.is_visible
	IS 'Set the property visible/invisible in the interface'
;

COMMENT ON COLUMN af.property_ui.is_void
	IS ''
;

COMMENT ON COLUMN af.property_ui.maximum
	IS 'Maximum value for a numeric property.'
;

COMMENT ON COLUMN af.property_ui.minimum
	IS 'Minimum value for a numeric property'
;

COMMENT ON COLUMN af.property_ui.tenant_id
	IS ''
;

COMMENT ON COLUMN af.property_ui.unit
	IS 'Defines the unit type of numeric properties. '
;

COMMENT ON COLUMN af.request.category
	IS 'Defines if the request is for a randomization or for an analysis.'
;

COMMENT ON COLUMN af.request.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.request.creator_id
	IS ''
;

COMMENT ON COLUMN af.request.crop
	IS 'Crop of the request.'
;

COMMENT ON COLUMN af.request.design
	IS 'Specific design of the request'
;

COMMENT ON COLUMN af.request.engine
	IS 'Version of the R Engine to use in the request.'
;

COMMENT ON COLUMN af.request.institute
	IS 'Name of the Institute where the request is coming from'
;

COMMENT ON COLUMN af.request.is_void
	IS ''
;

COMMENT ON COLUMN af.request.program
	IS 'Program of the request'
;

COMMENT ON COLUMN af.request.requestor_id
	IS 'Identifier of the person that made the request.'
;

COMMENT ON COLUMN af.request.status
	IS 'Status of the request, it can be New, Processed and Expired.'
;

COMMENT ON COLUMN af.request.tenant_id
	IS ''
;

COMMENT ON COLUMN af.request.type
	IS 'Subcategory of the request (e.g. trial design)'
;

COMMENT ON COLUMN af.request.uuid
	IS 'Universal Unique Identifier for the request.'
;

COMMENT ON COLUMN af.request_entry.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.request_entry.creator_id
	IS ''
;

COMMENT ON COLUMN af.request_entry.entry_id
	IS 'Entry_ids coming from b4r to be used in the analysis.'
;

COMMENT ON COLUMN af.request_entry.entry_number
	IS 'Entry number coming from b4r.'
;

COMMENT ON COLUMN af.request_entry.experiment_id
	IS 'Experiment id associated to the entries'
;

COMMENT ON COLUMN af.request_entry.tenant_id
	IS ''
;

COMMENT ON COLUMN af.request_parameter.creation_timestamp
	IS ''
;

COMMENT ON COLUMN af.request_parameter.creator_id
	IS ''
;

COMMENT ON COLUMN af.request_parameter.is_void
	IS ''
;

COMMENT ON COLUMN af.request_parameter.tenant_id
	IS ''
;

COMMENT ON COLUMN af.request_parameter.value
	IS ''
;