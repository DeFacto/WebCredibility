import pandas as pd
from sklearn.externals import joblib
from coffeeandnoodles.core.util import get_md5_from_string
from trustworthiness.config import DeFactoConfig
from trustworthiness.definitions import OUTPUT_FOLDER
from trustworthiness.feature_extractor import FeaturesCore

config = DeFactoConfig()

if __name__ == '__main__':
    try:
        df_annotations_humans = pd.read_table(OUTPUT_FOLDER + 'exp003/factbench/factbench_annotations.tsv',
                                              sep="\t", na_values=0, low_memory=False, skiprows=1)

        df_annotations_all = pd.read_table(OUTPUT_FOLDER + 'exp003/factbench/factbench_annotations.tsv',
                                           sep="\t", na_values=0, low_memory=False, skiprows=1)

        #file = BENCHMARK_FILE_NAME_TEMPLATE % (BEST_CLS_2class, BEST_PAD_2class, 'bin')
        file = 'cls_decisiontreeclassifier_bin_0_bin.pkl'
        print('loading model: ' + file)
        clf = joblib.load(OUTPUT_FOLDER + 'exp003/3c/models/text_features/' + file)
        encoder = joblib.load(config.enc_domain)

        for index, row in df_annotations_humans.iterrows():
            url = str(row[0])
            claim = row[1]
            likert = row[2]
            urlencoded = get_md5_from_string(url)
            extractor = FeaturesCore(url)
            if extractor.webscrap is None:
                extractor.call_web_scrap()

            if not extractor.error:
                out = extractor.get_final_feature_vector()
                out[3] = encoder.transform([out[3]])[0]
                del out[2]

                prediction = clf.predict([out])
                print(url, prediction[0])

    except:
        raise