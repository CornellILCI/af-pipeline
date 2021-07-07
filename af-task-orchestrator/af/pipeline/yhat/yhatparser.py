import pandas as pd


class YHatParser():
    """
    Prepares DataFrame from yht file
    """


    def __init__(self):
        self.df = None
        self.record = None
        self.yhat = None
        self.residual = None
        self.hat = None

    def read_yht(self,yht):
        self.df =  pd.read_csv(yht, delimiter="\s+" )

    def rename_columns(self):
        self.df.rename(columns={"Record":"record",
                                "Yhat":"yhat",
                                "Residual":"residual",
                                "Hat":"hat"}, inplace=True)

    # def create_dict_for_additional_columns(self):
    #     self.df["additional_info"] = ""


        # self.yhat = self.df['Yhat']
        # self.residual = self.df['Residual']
        # self.hat = self.df['Hat']
    def create_correct_df(self):
        agg_cols = ['RinvRes', 'AOMstat']
        self.df = self.df.join(self.df[agg_cols].agg(dict,axis=1).to_frame('additional_info')).drop(agg_cols,1)
        self.df = self.df.astype(str)

y = YHatParser()
y.read_yht('/home/vince/dev/work/ebsaf/af-core/af-task-orchestrator/af/pipeline/yhat/templates/71ac5d6f-5cdc-45fd-a2fa-2bc17a2c58ad_SA_1001_yht (1).txt')
print(y.df)
y.rename_columns()
# y.create_dict_for_additional_columns()
y.create_correct_df()
print(y.df.head())
