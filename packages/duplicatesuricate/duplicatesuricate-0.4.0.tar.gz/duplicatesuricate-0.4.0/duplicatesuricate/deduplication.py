import neatmartinet as nm
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score


class Suricate:
    def __init__(self, input_records,
                 target_records,
                 model,
                 filterdict=None,
                 intermediate_thresholds=None,
                 cleanfunc=None,
                 idcol='groupid', queryidcol='queryid', decision_threshold=0.5, verbose=True):
        """

        Args:
            input_records (pd.DataFrame): Input table for record linkage, records to link
            target_records (pd.DataFrame): Table of reference for record linkage
            model: evaluation model, has a .predict_proba and a .used_cols function
            filterdict (dict): define the all/any logic used detailed in filter_all_any {'all':['country_code'],'any':['duns']}
            intermediate_thresholds(dict): add an intermediary filter {'name_fuzzyscore':0.8}
            cleanfunc: cleaning function used for the databases
            idcol (str): name of the column where to store the deduplication results
            queryidcol (str): name of the column used to store the original match
            verbose (bool): Turns on or off prints
        """
        if cleanfunc is None:
            cleanfunc = lambda x: x

        self.input_records = cleanfunc(input_records)
        self.target_records = cleanfunc(target_records)

        self.linker = RecordLinker(df=self.target_records,
                                   filterdict=filterdict,
                                   intermediate_thresholds=intermediate_thresholds,
                                   evaluator=model, decision_threshold=decision_threshold
                                   )

        missingcols = list(filter(lambda x: x not in self.input_records.columns, self.linker.compared_cols))
        if len(missingcols) > 0:
            raise KeyError('RecordLinker does not have all necessary columns in input after cleaning', missingcols)

        missingcols = list(filter(lambda x: x not in self.target_records.columns, self.linker.compared_cols))
        if len(missingcols) > 0:
            raise KeyError('RecordLinker does not have all necessary columns in target after cleaning', missingcols)

        self.idcol = idcol
        self.queryidcol = queryidcol
        self.verbose = verbose

        self._results = {}
        pass

    def _generate_query_index_(self, in_index=None):
        """
        this function returns a random index from the input records with no group id to start the linkage process
        Args:
            in_index (pd.Index): index or list, default None the query should be in the selected index

        Returns:
            object: an index of the input records
        """

        if in_index is None:
            in_index = self.input_records.index

        x = self.input_records.loc[in_index]
        possiblechoices = x.loc[(x[self.idcol] == 0) | (x[self.idcol].isnull())].index
        if possiblechoices.shape[0] == 0:
            del x
            return None
        else:
            a = np.random.choice(possiblechoices)
            del x, possiblechoices
            return a

    def _find_matches_(self, query_index, n_matches_max=1):
        """
       search for records in the target records that match the query (input_records.loc[query_index])
        Args:
            query_index: index of the row to be deduplicated
            n_matches_max (int): max number of matches to be fetched. If None, all matches would be returned

        Returns:
            pd.Index (list of index in the target records)
        """

        # return the good matches as calculated by the evaluation

        goodmatches_index = self.linker.return_good_matches(query=self.input_records.loc[query_index])

        if goodmatches_index is None or len(goodmatches_index) == 0:
            return None
        elif n_matches_max is None:
            return goodmatches_index
        else:
            return goodmatches_index[:n_matches_max]

    def start_linkage(self, sample_size=10, in_index=None, n_matches_max=1, with_proba=False) -> dict:
        """
        Takes as input an index of the input records, and returns a dict showing their corresponding matches
        on the target records
        Args:
            in_index (pd.Index): index of the records (from input_records) to be deduplicated
            sample_size (int): number of records to be deduplicated. If 'all' is provided, deduplicaate all
            n_matches_max (int): maximum number of possible matches to be returned.
                If none, all matches would be returned
            with_proba (bool): whether or not to return the probabilities

        Returns:
            dict : results in the form of {index_of_input_record:[list of index_of_target_records]} or
                    {index_of_input_record:{index_of_target_records:proba of target records}}
        """
        if in_index is None and n_matches_max is None and with_proba is True:
            print(
                'careful, huge number of results (cartesian product) will be returned. Limit to the best probables matches with n_matches_,ax or set with_proba = False')
        if in_index is None:
            in_index = self.input_records.index

        if sample_size == 'all' or sample_size is None:
            n_total = self.input_records.shape[0]
        else:
            n_total = sample_size

        in_index = in_index[:n_total]

        print('starting deduplication at {}'.format(pd.datetime.now()))
        self._results = {}
        if with_proba is False:
            for i, ix in enumerate(in_index):
                # timing
                time_start = pd.datetime.now()

                goodmatches_index = self._find_matches_(query_index=ix, n_matches_max=n_matches_max)

                if goodmatches_index is None:
                    self._results[ix] = None
                    n_deduplicated = 0
                else:
                    self._results[ix] = list(goodmatches_index)
                    n_deduplicated = len(self._results[ix])

                # timing
                time_end = pd.datetime.now()
                duration = (time_end - time_start).total_seconds()

                if self.verbose:
                    print(
                        '{} of {} inputs records deduplicated | found {} of {} max possible matches | time elapsed {} s'.format(
                            i + 1, n_total, n_deduplicated, n_matches_max, duration))

            print('finished work at {}'.format(pd.datetime.now()))
        else:
            # return proba
            # timing
            time_start = pd.datetime.now()
            for i, ix in enumerate(in_index):
                # get the probability vector
                y_proba = self.linker.predict_proba(query=self.input_records.loc[ix])
                # if none sve none
                if y_proba is None or len(y_proba) == 0:
                    self._results[ix] = None
                    n_deduplicated = 0
                else:
                    # take the top n_matches_max to save
                    if n_matches_max is not None:
                        y_proba = y_proba.iloc[:n_matches_max]

                    self._results[ix] = y_proba.to_dict()
                    n_deduplicated = len(self._results[ix])

                # timing
                time_end = pd.datetime.now()
                duration = (time_end - time_start).total_seconds()

                if self.verbose:
                    print(
                        '{} of {} inputs records deduplicated | found {} of {} max possible matches | time elapsed {} s'.format(
                            i + 1, n_total, n_deduplicated, n_matches_max, duration))

            print('finished work at {}'.format(pd.datetime.now()))
        return self._results

    def format_results(self, res, display=None, fuzzyscorecols=None, exactscorecols=None, with_proba=False):
        """
        Return a formatted, side by side comparison of results
        Args:
            res (dict): results {'ix_source_1':['ix_target_2','ix_target_3']} / {'ix_source':{'ix_target1':0.9,'ix_target2':0.5}}
            display (list): list of columns to be displayed
            fuzzyscorecols (list): list of columns on which to perform fuzzy score
            exactscorecols (list): list of columns on which to calculate the number of exact_matching
            with_proba (bool) : if the result list has a list of probabilities
        Returns:
            pd.DataFrame
        """
        # x = pd.Series(index=list(r.keys()),values=list(r.keys()))
        # df=x.apply(lambda r:pd.Series(r))
        # assert isinstance(df,pd.DataFrame)

        # Melt the results dictionnary to have the form:
        # df.columns = ['ix_source','ix_target'] if with_proba is false, ['ix_source','ix_target','y_proba' otherwise]
        if with_proba is False:
            df = pd.DataFrame(columns=['ix_source', 'ix_target'])
            for ix_source in list(res.keys()):
                matches = res.get(ix_source)
                if matches is not None:
                    ixs_target = pd.Series(data=matches)
                    ixs_target.name = 'ix_target'
                    temp = pd.DataFrame(ixs_target).reset_index(drop=True)
                    temp['ix_source'] = ix_source
                    df = pd.concat([df, temp], axis=0, ignore_index=True)
            df.reset_index(inplace=True, drop=True)
        else:
            df = pd.DataFrame(columns=['ix_source', 'ix_target', 'y_proba'])
            for ix_source in list(res.keys()):
                probas = res.get(ix_source)
                if probas is not None:
                    ixs_target = pd.Series(probas)
                    ixs_target.index.name = 'ix_target'
                    ixs_target.name = 'y_proba'
                    temp = pd.DataFrame(ixs_target).reset_index(drop=False)
                    temp['ix_source'] = ix_source
                    df = pd.concat([df, temp], axis=0, ignore_index=True)
            df.reset_index(inplace=True, drop=True)

        if df.shape[0] == 0:
            return None
        if display is None:
            display = self.linker.compared_cols
        if fuzzyscorecols is None:
            allcols = display
        else:
            allcols = list(set(display + fuzzyscorecols))
        for c in allcols:
            df[c + '_source'] = df['ix_source'].apply(lambda r: self.input_records.loc[r, c])
            df[c + '_target'] = df['ix_target'].apply(lambda r: self.target_records.loc[r, c])

        if fuzzyscorecols is not None:
            df_fuzzy = pd.DataFrame(index=df.index)
            for c in fuzzyscorecols:
                df_fuzzy[c + '_fuzzyscore'] = df.apply(
                    lambda r: nm.compare_twostrings(r[c + '_source'], r[c + '_target']), axis=1)
            # after the loop, take the sum of the exact score (n ids matchings)
            df_fuzzy['avg_fuzzyscore'] = df_fuzzy.fillna(0).mean(axis=1)
            df = df.join(df_fuzzy)

        if exactscorecols is not None:
            df_exact = pd.DataFrame(index=df.index)
            for c in exactscorecols:
                # Make sure columns or in the table
                for s in ['_source', '_target']:
                    colname = (c + s)
                    if colname not in df.columns:
                        if s == '_source':
                            df[colname] = df['ix' + s].apply(lambda r: self.input_records.loc[r, c])
                        elif s == '_target':
                            df[colname] = df['ix' + s].apply(lambda r: self.target_records.loc[r, c])
                # Calculate the score
                df_exact[c + '_exactscore'] = df.apply(lambda r: nm.exactmatch(r[c + '_source'], r[c + '_target']),
                                                       axis=1)
            # after the loop, take the sum of the exact score (n ids matchings)
            df_exact['n_exactmatches'] = df_exact.fillna(0).sum(axis=1)
            df = df.join(df_exact)

        return df

    def build_labelled_table(self, query_index, on_index=None, display=None, fuzzy=None, ids=None,
                             return_filtered=True):
        """
        Create a labelled table
        Args:
            query_index (obj): name of the query index
            on_index (pd.Index): index of the target records
            display (list): list of columns to be displayed
            fuzzy (list): list of columns on which to perform fuzzy score
            ids (list): list of columns on which to calculate the number of exact_matching
            return_filtered (bool): if False, all targets row are returned (no filtering step)
        Returns:
            pd.DataFrame
        """
        y_proba = self.linker.predict_proba(query=self.input_records.loc[query_index],
                                            on_index=on_index,
                                            return_filtered=return_filtered)

        if y_proba is None or y_proba.shape[0] == 0:
            if return_filtered is True:
                return None
            else:
                y_proba = pd.Series(index=on_index).fillna(0)

        res = {query_index: list(y_proba.index)}

        table = self.format_results(res=res, display=display, fuzzyscorecols=fuzzy, exactscorecols=ids)
        table['y_proba'] = table['ix_target'].apply(lambda r: y_proba.loc[r])

        return table

    def chain_build_labelled_table(self, inputs, targets, display=None, fuzzy=None, ids=None):
        """
        Create a labelled table
        Args:
            inputs (pd.Index): list of records names to be linked
            targets (pd.Index): list of records names to be linked to
            display (list): list of columns to be displayed
            fuzzy (list): list of columns on which to perform fuzzy score
            ids (list): list of columns on which to calculate the number of exact_matching
        Returns:
            pd.DataFrame

        """
        res = {}
        for u, v in zip(inputs, targets):
            res[u] = [v]

        table = self.format_results(res, display=display, fuzzyscorecols=fuzzy, exactscorecols=ids)
        return table

    def build_training_table(self, inputs, targets, y_true, scoredict=None):
        """
        Create a scoring table, with a label (y_true), for supervised learning
        inputs, targets,y_true are expected to be of the same length
        Args:
            inputs (pd.Series): list of index of the input dataframe
            targets (pd.Series): list of index of the target dataframe
            y_true (pd.Series): labelled values (0 or 1) to say if it's a match or not
            scoredict (dict): dictionnary of scores you want to calculate

        Returns:
            pd.DataFrame
        """

        training_table_complete = pd.DataFrame(columns=self.linker.score_cols + ['y_true'])
        for t, u, v in zip(inputs, targets, y_true):
            similarity_vector = self.linker.scoringmodel.build_similarity_table(query=self.input_records.loc[t],
                                                                                on_index=pd.Index([u]),
                                                                                scoredict=scoredict)
            similarity_vector['y_true'] = v
            training_table_complete = pd.concat([training_table_complete, similarity_vector], ignore_index=True, axis=0)

        return training_table_complete


