#
# Equations or generic relations
#
scenary_relations = {
    "Eq(zobs, qnorm(1-pvalue, 0, 1))",
    "Eq(reject, pvalue + alpha)",
    "Eq(lowergreater, pvalue + alpha)",
    "Eq(sig, pvalue + alpha)",
}


#
# Variables: description of each variable controls the way they appear
# 
variable_attributes = {
    'zobs': {'type': 'numerical', 'tol': 0.001, 'givenvarlevel': 1},
    'pvalue':  {'type': 'multichoice', 'givenvarlevel': 1},
    'alpha':   {'type': 'multichoice', 'givenvarlevel': 1},
    'reject': {'type': 'multichoice', 'givenvarlevel': 2},
    'lowergreater':  {'type': 'multichoice', 'givenvarlevel': 2},
    'sig':  {'type': 'multichoice', 'givenvarlevel': 3},
}

from pathlib import Path
from pyequa.config import PyEqua

pe = PyEqua(Path(__file__).parent, scenary_relations, variable_attributes)

# Teacher can read and choose
#pe.hard_first(max_number_of_problems=None, 
#              max_combinations_givenvars_per_easynesslevel=5, 
#              number_of_problems_per_givenvars=1)


# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
#pe.randomquestion_sameblanks(fill_in_blanks_vars = {'zobs', 'pvalue', 'reject', 'sig'}, 
#                             number_of_problems_per_givenvars=4)

r"""
        <text>Problem 008 (data row is 04) de 008 (lowergreater, sig, alpha)</text>
    </name>
    <questiontext format="html">
        <text><![CDATA[<p>Consider a right-tailed hypothesis test for the mean \(\mu\) of a Normal population with known variance:</p>
<p>H0: \(\mu = 5\) versus  H1: \(\mu > 5\)</p>
<p>Considering</p>
<ul>
<li>\(z_\text{obs}\) = {:NUMERICAL:},</li>
<li>p-value = {:MULTICHOICE_S:%0%0.001~%0%0.05~%0%0.01~%0%0.3} = \( P(Z \ge  z_\text{obs}) \),</li>
<li>\(\alpha\) = <strong>0.05</strong></li>
</ul>
<p>{:MULTICHOICE_S:%0%reject~%0%don't reject} the null hypothesis (H0) because p-value <strong>is greater</strong> than \(\alpha\).</p>
<p>The expected value (population mean), \(\mu\), <strong>is significative</strong> greater than 5.</p>]]></text>
    </questiontext>
"""

# Teacher can read and choose
pe.exploratory() 