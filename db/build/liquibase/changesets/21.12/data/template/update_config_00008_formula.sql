--liquibase formatted sql

--changeset postgres:update_property_statements context:template splitStatements:false rollbackSplitStatements:false
--comment: BA-840 correct formula name and statement for config_00008

UPDATE af.property
SET name='Alpha-Lattice MET Univariate - G x E structure as heterogeneous variance',
statement='{trait_name} ~ mu loc loc.rep !r idh(loc).rep.block coruh(loc).id(entry) !f mv'
WHERE code = 'formula_opt4'
AND name='Alpha-Lattice MET Univariate'
AND statement='{trait_name} ~ mu loc loc.rep !r loc.rep.block entry entry.loc !f mv';

