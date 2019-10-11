import os
import sys
src_dir = os.path.join(os.getcwd(), '..', '03-src')
sys.path.append(src_dir)
import decisions_functions as hmd



decision = hmd.Decision()
decision.build_decision()
decision.print_results()
