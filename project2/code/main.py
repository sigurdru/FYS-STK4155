import argparse
from analysis import analyse_NN, analyse_SGD
import numpy as np

# np.random.seed(2021)

def parse_args(args=None):
    """
    Uses argparse module to return an object containing
    all runtime arguments specified in command line
    """
    parser = argparse.ArgumentParser(
        description='Kort beskrivelse av hva vi gjør dette prosjektet',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    add_arg = parser.add_argument

    add_arg('-m', '--method',
            type=str,
            default='NN',
            choices=['reg', 'NN'],
            help='Choose which prediction method to use.',
            )

    add_arg("-tts",
            type=float,
            default=0.2,
            choices=[0.2, 0.25, 0.3, 0.4],
            help="Train/test split ratio"
            )

    add_arg('-p', '--polynomial',
            type=int,
            default=5,
            help='Polynomial degree.',
            )

    add_arg('-n', '--num_points',
            type=int,
            default=30,
            help='Number of gridpoints along 1 axis',
            )

    add_arg('-Ne', '--num_epochs',
            type=int,
            default=100,
            help='Number of epochs',
            )

    add_arg('-eta',
            type=str,
            default='0.1',
            help="""Desired learning rate, can be array or float.
            For example:
                    -eta 'np.linspace(0.001, 1, 100)'
                    -eta 'np.logspace(0.001, 1, 10)'
                    -eta 1
                    """,
            )

    add_arg('-ga', '--gamma',
            type=float,
            default=0,
            help='Desired momentum parameter'
            )

    add_arg('-bs', '--batch_size',
            type=int,
            default=30,
            help='Set size of minibatch'
            )

    add_arg('-s', '--scaling',
            type=str,
            default='S',
            choices=["None", 'M', 'S', 'N'],
            help='Scaling method: None, MinMax, Standard, Normalizer.',
            )

    add_arg("-e", "--epsilon",
            type=float,
            default=0.2,
            help="Scale value of noice for Franke Function",
            )

    add_arg('-l', '--lmb',
            type=str,
            default="0",
            help="""Lambda values for Ridge regression. Can be array or float.
            For example:
                 -l 'np.linspace(0.001, 1, 100'
                 -l 'np.logspace(0.001, 1, 10)'
                 -l 0.1
                 """,
            )

    add_arg("-d", "--dataset",
            type=str,
            default="Franke",
            choices=["Franke", "Cancer", "MNIST"],
            help="""Dataset to be used.
                    Franke is continous fitting,
                    Cancer is binary classification,
                    MNIST is multi-category classification""",
            )

    add_arg("-show",
            action="store_true",
            dest="show",
            )

    add_arg("-push",
            action="store_true",
            dest="push",
            )

    add_arg("-nosave",
            action="store_false",
            dest="save",
            )

    args = parser.parse_args(args)

    print("Runtime arguments:", args, "\n")

    # for dynamic etas
    exec('args.eta = ' + args.eta)
    if np.shape(args.eta) == ():
        args.eta = [args.eta, ]

    exec('args.lmb = ' + args.lmb)
    if np.shape(args.lmb) == ():
        args.lmb = [args.lmb, ]

    return args


def main():
    args = parse_args()
    analyse_NN(args)


if __name__ == "__main__":
    main()
