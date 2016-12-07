import sys, os
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_news               # interacting with Google ads and Ad Settings
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.politics.txt'
site_file_politics = 'politics.txt'

def make_browser(unit_id, treatment_id):
    b = web.google_news.GoogleNewsUnit(browser='chrome', log_file=log_file, unit_id=unit_id,
        treatment_id=treatment_id, headless=False, proxy=None, keyword_filename='keywords.txt')
    return b

web.pre_experiment.alexa.collect_sites(make_browser, num_sites=15, output_file=site_file_politics,
    alexa_link="http://www.alexa.com/topsites/category/Top/Society/Politics/Nationalism")


# Control Group treatment
def control_treatment(unit):
    pass


# Experimental Group treatment
def exp_treatment(unit):
    unit.visit_sites(site_file_politics)
    # unit.read_articles(count=5, agency='CNN', category='Elections', time_on_site=5)


# Measurement - Collects ads
def measurement(unit):
    unit.collect_ads(reloads=10, delay=5, site='bbc')


# Shuts down the browser once we are done with it.
def cleanup_browser(unit):
    unit.quit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# Load results reads the log_file, and creates feature vectors
def load_results():
    collection, names = converter.reader.read_log(log_file)
    return converter.reader.get_feature_vectors(collection, feat_choice='ads')

# If you choose to perform ML, then test_stat is redundant. By default, correctly_classified is used,
# If not, then you can choose something, and that will be used to perform the analysis. 

def test_stat(observed_values, unit_assignments):
    return analysis.statistics.difference(observed_values, unit_assignments)


adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=14, num_units=2, timeout=2000,
                        log_file=log_file,
                        treatment_names=["control ()", "experimental (politics)"])