class RecordLinker:
    def __init__(self,
                 df, filterdict=None,
                 intermediate_thresholds=None,
                 fillna=-1,
                 evaluator=None,
                 decision_threshold=0.5,
                 verbose=True):
        """
        This class merges together the Scorer and the Evaluation model.
        it creates a similarity table
        evaluate the probability of being a match with the model
        and then can either:
        - return that probability with predict_proba
        - return a boolean: probability is higher than a decision threshold with predict
        - or return the index of the good matches with return_good_matches

        Args:
            df (pd.DataFrame): target records
            filterdict (dict): filtering dict with exact matches on an {'all':['country'],'any':[id1,id2]}
            intermediate_thresholds (dict): dictionary of minimum thresholds for intermediate scoring {'name_fuzzyscore':0.6}
            fillna (float): value with which to fill na values
            evaluator : Class used to calculate a probability vector. Has .predict_proba function and .used_cols attribute ['name_tokenscore','street_fuzzyscore']
            decision_threshold (float), default 0.8
            verbose (bool): control print output
        """

        self.verbose = verbose

        self.df = df

        # initiate query to empty
        self.query = pd.Series()

        self.decision_threshold = decision_threshold

        self.evaluationmodel = evaluator

        # set all compared cols to empty
        self.compared_cols = []
        self.score_cols = []
        self.filterdict = {}
        self.intermediate_score = {}
        self.further_score = {}

        # calculate compared cols based on parameters given to calculate comparison operations to perform and optimize code
        # Set the following parameters:
        # .filterdict, .intermediate_score, .further_score
        # .compared_cols, .score_cols

        self._calculate_scoredict(filterdict=filterdict,
                                  intermediatethreshold=intermediate_thresholds,
                                  decision_cols=self.evaluationmodel.used_cols)

        # configure the intermediate decision function
        # If threshold: threshold_based, if no : let all pass)
        if intermediate_thresholds is not None:
            decision_int_func = lambda r: threshold_based_decision(row=r, thresholds=intermediate_thresholds)
        else:
            decision_int_func = lambda r: 1

        # create associate scoring and filtering model
        self.scoringmodel = Scorer(df=df,
                                   filterdict=self.filterdict,
                                   score_intermediate=self.intermediate_score,
                                   decision_intermediate=decision_int_func,
                                   score_further=self.further_score,
                                   fillna=fillna
                                   )

        missingcols = list(filter(lambda x: x not in self.scoringmodel.scorecols, self.evaluationmodel.used_cols))
        if len(missingcols) > 0:
            raise KeyError('not all training columns are found in the output of the scorer:', missingcols)
        pass

    def _calculate_scoredict(self, filterdict, intermediatethreshold, decision_cols):
        """
        Set the following parameters:

        Dictionnaries of comparison operations to perform, and in which order
            self.filterdict: {'all': ['country_code'], 'any': ['duns']}
            self.intermediate_score {'fuzzy': ['name']}
            self.furtherscore : {'acronym': None, 'exact': None, 'fuzzy': ['street','name_wostopwords'],'token': ['name']}

        List of columns:
            self.compared_cols=['country_code','duns','name','street','name_wostopwords']
            self.score_cols=['country_code_exactscore','duns_exactscore','name_fuzzyscore','name_tokenscore','street_fuzzyscore','name_wostopwords_fuzzyscore']

        Args:
            filterdict (dict): {'all':['country'],'any':[id1,id2]}
            intermediatethreshold (dict): {'name_fuzzyscore':0.6}
            decision_cols (list): ['name_tokenscore','street_fuzzyscore','name_wostopwords_fuzzyscore']

        Returns:
            None
        """
        self.compared_cols = []
        self.score_cols = []

        if filterdict is not None:
            self.filterdict = _checkdict(filterdict, mandatorykeys=['all', 'any'], existinginput=self.score_cols)
            incols, outcols = _unpack_scoredict(self.filterdict)
            self.compared_cols += incols
            self.score_cols += outcols
        else:
            self.filterdict = None

        if intermediatethreshold is not None and len(intermediatethreshold) > 0:
            score_intermediate = calculatescoredict(existing_cols=self.score_cols,
                                                    used_cols=list(intermediatethreshold.keys()))
        else:
            score_intermediate = None

        if score_intermediate is not None:
            self.intermediate_score = _checkdict(score_intermediate, mandatorykeys=scoringkeys,
                                                 existinginput=self.score_cols)
            incols, outcols = _unpack_scoredict(self.intermediate_score)
            self.compared_cols += incols
            self.score_cols += outcols
        else:
            self.intermediate_score = None

        if decision_cols is not None and len(decision_cols) > 0:
            score_further = calculatescoredict(existing_cols=self.score_cols, used_cols=decision_cols)
        else:
            score_further = None

        if score_further is not None:
            self.further_score = _checkdict(score_further, mandatorykeys=scoringkeys, existinginput=self.score_cols)
            incols, outcols = _unpack_scoredict(self.further_score)
            self.compared_cols += incols
            self.score_cols += outcols
        else:
            self.further_score = None

        self.compared_cols = list(set(self.compared_cols))
        self.score_cols = list(set(self.score_cols))
        pass

    def return_good_matches(self, query, decision_threshold=None, on_index=None, n_matches_max=1):
        """
        Return the good matches
        - with the help of the scoring model, create a similarity table
        - with the help of the evaluation model, evaluate the probability of it being a match
        - using the decision threshold, decides if it is a match or not
        - return the index of the good matches
        Args:
            query (pd.Series): information available on our query
            decision_threshold (float): decision_threshold between 0 and 1
            on_index (pd.Index): index on which to return the records
            n_matches_max (int): number of matches to be returned

        Returns:
            pd.Index: the index of the target records identified as the same as the query by the algorithm

        """
        if decision_threshold is None:
            decision_threshold = self.decision_threshold

        y_bool = self.predict(query, decision_threshold=decision_threshold, on_index=on_index)

        if y_bool is None:
            return None
        else:
            goodmatches = y_bool.loc[y_bool].index
            if len(goodmatches) == 0:
                return None
            else:
                goodmatches = goodmatches[:max(n_matches_max, len(goodmatches))]
            return goodmatches

    def predict(self, query, decision_threshold=None, on_index=None):
        """
        Predict if it is a match or not.
        - with the help of the scoring model, create a similarity table
        - with the help of the evaluation model, evaluate the probability of it being a match
        - using the decision threshold, decides if it is a match or not

        Args:
            query (pd.Series): information available on our query
            decision_threshold (float): default None. number between 0 and 1. If not provided, take the default one from the model
            on_index (pd.Index): index on which to do the prediction

        Returns:
            pd.Series: a boolean vector: True if it is a match, false otherwise

        """
        if decision_threshold is None:
            decision_threshold = self.decision_threshold

        # calculate the probability of the records being the same as the query through the machine learning evaluation
        y_proba = self.predict_proba(query, on_index=on_index)
        if y_proba is None:
            return None
        else:
            assert isinstance(y_proba, pd.Series)
            # transform that probability in a boolean via a decision threshold
            # noinspection PyTypeChecker
            y_bool = (y_proba > decision_threshold)
            assert isinstance(y_bool, pd.Series)

            return y_bool

    def predict_proba(self, query, on_index=None, return_filtered=True):
        """
        Main method of this class:
        - with the help of the scoring model, create a similarity table
        - with the help of the evaluation model, evaluate the probability of it being a match
        - returns that probability

        Args:
            query (pd.Series): information available on our query
            on_index (pd.Index): index on which to do the prediction
            return_filtered (bool): whether or not to filter the table
        Returns:
            pd.Series : the probability vector of the target records being the same as the query

        """

        table_score_complete = self.scoringmodel.filter_compare(query=query, on_index=on_index,
                                                                return_filtered=return_filtered)

        if table_score_complete is None or table_score_complete.shape[0] == 0:
            return None
        else:
            # launch prediction using the predict_proba of the scikit-learn module

            y_proba = self.evaluationmodel.predict_proba(table_score_complete).copy()

            del table_score_complete

            # sort the results
            y_proba.sort_values(ascending=False, inplace=True)

            return y_proba

    def _showprobablematches(self, query, n_records=10, display=None, return_filtered=True):
        """
        Show the best matching recors after the filter_all_any method of the scorer
        Could be of interest to investigate the possible matches of a query
        Args:
            query (pd.Series):
            n_records (int): max number of records to be displayed
            display (list): list of columns to be displayed
            return_filtered (bool): whether or not to filter the table

        Returns:
            pd.DataFrame, incl. query

        """
        if n_records is None:
            n_records = self.df.shape[0]

        if display is None:
            display = self.compared_cols
        records = pd.DataFrame(columns=['proba'] + display)
        records.loc[0] = query[display].copy()
        records.rename(index={0: 'query'}, inplace=True)
        records.loc['query', 'proba'] = 'query'

        y_proba = self.predict_proba(query, return_filtered=return_filtered)
        if y_proba is not None and y_proba.shape[0] > 0:
            y_proba.sort_values(ascending=False, inplace=True)
            n_records = min(n_records, y_proba.shape[0])
            results = self.df.loc[y_proba.index[:n_records], display]
            results['proba'] = y_proba
            records = pd.concat([records, results], axis=0)
            return records
        else:
            return None

    def _showfilterstep(self, query, n_records=10, display=None, return_filtered=True):
        """
        Not used anymore
        Show the best matching recors after the filter_all_any method of the scorer
        Could be of interest to investigate the possible matches of a query
        Args:
            query (pd.Series):
            n_records (int): max number of records to be displayed
            display (list): list of columns to be displayed
            return_filtered (bool): whether or not to filter the table

        Returns:
            pd.DataFrame, incl query

        """
        if n_records is None:
            n_records = self.df.shape[0]

        if display is None:
            display = self.compared_cols
        records = pd.DataFrame(columns=['totalscore'] + display)
        records.loc[0] = query[display].copy()
        records.rename(index={0: 'query'}, inplace=True)
        records.loc['query', 'totalscore'] = 'query'

        table = self.scoringmodel.filter_all_any(query=query, return_filtered=return_filtered)
        if table is not None and table.shape[0] > 0:
            y_sum = table.sum(axis=1)
            y_sum.sort_values(ascending=False, inplace=True)
            n_records = min(n_records, y_sum.shape[0])
            results = self.df.loc[y_sum.index[:n_records], display]
            results['totalscore'] = y_sum
            records = pd.concat([records, results], axis=0)
            return records
        else:
            return None

    def _showscoringstep(self, query, n_records=10, display=None, return_filtered=True):
        """
        Not used anymore
        Show the total score of the scoring table after the filter_compare method of the scorer
        Could be of interest to investigate the possible matches of a query
        Args:
            query (pd.Series):
            n_records (int): max number of records to be displayed
            display (list): list of columns to be displayed
            return_filtered (bool): whether or not to filter the table

        Returns:
            pd.DataFrame, incl query as the first row

        """
        if n_records is None:
            n_records = self.df.shape[0]

        if display is None:
            display = self.compared_cols
        records = pd.DataFrame(columns=['totalscore'] + display)
        records.loc[0] = query[display].copy()
        records.rename(index={0: 'query'}, inplace=True)
        records.loc['query', 'totalscore'] = 'query'

        table = self.scoringmodel.filter_compare(query=query, return_filtered=return_filtered)

        if table is not None and table.shape[0] > 0:
            y_sum = table.sum(axis=1)
            y_sum.sort_values(ascending=False, inplace=True)
            n_records = min(n_records, y_sum.shape[0])
            results = self.df.loc[y_sum.index[:n_records], display]
            results['totalscore'] = y_sum
            records = pd.concat([records, results], axis=0)

            return records
        else:
            return None

    def _showsimilarityvector(self, query, target_index, scoredict=None):
        """
        returns the similarity vector, or the scoring vector, between a query and a target
        Args:
            query (pd.Series): name and attribute of the query
            target_index (obj): index of the target record
            scoredict (dict): dictionnary of the scores, default None --> default one used

        Returns:
            pd.Series similarity vector used for the decision function
        """

        scoring_vector = self.scoringmodel.build_similarity_table(query=query,
                                                                  on_index=pd.Index([target_index]),
                                                                  scoredict=scoredict)

        return scoring_vector


