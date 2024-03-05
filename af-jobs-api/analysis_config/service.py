import json

from database import Property, PropertyConfig, PropertyMeta, db
from sqlalchemy import and_, func, text

from analysis_config import api_models
from analysis_config import models as db_models
from database import db


def get_analysis_configs(page=0, page_size=1000, **kwargs):

    query_params = {}

    # make sure to add only non null query params
    query_params = {k: [v] for k, v in kwargs.items() if v is not None}

    analysis_config_base_property = Property.query.filter(Property.code == "analysis_config").one()

    # sub query to aggregate metadata code and value
    analysis_configs_sub_q = (
        db.session.query(Property.id, PropertyMeta.code, func.array_agg(PropertyMeta.value).label("meta_value"))
        .select_from(PropertyConfig)
        .join(
            Property,
            and_(
                Property.id == PropertyConfig.config_property_id,
                Property.id != analysis_config_base_property.id,
                PropertyConfig.property_id == analysis_config_base_property.id,
            ),
        )
        .join(PropertyMeta, Property.id == PropertyMeta.property_id)
        .group_by(Property.id, PropertyMeta.code)
        .subquery()
    )

    # query aggregated metadata code and value as json object
    analysis_configs_q = (
        db.session.query(Property)
        .select_from(analysis_configs_sub_q)
        .group_by(analysis_configs_sub_q.c.id, Property)
        .having(
            func.jsonb_object_agg(analysis_configs_sub_q.c.code, analysis_configs_sub_q.c.meta_value).op("@>")(
                json.dumps(query_params)
            )
        )
        .join(Property, Property.id == analysis_configs_sub_q.c.id)
        .order_by(Property.id)
    )

    if page_size is not None:
        analysis_configs_q = analysis_configs_q.limit(page_size)

    if page is not None:
        analysis_configs_q = analysis_configs_q.offset(page * page_size)

    analysis_configs = analysis_configs_q.all()
    total_count = analysis_configs_q.count()

    return analysis_configs, total_count


def submit_analysis_config(request_params: api_models.Analysis,
                           request_params_meta: api_models.AnalysisConfigMeta,
                           request_params_config: api_models.AnalysisConfig):

    """Submits analysis config to pipeline."""

    analysis_uuid = str(uuidlib.uuid4())

    analysis_property = Property(
        code=request_params.code,
        name=request_params.configName,
        label=request_params.label,
        description=request_params.description,
        type=request_params.design,
        data_type=request_params.dataType,
        creator_id=request_params.creatorId,
        modifier_id=request_params.modifierId,
        is_void=request_params.isVoid,
        tenant_id=request_params.tenantId,
        id=request_params.id,
        statement=request_params.statement
    )

    analysis_config_meta = PropertyMeta(
        property_id=request_params_meta.propertyId,
        code=request_params_meta.code,
        value=request_params_meta.value,
        tenant_id=request_params_meta.tenantId

    )

    analysis_config = PropertyConfig(
        order_number=request_params_config.order,
        creator_id=request_params_config.creatorId,
        is_void=request_params_config.is_void,
        property_id=request_params_config.propertyId,
        config_property_id=request_params_config.configPropertyId,
        is_layout_variable=request_params_config.isLayout,
    )


    with db.session.begin():
        # i may need to add multiple analysis config metas,
        db.session.add(analysis_property)
        db.session.add(analysis_config_meta)
        db.session.add(analysis_config)


