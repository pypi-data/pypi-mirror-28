#!/usr/bin/env python

"""
Set of unit tests for the topicmodels package.
"""

import unittest
import topicmodels
import pandas as pd


class TestPreprocessing(unittest.TestCase):

    """
    set of tests that check that we  can read an 
    input file into a pandas dataframe, use it to create a RawDocs object,
    and that this can then remove stopwords and do stemming.
    """

    def setUp(self):

        """
        read a test txt file into a pandas dataframe, and create a RawDocs object from it.
        """

        data = pd.read_table("topicmodel_tests/testfiles/speech_data_extend.txt", encoding="utf-8")
        self.data = data[data.year >= 1947]
        self.docsobj = topicmodels.RawDocs(self.data.speech, "long")
        
    def test_read_input(self):

        """ 
        check the test file was read OK, and get a dataframe with 3 columns and >0 rows.
        """

        print("Testing reading input text file")
        num_rows = self.data.shape[0]
        num_columns = self.data.shape[1]
        self.assertTrue(num_rows > 0 and num_columns == 3)


    def test_create_rawdocs(self):

        """ 
        confirm that the original created RawDocs object has a non-zero list of token lists
        (there should be one per row in the input dataframe).
        """

        print("Testing creation of RawDocs object")
        self.assertTrue(len(self.docsobj.tokens) > 0)

    def test_remove_stopwords(self):

        """ 
        Check that the list of tokens after removing stopwords is smaller than the initial list
        """

        print("Testing removal of stopwords from the first token list")
        orig_length = len(self.docsobj.tokens[0])
        self.docsobj.token_clean(1)
        self.docsobj.stopword_remove("tokens")
        new_length = len(self.docsobj.tokens[0])
        self.assertTrue(orig_length > new_length)        

    def test_stemming(self):
        """ 
        Check that the list of tokens after removing stopwords is smaller than the initial list
        """

        print("Testing finding stems")        
        self.docsobj.token_clean(1)
        self.docsobj.stopword_remove("tokens")
        self.docsobj.stem()
        all_stems = [s for d in self.docsobj.stems for s in d]
        self.assertTrue(len(all_stems) > 0)


class TestLDAGibbsSampling(unittest.TestCase):

    """
    Test the Latent Dirichlet Allocation / Gibbs sampling. 
    """

    def setUp(self):
        
        """
        Do all the preprocessing steps above, but with a smaller subset of the data
        """

        data = pd.read_table("topicmodel_tests/testfiles/speech_data_extend.txt", encoding="utf-8")
        self.data = data[data.year >= 1997]
        self.docsobj = topicmodels.RawDocs(self.data.speech, "long")
        self.docsobj.token_clean(1)
        self.docsobj.stopword_remove("tokens")
        self.docsobj.stem()
        self.docsobj.stopword_remove("stems")
        self.docsobj.term_rank("stems")
        self.docsobj.rank_remove("tfidf", "stems", self.docsobj.tfidf_ranking[1000][1])
        self.all_stems = [s for d in self.docsobj.stems for s in d]
        ## now create
        self.ldaobj = topicmodels.LDA.LDAGibbs(self.docsobj.stems, 30)


    def test_LDA_param_alpha(self):

        """ 
        test the values of LDA params alpha and beta, which depend on the user-defined value of K.
        and the number of unique stems, respectively
        """

        print("Checking value of LDA params")
        self.assertEqual(self.ldaobj.alpha, 50. / self.ldaobj.K)

    def test_LDA_param_beta(self):

        """ 
        test the values of LDA params alpha and beta, which depend on the user-defined value of K.
        and the number of unique stems, respectively
        """

        self.assertEqual(self.ldaobj.beta, 200. / len(set(self.all_stems)))
        

    def test_topic_seed_shape(self):

        """ 
        topic_seed shold be a len(all_stems)-dimensinal vector of integers.
        """
        self.assertEqual(self.ldaobj.topic_seed.shape[0], len(self.all_stems))


    def test_sampling(self):

        """
        test that we can run 100 iterations of sampling without crashing
        """

        ### 0 burn-in, thinning interval of 10, 10 samples (=100 iterations total)
        self.ldaobj.sample(0,10,10)
        self.assertEqual(self.ldaobj.samples,10)
        
        
if __name__ == "__main__":
    unittest.main()
