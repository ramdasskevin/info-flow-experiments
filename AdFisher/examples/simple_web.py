# A simple experiment looking at how setting the gender bit at
# Google's Ad Settings page affects the gender that Google lists.
# This is contrived experiment since we know setting the gender will
# result in showing that gender, but it makes for a simple example.

# Load the parts of AdFisher we need.  The first import loads the
# basic functionality.  The second loads AdFisher's support for
# experimental units that are automated browsers.
import sys
sys.path.append("../code")
import core.adfisher as adfisher
import web.browser_unit as browser_unit

log_file = 'simple_web.log.txt'

# Creates a new unit by setting up an automated Firefox browser.
# BrowserUnit is a wrapper class for a browser driver that makes
# certain experiments involving Google's Ad Settings easy.  We first
# have the browser opt into Google tracking so that it has a gender
# bit to set.
def make_browser(unit_id):
    b = browser_unit.BrowserUnit('firefox', log_file, unit_id)
    b.opt_in()
    return b

# Sets the gender bit of Google's Ad Settings to female.
def set_female(unit, unit_id):
    unit.set_gender('f', 'control (female)')

# Sets the gender bit of Google's Ad Settings to male.
def set_male(unit, unit_id):
    unit.set_gender('m', 'experimental (male)')

# Measures Google's gender bit and prints it to the log using the same
# format as found in simple_test.py.
def measure_gender(unit, unit_id, treatment_id):
    with open(log_file, "a") as fo:
        fo.write('response: ' + 
                 str(unit_id) + ' ' + 
                 str(treatment_id) + ' ' + 
                 str(unit.get_gender()) + '\n')    


# Shuts down the browser once we are done with it.
def cleanup_browser(unit, unit_id, treatment_id):
    unit.driver.quit()


# Loads the recorded genders from the log file as in simple_test.py.
def load_results():
    observed_values = []
    observed_assignment = []
    with open(log_file, 'r') as fo:
        for line in fo:
            tokens = line.split()
            if tokens[0] == 'response:':
                unit_id = int(tokens[1])
                treatment_id = int(tokens[2])
                response_value = tokens[3]
                observed_values.append(response_value)
                observed_assignment.append(treatment_id)
    return observed_values, observed_assignment

# Counts up the number of times the second group (treatment id of 1)
# was measured as male.  Since we set the second group to be male,
# this number should be all of them.
def test_stat(observed_values, unit_assignment):
    value = 0
    for i in range(0,len(observed_values)):
        observed_num = 0
        if(observed_values[i] == 'Male'):
            observed_num = 1
        value +=  observed_num * unit_assignment[i]
    return value

adfisher.do_experiment(make_browser, [set_female, set_male], 
                       measure_gender, cleanup_browser, 
                       load_results, test_stat,
                       num_blocks=1, num_units=2, timeout=120,
                       log_file=log_file, 
                       treatment_names=["control (female)", "experimental (male)"])