def create_analysis_config(
    property_code, property_configName, property_label, property_description, property_design, property_data_type, property_creator_id, property_modifier_id, property_tenant_id, property_statement,
    property_meta_version, property_meta_date, property_meta_author, property_meta_email, property_meta_organization_code, property_meta_engine, property_meta_breeding_program_id,
    property_meta_pipeline_id, property_meta_stage_id, property_meta_design, property_meta_trait_level, property_meta_analysis_objective, property_meta_exp_analysis_pattern,
    property_meta_loc_analysis_pattern, property_meta_year_analysis_pattern, property_meta_trait_pattern, fields, options, formulas, residuals, predictions, id = None
):
    try:
        db.session.begin()
            
        #create a property
        property = Property(
            code=property_code,
            name=property_configName,
            label=property_label,
            description=property_description,
            type=property_design,
            data_type=property_data_type,
            creator_id=property_creator_id,
            modifier_id=property_modifier_id,
            is_void=False,
            tenant_id=property_tenant_id,
            statement=property_statement
        )

        if (id is not None):
            property.id = id



        db.session.add(property)
        db.session.commit()
        db.session.refresh(property)
        
        sub_properties = []

        # for every field
        for field in fields:
            # first we make a sub property and add it to the DB
            field_property = Property(
                code=field.stat_factor,
                data_type=field.data_type,
                is_void=False,
            )
            db.session.add(field_property)
            db.session.commit()
            db.session.refresh(field_property)
            # then we get the id for the sub property and add the link (property config) from our first property to it
        
            property_link_to_parent = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=property.id,
                config_property_id=field_property.id,
                is_layout_variable=False,
            )
            
            property_link_to_root = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=159,
                config_property_id=field_property.id,
                is_layout_variable=False,
            )

            db.session.add(property_link_to_parent)
            db.session.add(property_link_to_root)
            db.session.commit()

        # then we also add a property config to the root of field 
        
        # repeat for options
        for option in options:
            # first we make a sub property and add it to the DB
            option_property = Property(
                code="option_opt"+option.id,
                statement=option.options,
                is_void=False,
            )
            db.session.add(option_property)
            db.session.commit()
            db.session.refresh(option_property)
            # then we get the id for the sub property and add the link (property config) from our first property to it
        
            property_link_to_parent = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=property.id,
                config_property_id=option_property.id,
                is_layout_variable=False,
            )
            
            property_link_to_root = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=137,
                config_property_id=option_property.id,
                is_layout_variable=False,
            )

            db.session.add(property_link_to_parent)
            db.session.add(property_link_to_root)
            db.session.commit()

        # repeat for formula
        for formula in formulas:
            # first we make a sub property and add it to the DB
            formula_property = Property(
                name=formula.name,
                label=formula.name,
                # check for description - description=formula.description,
                statement=formula.statement,
                code="formula_opt"+formula.id,
                type="catalog_item",
                is_void=False,
            )
            db.session.add(formula_property)
            db.session.commit()
            db.session.refresh(formula_property)
            # then we get the id for the sub property and add the link (property config) from our first property to it
        
            property_link_to_parent = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=property.id,
                config_property_id=formula_property.id,
                is_layout_variable=False,
            )
            
            property_link_to_root = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=139,
                config_property_id=formula_property.id,
                is_layout_variable=False,
            )

            db.session.add(property_link_to_parent)
            db.session.add(property_link_to_root)
            db.session.commit()

        # repeat for residual
        for residual in residuals:
            # first we make a sub property and add it to the DB
            residual_property = Property(
                name=residual.name,
                label=residual.name,
                # check for description - description=formula.description,
                statement=residual.statement,
                type="catalog_item",
                code="residual_opt"+residual.id,
                is_void=False,
            )
            db.session.add(residual_property)
            db.session.commit()
            db.session.refresh(residual_property)
            # then we get the id for the sub property and add the link (property config) from our first property to it
        
            property_link_to_parent = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=property.id,
                config_property_id=residual_property.id,
                is_layout_variable=False,
            )
            
            property_link_to_root = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=140,
                config_property_id=residual_property.id,
                is_layout_variable=False,
            )

            db.session.add(property_link_to_parent)
            db.session.add(property_link_to_root)
            db.session.commit()

        # repeat for predict
        for prediction in predictions:
            # first we make a sub property and add it to the DB
            prediction_property = Property(
                name=prediction.name,
                # check for description - description=formula.description,
                statement=prediction.statement,
                type="catalog_item",
                code=prediction.name,
                is_void=False,
            )
            db.session.add(prediction_property)
            db.session.commit()
            db.session.refresh(prediction_property)
            # then we get the id for the sub property and add the link (property config) from our first property to it
        
            property_link_to_parent = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=property.id,
                config_property_id=prediction_property.id,
                is_layout_variable=False,
            )
            
            property_link_to_root = PropertyConfig(
                order_number=999,
                is_void=False,
                property_id=5,
                config_property_id=prediction_property.id,
                is_layout_variable=False,
            )

            db.session.add(property_link_to_parent)
            db.session.add(property_link_to_root)
            db.session.commit()
        
        
        property_metas = []


        property_metas.extend([
            PropertyMeta(property_id=property.id, code='Version', value=property_meta_version, tenant_id=1),
            PropertyMeta(property_id=property.id, code='date', value=property_meta_date, tenant_id=1),
            PropertyMeta(property_id=property.id, code='author', value=property_meta_author, tenant_id=1),
            PropertyMeta(property_id=property.id, code='email', value=property_meta_email, tenant_id=1),
            PropertyMeta(property_id=property.id, code='organization_code', value=property_meta_organization_code, tenant_id=1),
            PropertyMeta(property_id=property.id, code='engine', value=property_meta_engine, tenant_id=1),

            PropertyMeta(property_id=property.id, code='breeding_program_id', value=property_meta_breeding_program_id, tenant_id=1),
            PropertyMeta(property_id=property.id, code='pipeline_id', value=property_meta_pipeline_id, tenant_id=1),
            PropertyMeta(property_id=property.id, code='stage_id', value=property_meta_stage_id, tenant_id=1),
            PropertyMeta(property_id=property.id, code='design', value=property_meta_design, tenant_id=1),

            PropertyMeta(property_id=property.id, code='trait_level', value=property_meta_trait_level, tenant_id=1),
            PropertyMeta(property_id=property.id, code='analysis_objective', value=property_meta_analysis_objective, tenant_id=1),
            PropertyMeta(property_id=property.id, code='exp_analysis_pattern', value=property_meta_exp_analysis_pattern, tenant_id=1),
            PropertyMeta(property_id=property.id, code='loc_analysis_pattern', value=property_meta_loc_analysis_pattern, tenant_id=1),
            PropertyMeta(property_id=property.id, code='year_analysis_pattern', value=property_meta_year_analysis_pattern, tenant_id=1),
            PropertyMeta(property_id=property.id, code='trait_pattern', value=property_meta_trait_pattern, tenant_id=1),
        ])

        analysis_config = PropertyConfig(
            order_number=999,
            creator_id=property_creator_id,
            is_void=False,
            property_id=134,
            config_property_id=property.id,
            is_layout_variable=False,
        )

        print(property_metas)

    

        for property_meta in property_metas:
            db.session.add(property_meta)
        db.session.add(analysis_config)
        db.session.commit()

    except exc.IntegrityError:
        db.session.rollback()



    return

