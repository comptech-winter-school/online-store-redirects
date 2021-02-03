import sys
sys.path.append('utils')
sys.path.append('pipeline')

from pipeline.negative_examples import make_negative_examples_from_searches

print(make_negative_examples_from_searches('resourses/420_searches.json'))