def threshold_based_decision(row, thresholds):
    """
    if any  (or all values) values of the row are above the thresholds, return 1, else return 0
    Args:
        row (pd.Series): row to be decided
        thresholds (dict): threshold of values {'aggfunc':'all' or 'any','name_fuzzyscore':0.6,'street_tokenscore':0.8
                    'fillna':0}

    Returns:
        float

    """
    #
    navalue = thresholds.get('fillna')
    if navalue is None:
        navalue = 0
    elif navalue == 'dropna':
        row = row.dropna()
    row = row.fillna(navalue)

    aggfunc = thresholds.get('aggfunc')

    if aggfunc == 'all':
        f = all
    elif aggfunc == 'any':
        f = any
    else:
        f = any
    scorekeys = thresholds.keys()
    scorekeys = filter(lambda k: k.endswith('score'), scorekeys)
    result = map(lambda k: row[k] >= thresholds[k], list(scorekeys))
    result = f(result)

    return result


scorename = {'fuzzy': '_fuzzyscore',
             'token': '_tokenscore',
             'exact': '_exactscore',
             'acronym': '_acronymscore'}
scorefuncs = {'fuzzy': nm.compare_twostrings,
              'token': nm.compare_tokenized_strings,
              'exact': nm.exactmatch,
              'acronym': nm.compare_acronyme}
