from tempfile import NamedTemporaryFile

from af.pipeline.sommer.services import get_predictions, get_model_stat


"""
Test get_model_statistics and get_predictions in /af/pipeline/sommer/services.py
"""


#def test_get_model_stat():
#    id = 1
#    t = NamedTemporaryFile()
#    ms = "logLik,AIC,BIC,Method,Converge\n-397.735837845444,799.471675690887,-808.840899146223,NR,TRUE"
#    t.write(bytes(ms, "UTF-8"))
#    t.seek(0)
#    model_stat_object = get_model_stat(id, t.name)
#    assert model_stat_object.log_lik == "-397.735837845444"
#    assert model_stat_object.aic == "799.471675690887"
#    assert model_stat_object.bic == "-808.840899146223"
#    assert model_stat_object.method_id == "NR"
#    assert model_stat_object.is_converged == "TRUE"
#    assert model_stat_object.log_lik != "397.735837845444"
#    assert model_stat_object.aic != "-799.471675690887"
#    assert model_stat_object.bic != "808.840899146223"
#    assert model_stat_object.method_id != ": )"
#    assert model_stat_object.is_converged != "FALSE"
#
#
#def test_get_predictions():
#    t = NamedTemporaryFile()
#    string = "trait,ID,predicted.value,standard.error\nPhenotype,H1,62.1888255460774,1.03460693957888\nPhenotype,H10,62.641540901158,1.00062584891098"
#    t.write(bytes(string, "UTF-8"))
#    t.seek(0)
#    prediction_object_list = get_predictions(id, t.name)
#    prediction_object = prediction_object_list[0]
#    assert prediction_object.trait_value == "Phenotype"
#    assert prediction_object.id == "H1"
#    assert prediction_object.value == "62.1888255460774"
#    assert prediction_object.std_error == "1.03460693957888"
#    assert prediction_object.trait_value != "Genotype"
#    assert prediction_object.id != "H2"
#    assert prediction_object.value != "-62.1888255460774"
#    assert prediction_object.std_error != "-1.03460693957888"
