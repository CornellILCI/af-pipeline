--liquibase formatted sql

--changeset postgres:update_db_documentation context:template splitStatements:false rollbackSplitStatements:false
--comment: DB-690 Update database documentation



DO LANGUAGE PLPGSQL $$
BEGIN
  EXECUTE FORMAT('COMMENT ON DATABASE %I IS %L', current_database(), 'Analythical Framework Database, Contains analysis, Results, Models, Predictions.');
END;
$$;

COMMENT ON SCHEMA af IS 'Analythical Framework';

COMMENT ON TABLE af.analysis
	IS 'A compartment of an analysis request. One analysis request can have more than one analysis (Usually it is 1 request : 1 analysis).'
;

COMMENT ON TABLE af.fitted_values
	IS 'An analysis result table. Stores the fitted values estimations from an analysis job.'
;

COMMENT ON TABLE af.job_data
	IS 'An analysis result table. Register the data that were used for each particular job.'
;

COMMENT ON TABLE af.model_stat
	IS 'An analysis result table. Stores the results and statistics of the model from an analysis job.'
;

COMMENT ON TABLE af.prediction_effect
	IS 'An analysis result table. Stores the predictions and effects estimations from an analysis job.'
;

COMMENT ON TABLE af.residual_outlier
	IS 'An analysis result table. Stores the predictions and effects estimations from an analysis job.'
;

COMMENT ON TABLE af.task
	IS 'Register the actions (tasks) of the analytical pipeline. A request triggers a sequence of tasks.'
;

COMMENT ON TABLE af.variance
	IS 'An analysis result table. Stores the variance components from analysis jobs'
;

COMMENT ON COLUMN af.analysis.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.analysis.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.analysis.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.analysis.is_void
	IS 'Indicator whether the record is deleted (true) or not (false).'
;

COMMENT ON COLUMN af.analysis.model_id
	IS 'Reference to the Model id related to the analysis.'
;

COMMENT ON COLUMN af.analysis.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.analysis.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.analysis.request_id
	IS 'Reference to the request related to the analysis.'
;

COMMENT ON COLUMN af.analysis.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.fitted_values.additional_info
	IS 'Additional information that may be generated about the fitted value. Usually some statistics regarding outliers.'
;

COMMENT ON COLUMN af.fitted_values.hat
	IS 'Diagonal Element of the Hat matrix.'
;

COMMENT ON COLUMN af.fitted_values.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.fitted_values.plot_id
	IS 'Reference to the plot_id. Particular place where the entry is planted.'
;

COMMENT ON COLUMN af.fitted_values.record
	IS 'The number that identifies the data point in the analysis input data (csv).'
;

COMMENT ON COLUMN af.fitted_values.residual
	IS 'Residual associated to the observation in the linear model.'
;

COMMENT ON COLUMN af.fitted_values.stat_factor
	IS 'Reference to the statistical factor.'
;

COMMENT ON COLUMN af.fitted_values.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.fitted_values.trait_value
	IS 'The original data (observation collected).'
;

COMMENT ON COLUMN af.fitted_values.yhat
	IS 'Fitted value for the observation.'
;

COMMENT ON COLUMN af.job.analysis_id
	IS 'Reference to the analysis.'
;

COMMENT ON COLUMN af.job.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.job.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.job.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.job.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.job.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.job.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.job.tenant_id
	IS 'Id of the selected Tenant'
;

COMMENT ON COLUMN af.job_data.data
	IS 'Reference for the data value (Experiment, Occurrence, Trait).'
;

COMMENT ON COLUMN af.job_data.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.job_data.job_id
	IS 'Reference to the job.'
;

COMMENT ON COLUMN af.job_data.value
	IS 'IDs of the data the job is analyzing.'
;

COMMENT ON COLUMN af.model_stat.aic
	IS 'Akaike Information Criterion.'
;

COMMENT ON COLUMN af.model_stat.bic
	IS 'Bayesian Information Criterion.'
;

COMMENT ON COLUMN af.model_stat.components
	IS 'Number of components (variance parameters) associated to the model.'
;

COMMENT ON COLUMN af.model_stat.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.model_stat.job_id
	IS 'Reference to the Job.'
;