scoringkeys = list(scorename.keys())


class Scorer:
    def __init__(self, df, filterdict=None, score_intermediate=None, decision_intermediate=None, score_further=None,
                 fillna=-1):
        """
        This class is used to calculate similarity tables between a reference table and a possible query.
        It has three main steps in proceeding:
        - filter based on an all / any logic (filter_all_any)
        - calculate an intermediate score using  build_similarity_table
        - takes an intermediate decision function
        - if the decision function is positive, calculate further scores using  build_similarity_table
        - those three steps are meshed together in the filter_compare method
        Args:
            df (pd.DataFrame): reference records
            filterdict (dict): define the all/any logic used detailed in filter_all_any
            score_intermediate (dict): create the intermediate scoring table using a scoredict detailed in _unpackscoredict
            decision_intermediate (func): take a decision: function takes as input a row of the scoring table and returns a boolean
            score_further (dict): creates the additional scoring fields using a scoredict
            fillna (float): Value used to fill the na values
        Examples:
            filterdict : {'all':
        """

        self.df = df
        self.scorecols = []
        self.compared_cols = []

        self.filterdict = _checkdict(filterdict, mandatorykeys=['all', 'any'], existinginput=self.scorecols)
        incols, outcols = _unpack_scoredict(self.filterdict)
        self.compared_cols += incols
        self.scorecols += outcols

        self.intermediate_score = _checkdict(score_intermediate, mandatorykeys=scoringkeys,
                                             existinginput=self.scorecols)
        incols, outcols = _unpack_scoredict(self.intermediate_score)
        self.compared_cols += incols
        self.scorecols += outcols

        self.further_score = _checkdict(score_further, mandatorykeys=scoringkeys, existinginput=self.scorecols)
        incols, outcols = _unpack_scoredict(self.further_score)
        self.compared_cols += incols
        self.scorecols += outcols

        self.total_scoredict = calculatescoredict(used_cols=self.scorecols)

        self.intermediate_func = decision_intermediate

        self.navalue = fillna

        self.input_records = pd.DataFrame()

        pass

    def filter_all_any(self, query, on_index=None, filterdict=None, return_filtered=True):
        """
        returns a pre-filtered table score calculated on the column names provided in the filterdict.
        in the values for 'any': an exact match on any of these columns ensure the row is kept for further analysis
        in the values for 'all': an exact match on all of these columns ensure the row is kept for further analysis
        if the row does not have any exact match for the 'any' columns, or if it has one bad match for the 'all' columns,
        it is filtered out
        MODIF: if return_filtered, this will not filter the table at all but just returns the scores
        Args:
            query (pd.Series): query
            on_index (pd.Index): index
            filterdict(dict): dictionnary two lists of values: 'any' and 'all' {'all':['country_code'],'any':['duns','taxid']}
            return_filtered (bool): whether or not to filter after calculation of the first scores (Not filtering used for deep inspections of the results)

        Returns:
            pd.DataFrame: a DataFrame with the exact score of the columns provided in the filterdict

        Examples:
            table = ['country_code_exactscore','duns_exactscore']
        """
        # create repository for the score
        table = pd.DataFrame(index=on_index)

        # Tackle the case where no index is given: use the whole index available
        if on_index is None:
            on_index = self.df.index

        # if no specific filterdict is given use the one from init
        if filterdict is None:
            filterdict = self.filterdict

        # if no filter dict is given returns an empty table with all of the rows selected: no filterdict has been applied!
        if filterdict is None:
            return table

        match_any_cols = filterdict.get('any')
        match_all_cols = filterdict.get('all')

        # same as comment above
        if match_all_cols is None and match_any_cols is None:
            return table

        df = self.df.loc[on_index]

        # perform the "any criterias match" logic
        if match_any_cols is not None:
            match_any_df = pd.DataFrame(index=on_index)
            for c in match_any_cols:
                match_any_df[c + '_exactscore'] = df[c].apply(
                    lambda r: nm.exactmatch(r, query[c]))
            y = (match_any_df == 1)
            assert isinstance(y, pd.DataFrame)

            anycriteriasmatch = y.any(axis=1)
            table = pd.concat([table, match_any_df], axis=1)
        else:
            anycriteriasmatch = pd.Series(index=on_index).fillna(False)

        # perform the "all criterias match" logic
        if match_all_cols is not None:
            match_all_df = pd.DataFrame(index=on_index)
            for c in match_all_cols:
                match_all_df[c + '_exactscore'] = df[c].apply(
                    lambda r: nm.exactmatch(r, query[c]))
            y = (match_all_df == 1)
            assert isinstance(y, pd.DataFrame)
            allcriteriasmatch = y.all(axis=1)

            table = pd.concat([table, match_all_df], axis=1)
        else:
            allcriteriasmatch = pd.Series(index=on_index).fillna(False)

        # perform the all criterias match OR at least one criteria match logic
        results = (allcriteriasmatch | anycriteriasmatch)

        assert isinstance(table, pd.DataFrame)

        if return_filtered is True:
            table = table.loc[results]

        return table

    def build_similarity_table(self,
                               query,
                               on_index=None,
                               scoredict=None):
        """
        Return the similarity features between the query and the rows in the required index, with the selected comparison functions.
        They can be fuzzy, token-based, exact, or acronym.
        The attribute request creates two column: one with the value for the query and one with the value for the row

        Args:
            query (pd.Series): attributes of the query
            on_index (pd.Index):
            scoredict (dict):

        Returns:
            pd.DataFrame:

        Examples:
            scoredict={'attributes':['name_len'],
                        'fuzzy':['name','street']
                        'token':'name',
                        'exact':'id'
                        'acronym':'name'}
            returns a comparison table with the following column names (and the associated scores):
                ['name_len_query','name_len_row','name_fuzzyscore','street_fuzzyscore',
                'name_tokenscore','id_exactscore','name_acronymscore']
        """

        if on_index is None:
            on_index = self.df.index

        if scoredict is None:
            scoredict = self.total_scoredict

        table_score = pd.DataFrame(index=on_index)

        attributes_cols = scoredict.get('attributes')
        if attributes_cols is not None:
            for c in attributes_cols:
                table_score[c + '_query'] = query[c]
                table_score[c + '_row'] = self.df.loc[on_index, c]

        for c in scoringkeys:
            table = self._compare(query, on_index=on_index, on_cols=scoredict.get(c), func=scorefuncs[c],
                                  suffix=scorename[c])
            table_score = pd.concat([table_score, table], axis=1)

        return table_score

    def filter_compare(self, query, on_index=None, return_filtered=True):
        """
        Simultaneously create a similarity table and filter the data.
        It works in three steps:
        - filter with a logic (exact match on any of these cols OR exact match on all of these columns)
        - intermediate score with dedicated comparison methods on selected columns
        - filter with an intermediate decision function
        - further score with dedicated comparison methods on selected columns
        - returns the final similarity table which is the concatenation of all of the scoring functions above on the rows
            that have been filtered
        MODIF : if return_filtered parameter is set to False, then it will not filter the data.

        Args:
            query (pd.Series): query
            on_index (pd.Index): index on which to filter and compare
            return_filtered (bool): whether or not to filter after calculation of the first scores

        Returns:
            pd.DataFrame similarity table
        """

        # pre filter the records for further scoring based on an all / any exact match
        if on_index is None:
            workingindex = self.df.index
        else:
            workingindex = on_index

        table_score_complete = self.filter_all_any(query=query,
                                                   on_index=workingindex,
                                                   filterdict=self.filterdict,
                                                   return_filtered=return_filtered
                                                   )
        workingindex = table_score_complete.index

        if table_score_complete.shape[0] == 0:
            return None

        else:
            # do further scoring on the possible choices and the sure choices
            table_intermediate = self.build_similarity_table(query=query,
                                                             on_index=workingindex,
                                                             scoredict=self.intermediate_score)

            table_score_complete = table_score_complete.join(table_intermediate, how='left')
            del table_intermediate

            y_intermediate = table_score_complete.apply(lambda r: self.intermediate_func(r), axis=1)
            y_intermediate = y_intermediate.astype(bool)

            assert isinstance(y_intermediate, pd.Series)
            assert (y_intermediate.dtype == bool)

            if return_filtered is True:
                table_score_complete = table_score_complete.loc[y_intermediate]

            workingindex = table_score_complete.index

            if table_score_complete.shape[0] == 0:
                return None
            else:
                # we perform further analysis on the filtered index:
                # we complete the fuzzy score with additional columns

                table_additional = self.build_similarity_table(query=query, on_index=workingindex,
                                                               scoredict=self.further_score)

                # check to make sure no duplicates columns
                duplicatecols = list(filter(lambda x: x in table_score_complete.columns, table_additional.columns))
                if len(duplicatecols) > 0:
                    table_additional.drop(duplicatecols, axis=1, inplace=True)

                # we join the two tables to have a complete view of the score
                table_score_complete = table_score_complete.join(table_additional, how='left')

                del table_additional

                table_score_complete = table_score_complete.fillna(self.navalue)

                return table_score_complete

    def _compare(self, query, on_index, on_cols, func, suffix):
        """
        compare the query to the target records on the selected row, with the selected cols,
        with a function. returns a pd.DataFrame with colum names the names of the columns compared and a suffix.
        if the query is null for the given column name, it retuns an empty column
        Args:
            query (pd.Series): query
            on_index (pd.Index): index on which to compare
            on_cols (list): list of columns on which to compare
            func (func): comparison function
            suffix (str): string to be added after column name

        Returns:
            pd.DataFrame

        Examples:
            table = self._compare(query,on_index=index,on_cols=['name','street'],func=fuzzyratio,sufix='_fuzzyscore')
            returns column names ['name_fuzzyscore','street_fuzzyscore']]
        """
        table = pd.DataFrame(index=on_index)

        if on_cols is None:
            return table

        compared_cols = on_cols.copy()
        if type(compared_cols) == str:
            compared_cols = [compared_cols]
        assert isinstance(compared_cols, list)

        for c in compared_cols:
            assert isinstance(c, str)
            colname = c + suffix
            if pd.isnull(query[c]):
                table[colname] = None
            else:
                table[colname] = self.df.loc[on_index, c].apply(lambda r: func(r, query[c]))
        return table

    def compare_nofilter(self, query, on_index):
        """
        Calculate the score, without filtering
        Only advised in order to calculate a training table, when on_index is a limited scope of the data
        Args:
            query (pd.Series):
            on_index (pd.Index):

        Returns:
            pd.DataFrame
        """
        table_score_complete = self.filter_compare(query=query,
                                                   on_index=on_index,
                                                   return_filtered=False)
        return table_score_complete


