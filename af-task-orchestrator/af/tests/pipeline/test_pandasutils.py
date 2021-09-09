import os
from tempfile import TemporaryDirectory

import pandas as pd
from af.pipeline import pandasutil
from pandas._testing import assert_frame_equal


def test_save_dataframe():

    output_folder = TemporaryDirectory()

    input_dataframe = pd.DataFrame([{"a": 1, "b": 1}, {"a": 2, "b": 2}])

    file_name = "test"

    pandasutil.save_df_to_tsv(input_dataframe, file_name, output_folder.name)

    output_file = os.path.join(output_folder.name, file_name)

    with open(output_file) as f:
        dataframe_from_saved_file = pd.read_csv(f, sep="\t")
        assert_frame_equal(dataframe_from_saved_file, input_dataframe)

