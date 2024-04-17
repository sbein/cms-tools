import sys
import os

sys.path.append(os.path.expandvars("$CMSSW_BASE/src/cms-tools/lib"))

from plot_params_base import *
from plot_params_bg import *
from plot_params_jpsi import *
from plot_params_leptons import *
from plot_params_analysis_categories import *
from plot_params_jet_isolation import *
from plot_params_track_bdt import *
from plot_params_dilepton_bdt import *
#from plot_params_isocr import *
from plot_params_bg_validation import *
from plot_params_data_control_regions import *
from plot_params_signal import *
from plot_params_dqa import *
from plot_params_unblinded import *
from plot_params_isocr_wzto3 import *

default_params = track_selection