def _unpack_scoredict(scoredict):
    """
    Calculate, from the scoredict, two lists:
    - the list of the names of columns on which the scoring is performeed
    - the list of the names of the scoring columns

    The names of the keys can be : 'all','any'
    - 'all','any': used only in the filter_all_any method
    - 'attributes':
    - 'fuzzy','token','exact','acronym': four kinds of comparison.
    Args:
        scoredict (dict): of the type {'fuzzy':['name','street'],'exact':['id'],'token':None}.\
        Should be of the form key:[list] or key:None.

    Returns:
        list,list : input_cols, output_cols
    Examples:
        _unpack_scoredict({'fuzzy':['name','street'],'exact':['id'],'token':None,'attributes':['name_len'],
        all=['id','id2']}):
        returns ['name','street','id','name_len','id2'],['name_fuzzyscore','street_fuzzyscore','id_exactscore','id2_exactscore','name_len_query','name_len_row']
    """

    outputcols = []
    inputcols = []

    for d in ['all', 'any']:
        if scoredict.get(d) is not None:
            for c in scoredict[d]:
                inputcols.append(c)
                outputcols.append(c + '_exactscore')
    if scoredict.get('attributes') is not None:
        for c in scoredict['attributes']:
            inputcols.append(c)
            outputcols.append(c + '_query')
            outputcols.append(c + '_row')
    for k in scorename.keys():
        if scoredict.get(k) is not None:
            for c in scoredict[k]:
                inputcols.append(c)
                outputcols.append(c + scorename[k])
    return inputcols, outputcols