def locate_analysis_config(
    property_code, property_configName, property_label, property_description, property_creator_id, property_meta_author, 
    property_meta_email, property_meta_organization_code, property_meta_engine, property_meta_breeding_program_id,
    property_meta_design, property_meta_analysis_objective
):
       
    configSelect = ("select code, name, label, description, type, creation_timestamp, id from af.property where id in ( "+
        "   select pc.config_property_id from af.property_config pc where property_id = 134 "+
        ")")

    if (property_code is not None and property_code != ""):
        configSelect = configSelect+"and code like ('%{}%')".format(property_code)
    
    if (property_configName is not None and property_configName != ""):
        configSelect = configSelect+"and name like ('%{}%')".format(property_configName)

    if (property_label is not None and property_label != ""):
        configSelect = configSelect+"and label like ('%{}%')".format(property_label)

    if (property_description is not None and property_description != ""):
        configSelect = configSelect+"and description like ('%{}%')".format(property_description)

    if (property_creator_id is not None and property_creator_id != ""):
        configSelect = configSelect+"and creator_id like ('%{}%')".format(property_creator_id)

    sql = text(configSelect)
    with db.engine.connect() as conn:
        result = conn.execute(sql)
        
        configs = []

        for row in result:
            values = row
            config = {
                "code":values[0],
                "name":values[1], 
                "label":values[2], 
                "description":values[3], 
                "type":values[4], 
                "creation_timestamp":values[5].strftime("%Y-%m-%dT%H:%M:%SZ"), 
                "id":values[6]
            }
            
            #add the property meta to the result
            metaSql = text(
            (
                "select code, value from af.property_meta pm  where pm.property_id = {}"
            ).format(values[6])
            )

            metaResult = conn.execute(metaSql)

            #this filters by metas
            skipFlag = False
            for metaRow in metaResult:
                config["property_meta_"+metaRow[0]] = metaRow[1]
                if(property_meta_author is not None and property_meta_author != "" and metaRow[0] == "author" and metaRow[1].lower().find(property_meta_author.lower()) == -1):
                    skipFlag = True
                if(property_meta_email is not None and property_meta_email != "" and metaRow[0] == "email" and metaRow[1].lower().find(property_meta_email.lower()) == -1):
                    skipFlag = True
                if(property_meta_organization_code is not None and property_meta_organization_code != "" and metaRow[0] == "organization_code" and metaRow[1].lower().find(property_meta_organization_code.lower()) == -1):
                    skipFlag = True
                if(property_meta_breeding_program_id is not None and property_meta_breeding_program_id != "" and metaRow[0] == "breeding_program_id" and metaRow[1].lower().find(property_meta_breeding_program_id.lower()) == -1):
                    skipFlag = True
                if(property_meta_design is not None and property_meta_design != "" and metaRow[0] == "design" and metaRow[1].lower().find(property_meta_design.lower()) == -1):
                    skipFlag = True
                if(property_meta_analysis_objective is not None and property_meta_analysis_objective != "" and metaRow[0] == "analysis_objective" and metaRow[1].lower().find(property_meta_analysis_objective.lower()) == -1):
                    skipFlag = True
                if(property_meta_engine is not None and property_meta_engine != "" and metaRow[0] == "engine" and metaRow[1].lower().find(property_meta_engine.lower()) == -1):
                    skipFlag = True
            
            if(skipFlag):
                continue

            #add formula
            formulaSql = text(
            (
                "select code, name, statement from af.property where id in ( select pc.config_property_id from af.property_config pc where property_id = {} ) "+
                "and id in (select pc.config_property_id from af.property_config pc where property_id = 139)"
            ).format(values[6])
            )   
            formulaResult = conn.execute(formulaSql)
            formulas = []
            for formulaRow in formulaResult:
                formulas.append({
                    "statement":formulaRow[2],
                    "id": formulaRow[0].replace("formula_opt",""),
                    "name":formulaRow[1]
                })

            config["formulas"] = formulas

            #fields

            fieldSql = text(
            (
                "select code, name, data_type from af.property where id in ( select pc.config_property_id from af.property_config pc where property_id = {} ) "+
                "and id in (select pc.config_property_id from af.property_config pc where property_id = 159)"
            ).format(values[6])
            )   
            fieldResult = conn.execute(fieldSql)
            fields = []
            for fieldRow in fieldResult:
                fields.append({
                    "stat_factor":fieldRow[0],
                    "data_type":fieldRow[2]
                })
                
            config["fields"] = fields

            #options
            optionSql = text(
            (
                "select code, name, statement from af.property where id in ( select pc.config_property_id from af.property_config pc where property_id = {} ) "+
                "and id in (select pc.config_property_id from af.property_config pc where property_id = 137)"
            ).format(values[6])
            )   
            optionResult = conn.execute(optionSql)
            options = []
            for optionRow in optionResult:
                options.append({
                    "options":optionRow[2],
                    "id": optionRow[0].replace("option_opt","")
                })

            config["options"] = options

            #residuals
            residualSql = text(
            (
                "select code, name, statement, type from af.property where id in ( select pc.config_property_id from af.property_config pc where property_id = {} ) "+
                "and id in (select pc.config_property_id from af.property_config pc where property_id = 140)"
            ).format(values[6])
            )   
            residualResult = conn.execute(residualSql)
            residuals = []
            for residualRow in residualResult:
                residuals.append({
                    "name":residualRow[1],
                    "statement":residualRow[2],
                    "catalog_item":residualRow[3],
                    "id": residualRow[0].replace("residual_opt","")
                })

            config["residuals"] = residuals

            #predictions
            predictionSql = text(
            (
                "select code, name, statement, type from af.property where id in ( select pc.config_property_id from af.property_config pc where property_id = {} ) "+
                "and id in (select pc.config_property_id from af.property_config pc where property_id = 5)"
            ).format(values[6])
            )   
            predictionResult =conn.execute(predictionSql)
            predictions = []
            for predictionRow in predictionResult:
                predictions.append({
                    "name":predictionRow[1],
                    "statement":predictionRow[2],
                    "catalog_item":predictionRow[3],
                })
            
            config["predictions"] = predictions
        
            configs.append(config)

    return configs

