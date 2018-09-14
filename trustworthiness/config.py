import datetime
import os
import sys
from configparser import SafeConfigParser, ConfigParser
import pkg_resources
import logging

from trustworthiness.definitions import OUTPUT_FOLDER


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DeFactoConfig(object):
    __metaclass__ = Singleton

    def set_logger(self, log_file, file_level=logging.DEBUG, console_level=logging.INFO):

        formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        fileHandler = logging.FileHandler(log_file)
        fileHandler.setFormatter(formatter)
        fileHandler.setLevel(file_level)

        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(formatter)
        consoleHandler.setLevel(console_level)

        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(fileHandler)
        self.logger.addHandler(consoleHandler)
        self.logger.propagate = False

    def __init__(self):
        fine = False
        config = None
        self.logger = logging.getLogger('defacto')
        for ini_file in os.curdir, os.path.expanduser("~"), "/etc/defacto", os.environ.get('DEFACTO_CONF'), '/':
            try:
                self.version = "3.0.1"
                self.version_label = "DeFacto 3.0.1"
                with open(os.path.join(ini_file, "defacto.ini")) as source:

                    parser = ConfigParser()
                    parser.read(source.name)
                    self.root_dir = os.path.dirname(os.path.abspath(__file__)) + '/'
                    self.root_dir_data = self.root_dir + 'data/'
                    #self.log_level = parser.get('conf', 'log_level')

                    # absolute path
                    self.database = parser.get('database', 'path')
                    self.datasets_ext = parser.get('dataset_external_path', 'path')
                    self.datasets = self.root_dir_data + parser.get('dir', 'datasets')
                    #self.dir_output = self.root_dir_data + parser.get('dir', 'output')
                    self.dir_output = OUTPUT_FOLDER
                    self.dir_models = self.root_dir_data + parser.get('dir', 'models')
                    self.dir_encoders = self.root_dir_data + parser.get('dir', 'encoders')
                    self.dir_log = self.root_dir_data + 'log/'


                    # encoders and models
                    self.enc_domain = self.dir_encoders + parser.get('encoders', 'enc_webdomain')
                    self.model_credibility = self.dir_models + parser.get('models', 'clf_credibility')

                    # external datasets
                    self.dataset_ext_spam = self.datasets_ext + parser.get('dataset_external_path', 'spam_kaggle')
                    self.dataset_ext_uci_news = self.datasets_ext + parser.get('dataset_external_path', 'uci_news')
                    self.dataset_ext_microsoft_webcred_webpages_cache = self.datasets_ext + parser.get('dataset_external_path',
                                                                                               'microsoft_webcred_webpages_cached')
                    self.dataset_ext_microsoft_webcred_webpages_cache_missing = self.datasets_ext + parser.get('dataset_external_path',
                                                                                                       'microsoft_webcred_webpages_missing')
                    self.dataset_ext_bbc_folder = self.datasets_ext + parser.get('dataset_external_path', 'bbc_folder')

                    # internal datasets
                    self.dataset_microsoft_webcred = self.datasets + parser.get('dataset', 'microsoft_webcred')

                    # relative path
                    #models_rootdir = pkg_resources.resource_filename('resources', 'models') + "/"

                    # configurations
                    self.nr_threads_feature_extractor = parser.get('defacto', 'number_threads_feature_extractor')
                    self.search_engine_api = parser.get('search-engine', 'api')
                    self.search_engine_key = parser.get('search-engine', 'key')
                    self.search_engine_tot_resources = parser.get('search-engine', 'tot_resources')
                    self.open_page_rank_api = parser.get('search-engine', 'open_pagerank_api')

                    self.translation_id = parser.get('translation', 'microsoft_client_id')
                    self.translation_secret = parser.get('translation', 'microsoft_client_secret')

                    self.wot_key = parser.get('wot', 'key')
                    self.waybackmachine_tot = parser.get('waybackmachine', 'tot_archive_lookup')
                    self.waybackmachine_weight = parser.get('waybackmachine', 'weight_domain')

                    fine = True

                    break
                    #config.readfp(source)
            except IOError:
                pass

        if fine is False:
            raise ValueError('error on trying to read the conf file (defacto.conf)! Please set DEFACTO_CONF with its '
                             'path or place it at your home dir')
        else:
            if len(self.logger.handlers) == 0:
                # first file logger (can add more..)
                now = datetime.datetime.now()
                self.set_logger(self.dir_log + 'defacto_' + now.strftime("%Y-%m-%d") + '.log')

        #ini_file = pkg_resources.resource_filename('resource', "horus.conf")
        #rootdir = os.getcwd()
        #

    @staticmethod
    def get_report():
        return 'to be implemented'