def _checkdict(inputdict, mandatorykeys, existinginput=None):
    """
    Takes as in input a dictionnary, and re-format it in order to have all mandatory keys, and by filtering out the values
    already containted in the existing input
    Args:
        inputdict (dict): source dictionnary
        mandatorykeys (list): list of names
        existinginput (list): list of already existing names

    Returns:
        dict
    """
    mydict = {}
    if inputdict is None:
        for c in mandatorykeys:
            mydict[c] = None
    else:
        for c in mandatorykeys:
            if inputdict.get(c) is None:
                mydict[c] = None
            else:
                if existinginput is None:
                    mydict[c] = inputdict[c].copy()
                else:
                    mydict[c] = [v for v in inputdict[c] if v not in existinginput]
    return mydict


def calculatescoredict(used_cols, existing_cols=None):
    """
    From a set of existing comparison columns and columns needed for a decision function,
    calculate the scoring dict that is needed for the scorer to calculate all the needed columns.
    Args:
        existing_cols (list): list of existing columns that are already calculated.
        used_cols (list): list of columns needed for the decision function.

    Returns:
        dict: scoredict-type
    Examples:
        calculatescoredict(['name_fuzzyscore','id_exactscore'],existing_cols=['name_fuzzyscore'])
        returns {'exact':['id']}

        calculatescoredict(['name_fuzzyscore'])
        returns {'fuzzy':['name']}
    """
    if existing_cols is None:
        existing_cols = []

    x_col = list(filter(lambda x: x not in existing_cols, used_cols))
    m_dic = {}

    def _findscoreinfo(colname):
        if colname.endswith('_row') or colname.endswith('_query'):
            k = 'attributes'
            u = nm.rmv_end_str(colname, '_row')
            return k, u
        elif colname.endswith('score'):
            u = nm.rmv_end_str(colname, 'score')
            for k in ['fuzzy', 'token', 'exact', 'acronym']:
                if u.endswith('_' + k):
                    u = nm.rmv_end_str(u, '_' + k)
                    return k, u
        else:
            return None

    for c in x_col:
        result = _findscoreinfo(c)
        if result is not None:
            method, column = result[0], result[1]
            if m_dic.get(method) is None:
                m_dic[method] = [column]
            else:
                m_dic[method] = list(set(m_dic[method] + [column]))
    if len(m_dic) > 0:
        return m_dic
    else:
        return None