COMMENT ON COLUMN af.model_stat.log_lik
	IS 'Log-likelihood of the last iteration.'
;

COMMENT ON COLUMN af.prediction_effect.additional_info
	IS 'Additional information that may be generated about the effects. Usually some statistics regarding the effect outliers.'
;

COMMENT ON COLUMN af.prediction_effect.e_code
	IS 'Code of the predicted value. E means "Estimable", * not estimable'
;

COMMENT ON COLUMN af.prediction_effect.effect
	IS 'Estimated effect of each level factor.'
;

COMMENT ON COLUMN af.prediction_effect.factor
	IS 'Statistical factor and its level that the predicted value and effects are for.'
;

COMMENT ON COLUMN af.prediction_effect.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.prediction_effect.job_id
	IS 'Reference to the Job.'
;

COMMENT ON COLUMN af.prediction_effect.se_effect
	IS 'Standard error associated to the estimated effect'
;

COMMENT ON COLUMN af.prediction_effect.std_error
	IS 'Standard error associated to the predicted value.'
;

COMMENT ON COLUMN af.prediction_effect.tenant_id
	IS 'Id of the selected Tenant'
;

COMMENT ON COLUMN af.prediction_effect.value
	IS 'Predicted value of the given factor and level.'
;

COMMENT ON COLUMN af.property.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.property.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.property.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.property.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.property.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.property.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.property.statement
	IS ''
;

COMMENT ON COLUMN af.property.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.property_acl.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.property_acl.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.property_acl.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.property_acl.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.property_acl.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.property_acl.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.property_acl.property_id
	IS 'Reference to the property.'
;

COMMENT ON COLUMN af.property_acl.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.property_config.config_property_id
	IS 'Reference to the property that will help to filter.'
;

COMMENT ON COLUMN af.property_config.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.property_config.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.property_config.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.property_config.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.property_config.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.property_config.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.property_config.property_id
	IS 'Reference to the property'
;

COMMENT ON COLUMN af.property_config.property_ui_id
	IS 'Reference to the property ui id that will link the type of configuration in the user interface.'
;

COMMENT ON COLUMN af.property_config.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.property_meta.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.property_meta.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.property_meta.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.property_meta.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.property_meta.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.property_meta.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.property_meta.property_id
	IS 'Reference to the property.'
;

COMMENT ON COLUMN af.property_meta.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.property_rule.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.property_rule.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.property_rule.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.property_rule.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.property_rule.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.property_rule.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.property_rule.property_config_id
	IS 'Reference to the property config.'
;

COMMENT ON COLUMN af.property_rule.property_id
	IS 'Reference to the property.'
;

COMMENT ON COLUMN af.property_rule.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.property_ui.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.property_ui.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.property_ui.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.property_ui.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.property_ui.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.property_ui.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.property_ui.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.request.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.request.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.request.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.request.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.request.method_id
	IS 'Reference to the Property table that contains the method.'
;

COMMENT ON COLUMN af.request.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.request.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.request.msg
	IS 'Specific message for the request.'
;

COMMENT ON COLUMN af.request.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.request_entry.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.request_entry.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.request_entry.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.request_entry.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.request_entry.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.request_entry.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.request_entry.request_id
	IS 'Reference to the Request related.'
;

COMMENT ON COLUMN af.request_entry.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.request_parameter.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.request_parameter.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.request_parameter.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.request_parameter.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.request_parameter.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.request_parameter.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.request_parameter.property_id
	IS 'Reference the property related to the request.'
;

COMMENT ON COLUMN af.request_parameter.request_id
	IS 'Reference to the Request.'
;

COMMENT ON COLUMN af.request_parameter.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.residual_outlier.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.residual_outlier.job_id
	IS 'Reference to the job.'
;

COMMENT ON COLUMN af.residual_outlier.outlier
	IS 'List of the outliers (Key value pairs)'
;

COMMENT ON COLUMN af.residual_outlier.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.task.creation_timestamp
	IS 'Timestamp when the record was added to the table'
;

COMMENT ON COLUMN af.task.creator_id
	IS 'ID of the user who added the record to the table'
;

COMMENT ON COLUMN af.task.err_msg
	IS 'Error message if exists.'
;

