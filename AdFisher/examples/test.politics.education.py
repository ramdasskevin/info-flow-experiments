import sys
sys.path.append("../core")          # files from the core 
import adfisher                     # adfisher wrapper function
import web.pre_experiment.alexa     # collecting top sites from alexa
import web.google_ads               # interacting with Google ads and Ad Settings
import converter.reader             # read log and create feature vectors
import analysis.statistics          # statistics for significance testing

log_file = 'log.politics.education.txt'
site_file_education = 'education.txt'
site_file_hilary = 'hilary.txt'
site_file_trump = 'trump.txt'

def make_browser(unit_id, treatment_id):
    b = web.google_ads.GoogleAdsUnit(browser='firefox', log_file=log_file, unit_id=unit_id, 
        treatment_id=treatment_id, headless=True, proxy = None)
    return b

# Control Group treatment
def control_treatment(unit):
    unit.visit_sites(site_file_hilary)
    unit.read articles(count=5, agency=‘CNN’, keyword='hilary', category='Politics', time on site=10)
    unit.visit_sites(site_file_education)

# Experimental Group treatment
def exp_treatment(unit):
    unit.visit_sites(site_file_trump)
    unit.read articles(count=5, agency=‘CNN’, keyword='trump', category='Politics', time on site=10)
    unit.visit_sites(site_file_education)



# Measurement - Collects ads
def measurement(unit):
    unit.collect_ads(reloads=10, delay=5, site='bbc')
    unit.get_interests()


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
#   return statistics.correctly_classified(observed_values, unit_assignments)

web.pre_experiment.alexa.collect_sites(make_browser, num_sites=50, output_file=site_file_education,
    alexa_link="http://www.alexa.com/topsites/category/Top/Arts/Education")

adfisher.do_experiment(make_unit=make_browser, treatments=[control_treatment, exp_treatment], 
                        measurement=measurement, end_unit=cleanup_browser,
                        load_results=load_results, test_stat=test_stat, ml_analysis=True, 
                        num_blocks=13, num_units=2, timeout=2000,
                        log_file=log_file,
                        treatment_names=["control (hilary)", "experimental (trump)"])