class FuncEvaluationModel:
    """
    This evaluation model applies a hard-coded evaluation function to return a probability vector
    Examples:
        decisionfunc = lambda r:r[id_cols].mean()
        dm = FuncEvaluationModel(used_cols=id_cols,eval_func=decisionfunc)
        x_score = compare(query,target_records)
        y_proba = dm.predict_proba(x_score)
    """

    def __init__(self, used_cols, eval_func):
        """
        Create the model
        Args:
            used_cols (list): list of columns necessary for decision
            eval_func (func): evaluation function to be applied. must return a probability vector
        """
        self.used_cols = used_cols
        self.eval_func = eval_func
        pass

    def fit(self):
        """
        pass
        Returns:
            None
        """
        pass

    @classmethod
    def from_dict(cls, thresholds):
        # TODO: how to initiate that function from a dict like a scoredict
        """
        Args:
            thresholds (dict):

        Returns:
            FuncEvaluationModel
        """

    def predict_proba(self, x_score):
        """
        This is the evaluation function.
        It takes as input a DataFrame with each row being the similarity score between the query and the target records.
        It returns a series with the probability vector that the target records is the same as the query.
        The scoring tables column names must fit the columns used for the model
        If x_score is None or has no rows it returns None.
        Args:
            x_score (pd.DataFrame):the table containing the scoring records

        Returns:
            pd.Series : the probability vector of the target records being the same as the query
        """
        missing_cols = list(filter(lambda x: x not in x_score.columns, self.used_cols))
        if len(missing_cols) > 0:
            raise KeyError('not all training columns are found in the output of the scorer:', missing_cols)
        x_score = x_score[self.used_cols]

        y_proba = x_score.apply(lambda r: self.eval_func(r), axis=1)
        y_proba.name = 1

        return y_proba


