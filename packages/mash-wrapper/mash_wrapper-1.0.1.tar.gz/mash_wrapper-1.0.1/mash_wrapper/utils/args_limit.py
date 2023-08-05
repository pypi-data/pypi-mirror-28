import argparse

def required_length(nmin,nmax):
    '''Function to limit args

    Function to control the maximum and minimum number of arguments passed to a
    given argparser args

    Parameters
    ----------
    nmin: int
        minimum number of arguments that a given option must have
    nmax: int
        maximum number of arguments that a given option must have

    Returns
    -------
    RequiredLength: argparse.Action
    '''
    class RequiredLength(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
            if not nmin<=len(values)<=nmax:
                msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
                    f=self.dest,nmin=nmin,nmax=nmax)
                raise argparse.ArgumentTypeError(msg)
            setattr(args, self.dest, values)
    return RequiredLength