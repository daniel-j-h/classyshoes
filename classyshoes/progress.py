from progress.bar import Bar


# Reports position in iterable and ETA
def mkProgress(description):
  return lambda iterable: Bar('{} %(index)d/%(max)d'.format(description), suffix='ETA: %(eta_td)ss').iter(iterable)


# Dummy pass-through
def mkNullProgress(description):
  return lambda iterable: iterable