def delete_analysis_config(id):
    with db.engine.connect as conn:
    # --prove that there is one record and that it is an analysis config
    # select count(*) from af.property where id in ( select pc.config_property_id from af.property_config pc where property_id = 134 and config_property_id <> 134 ) and id = 248
        proveOneRecordSql = text(
            (
             "select count(*) from af.property where id in ( select pc.config_property_id from af.property_config pc where property_id = 134 and config_property_id <> 134 ) and id = {}"
         ).format(id)
         )   
        proveOneRecordResult = conn.execute(proveOneRecordSql)
        for row in proveOneRecordResult:
         if (row[0] != 1):
             raise Exception("Searching for a matching analysis config did not return exactly one result.")
            
        # --get all the property meta ids for this analysis config
        # select id from af.property_meta pm where property_id = 248
        getAllPropertyMetaIdsSql = text(
            (
                "select id from af.property_meta pm where property_id = {}"
            ).format(id)
            )   
        getAllPropertyMetaIdsResult = conn.execute(getAllPropertyMetaIdsSql)
        propertyMetaIds = []
        for row in getAllPropertyMetaIdsResult:
            propertyMetaIds.append(row[0])

        # --get the id that links root analysis config to this config
        # select id from af.property_config pc where config_property_id = 248 
        getRootPropertyConfigToAnalysisIdSql = text(
            (
                "select id from af.property_config pc where config_property_id = {}"
            ).format(id)
            )   
        getRootPropertyConfigToAnalysisIdResult = conn.execute(getRootPropertyConfigToAnalysisIdSql)
        propertyConfigIds = []
        for row in getRootPropertyConfigToAnalysisIdResult:
            propertyConfigIds.append(row[0])

        # --get all property ids for downstream propertys to the analysis config NOTE DELETE THESE FROM PROPERTY
        # select id from af.property where id in (select config_property_id from af.property_config pc where property_id = 248)
        getPropertyIdsforDownstreamPropertiesSql = text(
            (
                "select id from af.property where id in (select config_property_id from af.property_config pc where property_id = {})"
            ).format(id)
            )   
        getPropertyIdsforDownstreamPropertiesResult = conn.execute(getPropertyIdsforDownstreamPropertiesSql)
        propertyIds = []
        for row in getPropertyIdsforDownstreamPropertiesResult:
            propertyIds.append(row[0])

        # --get the ids for all links to the sub properties
        # select id from af.property_config pc where config_property_id in (select config_property_id from af.property_config pc where property_id = 248 ) 
        getAllDownstreamPropertyIdsSql = text(
            (
                "select id from af.property_config pc where config_property_id in (select config_property_id from af.property_config pc where property_id = {} )"
            ).format(id)
            )   
        getAllDownstreamPropertyIdsResult = conn.execute(getAllDownstreamPropertyIdsSql)
        for row in getAllDownstreamPropertyIdsResult:
            propertyConfigIds.append(row[0])

        propertyIds.append(id)

        #delete all property configs
        for propertyConfigId in propertyConfigIds:
            conn.execute(
                text(("delete from af.property_config where id = {}").format(propertyConfigId))
            )

        #delete all property metas
        for propertyMetaId in propertyMetaIds:
            conn.execute(
                text(("delete from af.property_meta where id = {}").format(propertyMetaId))
            )

        #delete all properties
        for propertyId in propertyIds:
            conn.execute(
                text(("delete from af.property where id = {}").format(propertyId))
            )
            conn.commit()# Moving to connection from db.engine.execute for sqlalchemy 2 - now need to commit conn explicitly, if I'm reading this correctly


