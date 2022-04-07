import papermill as pm

for P_NOISE_CHAR in [0.1, 0.15]:
    for ROW_COL_MISSING_OR_SWAPPED in [None, 'SWAP', 'MISSING']:
        for P_ROW_COL_MISSING_OR_SWAPPED in [0.1, 0.2]:
            if ROW_COL_MISSING_OR_SWAPPED is None:
                P_ROW_COL_MISSING_OR_SWAPPED = None
            for TFIDF_NGRAM_LO in [1,2,3,4]:
                for TFIDF_NGRAM_HI in [1,2,3,4]:
                    if TFIDF_NGRAM_HI < TFIDF_NGRAM_LO:
                        continue
                    for TFIDF_MAX_DF in [0.6, 0.8]:
                        for TFIDF_MIN_DF in [20, 50]:
                            pm.execute_notebook(
                               'content_aware_column_match_detection_between_databases.ipynb',
                               'output.ipynb',
                               parameters = dict(
                                    P_NOISE_CHAR = P_NOISE_CHAR,
                                    NUM_TOKENS_KEPT_ADDR = 2,
                                    ROW_COL_MISSING_OR_SWAPPED = ROW_COL_MISSING_OR_SWAPPED,
                                    P_ROW_COL_MISSING_OR_SWAPPED = P_ROW_COL_MISSING_OR_SWAPPED,
                                    FRAC_KEPT_ROWS_DB2 = 0.5,
                                    TFIDF_ANALYZER = 'char_wb',
                                    TFIDF_NGRAM_LO = TFIDF_NGRAM_LO,
                                    TFIDF_NGRAM_HI = TFIDF_NGRAM_HI,
                                    TFIDF_MAX_DF = TFIDF_MAX_DF,
                                    TFIDF_MIN_DF = TFIDF_MIN_DF,
                                    TFIDF_MAX_FEATS = 100000,
                               )
                            )