class TrainerModel:
    def __init__(self, scoredict):
        """
        Create the model
        used_cols (list): list of columns necessary for decision
        eval_func (func): evaluation function to be applied. must return a probability vector
        Args:
            scoredict (dict): {'fuzzy':['name','street'],'token':['name_wostopwords'],'acronym':None}
        """
        self.scoredict = scoredict
        compared_cols, used_cols = _unpack_scoredict(scoredict)
        self.used_cols = used_cols
        self.compared_cols = compared_cols
        pass


class MLEvaluationModel:
    """
    The evaluation model is based on machine learning, it is an implementation of the Random Forest algorithm.
    It requires to be fitted on a training table before making decision.

    Examples:
        dm = MLEvaluationModel()
        x_train,y_train=dm.load_training_data('mytrainingdata.csv',targetcol='ismatch')
        dm.fit(x_train,y_train)
        x_score = compare(query,target_records) where compare creates a similarity table
        y_proba = dm.predict_proba(x_score)
    """

    def __init__(self, verbose=True,
                 n_estimators=2000, model=None):
        """
        Create the model
        Args:
            verbose (bool): control print output
            n_estimators (int): number of estimators for the Random Forest Algorithm
            model: sklearn classifier model, default RandomForrest
        """
        self.verbose = verbose
        if model is None:
            self.model = RandomForestClassifier(n_estimators=n_estimators)
        else:
            self.model = model
        self.used_cols = []

        pass

    def fit(self, X, y):
        """
        fit the machine learning evaluation model on the provided data set.
        It takes as input a training table with numeric values calculated from previous examples.
        Args:
            X (pd.DataFrame): pandas DataFrame containing annotated data
            y (pd.Series):name of the target vector in the training_set

        Returns:
            None

        """

        self.used_cols = X.columns

        start = pd.datetime.now()

        if self.verbose:
            print('shape of training table ', X.shape)
            print('number of positives in table', y.sum())

        # fit the evaluationmodel
        self.model.fit(X, y)

        if self.verbose:
            # show precision and recall score of the evaluationmodel on training data
            y_pred = self.model.predict(X)
            precision = precision_score(y_true=y, y_pred=y_pred)
            recall = recall_score(y_true=y, y_pred=y_pred)
            print('precision score on training data:', precision)
            print('recall score on training data:', recall)

        if self.verbose:
            end = pd.datetime.now()
            duration = (end - start).total_seconds()
            print('time elapsed', duration, 'seconds')

        return None

    def predict_proba(self, x_score):
        """
        This is the evaluation function.
        It takes as input a DataFrame with each row being the similarity score between the query and the target records.
        It returns a series with the probability vector that the target records is the same as the query.
        The scoring table must not have na values.
        The scoring tables column names must fit the training table column names. (accessible via self.decisioncols).
        If x_score is None or has no rows it returns None.
        Args:
            x_score (pd.DataFrame): the table containing the scoring records

        Returns:
            pd.Series : the probability vector of the target records being the same as the query

        """
        if x_score is None or x_score.shape[0] == 0:
            return None
        else:
            missing_cols = list(filter(lambda x: x not in x_score.columns, self.used_cols))
            if len(missing_cols) > 0:
                raise KeyError('not all training columns are found in the output of the scorer:', missing_cols)

            # re-arrange the column order
            x_score = x_score[self.used_cols]

            # launch prediction using the predict_proba of the scikit-learn module
            y_proba = \
                pd.DataFrame(self.model.predict_proba(x_score), index=x_score.index)[1]
            assert isinstance(y_proba, pd.Series)
            return y_proba

# Thank you