# https://bitbucket.org/ebsproject/ba-db/src/develop/build/liquibase/changesets/21.09/data/template/add_2_new_models_for_cimmyt.sql?atlOrigin=eyJpIjoiMWRiZjlmZjhkYmE3NDg0Mzk3NWI3ODZhZjczNGQyODQiLCJwIjoiYmItY2hhdHMtaW50ZWdyYXRpb24ifQ

def update_analysis_config(id, property_code, property_configName, property_label, property_description, property_design, property_data_type, property_creator_id, property_modifier_id, property_tenant_id, property_statement,
    property_meta_version, property_meta_date, property_meta_author, property_meta_email, property_meta_organization_code, property_meta_engine, property_meta_breeding_program_id,
    property_meta_pipeline_id, property_meta_stage_id, property_meta_design, property_meta_trait_level, property_meta_analysis_objective, property_meta_exp_analysis_pattern,
    property_meta_loc_analysis_pattern, property_meta_year_analysis_pattern, property_meta_trait_pattern, fields, options, formulas, residuals, predictions):

    delete_analysis_config(id)
    create_analysis_config(property_code, property_configName, property_label, property_description, property_design, property_data_type, property_creator_id, property_modifier_id, property_tenant_id, property_statement,
    property_meta_version, property_meta_date, property_meta_author, property_meta_email, property_meta_organization_code, property_meta_engine, property_meta_breeding_program_id,
    property_meta_pipeline_id, property_meta_stage_id, property_meta_design, property_meta_trait_level, property_meta_analysis_objective, property_meta_exp_analysis_pattern,
    property_meta_loc_analysis_pattern, property_meta_year_analysis_pattern, property_meta_trait_pattern, fields, options, formulas, residuals, predictions)