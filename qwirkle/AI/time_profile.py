import cProfile
from qwirkle.AI.run_AI import main

#cProfile.run('main()', 'ai_multitile_stats')

import pstats

p = pstats.Stats('ai_multitile_stats')

p.sort_stats('tottime').print_stats(10)
#p.strip_dirs().sort_stats(-1).print_stats()