COMMENT ON COLUMN af.task.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.task.is_void
	IS 'Indicator whether the record is deleted (true) or not (false)'
;

COMMENT ON COLUMN af.task.modification_timestamp
	IS 'Timestamp when the record was last modified'
;

COMMENT ON COLUMN af.task.modifier_id
	IS 'ID of the user who last modified the record'
;

COMMENT ON COLUMN af.task.name
	IS 'Name of the task.'
;

COMMENT ON COLUMN af.task.parent_id
	IS 'Recursive relation to identify if a task has a parent task.'
;

COMMENT ON COLUMN af.task.processor
	IS 'Type of processor used in the task.'
;

COMMENT ON COLUMN af.task.request_id
	IS 'Reference to the Request related to the task.'
;

COMMENT ON COLUMN af.task.status
	IS 'Current status of the task. In process, Started, Finished.'
;

COMMENT ON COLUMN af.task.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

COMMENT ON COLUMN af.task.time_end
	IS 'Time when the task was finished.'
;

COMMENT ON COLUMN af.task.time_start
	IS 'Time when the task was started.'
;

COMMENT ON COLUMN af.variance.code
	IS 'Code of the estimation status.'
;

COMMENT ON COLUMN af.variance.component
	IS 'Quantity of parameters (components) that were estimated.'
;

COMMENT ON COLUMN af.variance.component_ratio
	IS 'Ratio of the component relative to the square root of the diagonal element of the inverse of the average information matrix.'
;

COMMENT ON COLUMN af.variance.gamma
	IS 'Reports the actual parameter fitted.'
;

COMMENT ON COLUMN af.variance.id
	IS 'Unique identifier of the record within the table.'
;

COMMENT ON COLUMN af.variance.job_id
	IS 'Reference to the Job associated to this variance results.'
;

COMMENT ON COLUMN af.variance.last_change_percentage
	IS 'The percentage change in the parameter at the last iteration.'
;

COMMENT ON COLUMN af.variance.model
	IS 'How the component was modeled.'
;

COMMENT ON COLUMN af.variance.source
	IS 'Model term (component) associated to the variance.'
;

COMMENT ON COLUMN af.variance.tenant_id
	IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.'
;

--Revert Changes

--rollback COMMENT ON SCHEMA af IS 'Analythical Framework';

--rollback COMMENT ON TABLE af.analysis IS 'A compartment of an analysis request. One analysis request can have more than one analysis (Usually it is 1 request : 1 analysis).';
--rollback COMMENT ON TABLE af.fitted_values IS 'An analysis result table. Stores the fitted values estimations from an analysis job.';
--rollback COMMENT ON TABLE af.job_data IS 'An analysis result table. Register the data that were used for each particular job.';
--rollback COMMENT ON TABLE af.model_stat IS 'An analysis result table. Stores the results and statistics of the model from an analysis job.';
--rollback COMMENT ON TABLE af.prediction_effect IS 'An analysis result table. Stores the predictions and effects estimations from an analysis job.';
--rollback COMMENT ON TABLE af.residual_outlier IS 'An analysis result table. Stores the predictions and effects estimations from an analysis job.';
--rollback COMMENT ON TABLE af.task IS 'Register the actions (tasks) of the analytical pipeline. A request triggers a sequence of tasks.';
--rollback COMMENT ON TABLE af.variance IS 'An analysis result table. Stores the variance components from analysis jobs';

