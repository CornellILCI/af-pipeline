
from tempfile import NamedTemporaryFile

from af.pipeline.sommer.services import get_prediction, get_model_stat

pred = "/home/vince/Documents/work/BA-726/output_pred.csv"
stat_model = "/home/vince/Documents/work/BA-726/output_statmodel.csv"

def test_sommer_services():
    """
    """
    id = 1
    # testing both how many objects, as well as those pred objects
    t = NamedTemporaryFile()
    ms = "logLik\tAIC\tBIC\tMethod\tConverge\n-397.735837845444\t799.471675690887\t808.840899146223\tNR\tTRUE"
    t.write(bytes(ms, "UTF-8"))
    t.seek(0)
    m = get_model_stat(id,t.name)
    assert m.log_lik == "-397.735837845444"

   
    t = NamedTemporaryFile()
    string = "trait\tID\tpredicted.value\tstandard.error\nPhenotype\tH1\t62.1888255460774\t1.03460693957888\nPhenotype\tH10\t62.641540901158\t1.00062584891098"
    t.write(bytes(string, "UTF-8"))
    t.seek(0) 
    x = get_prediction(id,t.name)
    x2 = x[0]
    assert x2.value == "62.1888255460774"


#   string = ""
#   t.write(bytes(string, "UTF-8"))
#   t.seek(0)
#   print("hi")



