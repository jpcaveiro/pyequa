# --------------------------
# mean_variance
# --------------------------

#
# Equations or generic relations
#
scenario_relations = {
    "Eq(mean,  (x1+x2+x3)/3 )",
    "Eq(variance, ( (x1-mean)**2 + (x2-mean)**2 + (x3-mean)**2 )/2 )",
    "Eq(cv,   sqrt(variance)/mean)",
}

#
# Variables: description of each variable controls the way they appear
# 
variable_attributes = {
    "x1":   {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
    "x2":   {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
    "x3":   {"type": "numerical", "tol": 0.05,  "givenvarlevel": 1},
    "mean": {"type": "numerical", "tol": 0.05,  "givenvarlevel": 2},
    "variance": {"type": "numerical", "tol": 0.05,  "givenvarlevel": 2},
    "cv":   {"type": "numerical", "tol": 0.05,  "givenvarlevel": 3},
}


from pyequa.config import PyEqua

pe = PyEqua("mean_variance", scenario_relations, variable_attributes)

#pe.scenario.draw_wisdom_graph()


#import cProfile

# Profile the function
#profiler = cProfile.Profile()
#profiler.enable()



# Learning from the same exercises for everybody
#pe.challenge_deterministic(max_combinations_givenvars_per_easynesslevel = 1, 
#                           number_of_problems_per_givenvars = 1)



# Learning using "moodle random questions" based in a similar level
#pe.challenge_with_randomquestions(max_combinations_givenvars_per_easynesslevel = 2)



# To make "moodle random questions" for evaluation 
#   (all questions with equal difficult but different values)
#pe.randomquestion_sameblanks(fill_in_blanks_vars = {'mean', 'variance', 'cv'}, 
#                             number_of_problems_per_givenvars=4)



# Teacher can read and choose
pe.exploratory() # is the same as


# Teacher can read and choose
#pe.hard_first(max_number_of_problems=None, 
#              max_combinations_givenvars_per_easynesslevel=2, 
#              number_of_problems_per_givenvars=1)


#profiler.disable()
#profiler.print_stats(sort='time')  # Sort by time spent