--rollback COMMENT ON COLUMN af.analysis.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.analysis.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.analysis.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.analysis.is_void IS 'Indicator whether the record is deleted (true) or not (false).';
--rollback COMMENT ON COLUMN af.analysis.model_id IS 'Reference to the Model id related to the analysis.';
--rollback COMMENT ON COLUMN af.analysis.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.analysis.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.analysis.request_id IS 'Reference to the request related to the analysis.';
--rollback COMMENT ON COLUMN af.analysis.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.fitted_values.additional_info IS 'Additional information that may be generated about the fitted value. Usually some statistics regarding outliers.';
--rollback COMMENT ON COLUMN af.fitted_values.hat IS 'Diagonal Element of the Hat matrix.';
--rollback COMMENT ON COLUMN af.fitted_values.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.fitted_values.plot_id IS 'Reference to the plot_id. Particular place where the entry is planted.';
--rollback COMMENT ON COLUMN af.fitted_values.record IS 'The number that identifies the data point in the analysis input data (csv).';
--rollback COMMENT ON COLUMN af.fitted_values.residual IS 'Residual associated to the observation in the linear model.';
--rollback COMMENT ON COLUMN af.fitted_values.stat_factor IS 'Reference to the statistical factor.';
--rollback COMMENT ON COLUMN af.fitted_values.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.fitted_values.trait_value IS 'The original data (observation collected).';
--rollback COMMENT ON COLUMN af.fitted_values.yhat IS 'Fitted value for the observation.';
--rollback COMMENT ON COLUMN af.job.analysis_id IS 'Reference to the analysis.';
--rollback COMMENT ON COLUMN af.job.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.job.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.job.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.job.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.job.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.job.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.job.tenant_id IS 'Id of the selected Tenant';
--rollback COMMENT ON COLUMN af.job_data.data IS 'Reference for the data value (Experiment, Occurrence, Trait).';
--rollback COMMENT ON COLUMN af.job_data.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.job_data.job_id IS 'Reference to the job.';
--rollback COMMENT ON COLUMN af.job_data.value IS 'IDs of the data the job is analyzing.';
--rollback COMMENT ON COLUMN af.model_stat.aic IS 'Akaike Information Criterion.';
--rollback COMMENT ON COLUMN af.model_stat.bic IS 'Bayesian Information Criterion.';
--rollback COMMENT ON COLUMN af.model_stat.components IS 'Number of components (variance parameters) associated to the model.';
--rollback COMMENT ON COLUMN af.model_stat.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.model_stat.job_id  IS 'Reference to the Job.';
--rollback COMMENT ON COLUMN af.model_stat.log_lik IS 'Log-likelihood of the last iteration.';
--rollback COMMENT ON COLUMN af.prediction_effect.additional_info IS 'Additional information that may be generated about the effects. Usually some statistics regarding the effect outliers.';
--rollback COMMENT ON COLUMN af.prediction_effect.e_code IS 'Code of the predicted value. E means "Estimable", * not estimable';
--rollback COMMENT ON COLUMN af.prediction_effect.effect IS 'Estimated effect of each level factor.';
--rollback COMMENT ON COLUMN af.prediction_effect.factor IS 'Statistical factor and its level that the predicted value and effects are for.';
--rollback COMMENT ON COLUMN af.prediction_effect.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.prediction_effect.job_id IS 'Reference to the Job.';
--rollback COMMENT ON COLUMN af.prediction_effect.se_effect IS 'Standard error associated to the estimated effect';
--rollback COMMENT ON COLUMN af.prediction_effect.std_error IS 'Standard error associated to the predicted value.';
--rollback COMMENT ON COLUMN af.prediction_effect.tenant_id IS 'Id of the selected Tenant';
--rollback COMMENT ON COLUMN af.prediction_effect.value IS 'Predicted value of the given factor and level.';
--rollback COMMENT ON COLUMN af.property.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.property.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.property.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.property.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.property.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.property.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.property.statement IS 'A command, instruction, piece of code, etc., associated to the property';
--rollback COMMENT ON COLUMN af.property.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.property_acl.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.property_acl.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.property_acl.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.property_acl.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.property_acl.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.property_acl.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.property_acl.property_id IS 'Reference to the property.';
--rollback COMMENT ON COLUMN af.property_acl.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.property_config.config_property_id IS 'Reference to the property that will help to filter.';
--rollback COMMENT ON COLUMN af.property_config.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.property_config.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.property_config.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.property_config.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.property_config.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.property_config.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.property_config.property_id IS 'Reference to the property' ;
--rollback COMMENT ON COLUMN af.property_config.property_ui_id IS 'Reference to the property ui id that will link the type of configuration in the user interface.';
--rollback COMMENT ON COLUMN af.property_config.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.property_meta.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.property_meta.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.property_meta.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.property_meta.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.property_meta.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.property_meta.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.property_meta.property_id IS 'Reference to the property.';
--rollback COMMENT ON COLUMN af.property_meta.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.property_rule.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.property_rule.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.property_rule.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.property_rule.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.property_rule.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.property_rule.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.property_rule.property_config_id IS 'Reference to the property config.';
--rollback COMMENT ON COLUMN af.property_rule.property_id IS 'Reference to the property.';
--rollback COMMENT ON COLUMN af.property_rule.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.property_ui.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.property_ui.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.property_ui.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.property_ui.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.property_ui.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.property_ui.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.property_ui.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.request.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.request.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.request.id IS 'Unique identifier of the record within the table.' ;
--rollback COMMENT ON COLUMN af.request.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.request.method_id IS 'Reference to the Property table that contains the method.';
--rollback COMMENT ON COLUMN af.request.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.request.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.request.msg IS 'Specific message for the request.';
--rollback COMMENT ON COLUMN af.request.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.request_entry.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.request_entry.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.request_entry.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.request_entry.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.request_entry.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.request_entry.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.request_entry.request_id IS 'Reference to the Request related.';
--rollback COMMENT ON COLUMN af.request_entry.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.request_parameter.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.request_parameter.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.request_parameter.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.request_parameter.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.request_parameter.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.request_parameter.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.request_parameter.property_id IS 'Reference the property related to the request.';
--rollback COMMENT ON COLUMN af.request_parameter.request_id IS 'Reference to the Request.';
--rollback COMMENT ON COLUMN af.request_parameter.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.residual_outlier.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.residual_outlier.job_id IS 'Reference to the job.';
--rollback COMMENT ON COLUMN af.residual_outlier.outlier IS 'List of the outliers (Key value pairs)';
--rollback COMMENT ON COLUMN af.residual_outlier.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.task.creation_timestamp IS 'Timestamp when the record was added to the table';
--rollback COMMENT ON COLUMN af.task.creator_id IS 'ID of the user who added the record to the table';
--rollback COMMENT ON COLUMN af.task.err_msg IS 'Error message if exists.';
--rollback COMMENT ON COLUMN af.task.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.task.is_void IS 'Indicator whether the record is deleted (true) or not (false)';
--rollback COMMENT ON COLUMN af.task.modification_timestamp IS 'Timestamp when the record was last modified';
--rollback COMMENT ON COLUMN af.task.modifier_id IS 'ID of the user who last modified the record';
--rollback COMMENT ON COLUMN af.task.name IS 'Name of the task.';
--rollback COMMENT ON COLUMN af.task.parent_id IS 'Recursive relation to identify if a task has a parent task.';
--rollback COMMENT ON COLUMN af.task.processor IS 'Type of processor used in the task.';
--rollback COMMENT ON COLUMN af.task.request_id IS 'Reference to the Request related to the task.';
--rollback COMMENT ON COLUMN af.task.status IS 'Current status of the task. In process, Started, Finished.';
--rollback COMMENT ON COLUMN af.task.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
--rollback COMMENT ON COLUMN af.task.time_end IS 'Time when the task was finished.';
--rollback COMMENT ON COLUMN af.task.time_start IS 'Time when the task was started.';
--rollback COMMENT ON COLUMN af.variance.code IS 'Code of the estimation status.';
--rollback COMMENT ON COLUMN af.variance.component IS 'Quantity of parameters (components) that were estimated.';
--rollback COMMENT ON COLUMN af.variance.component_ratio IS 'Ratio of the component relative to the square root of the diagonal element of the inverse of the average information matrix.';
--rollback COMMENT ON COLUMN af.variance.gamma IS 'Reports the actual parameter fitted.';
--rollback COMMENT ON COLUMN af.variance.id IS 'Unique identifier of the record within the table.';
--rollback COMMENT ON COLUMN af.variance.job_id IS 'Reference to the Job associated to this variance results.';
--rollback COMMENT ON COLUMN af.variance.last_change_percentage IS 'The percentage change in the parameter at the last iteration.';
--rollback COMMENT ON COLUMN af.variance.model IS 'How the component was modeled.';
--rollback COMMENT ON COLUMN af.variance.source IS 'Model term (component) associated to the variance.';
--rollback COMMENT ON COLUMN af.variance.tenant_id IS 'Id reference to the Tenant table. Indicates the selected Tenant in the system.';
