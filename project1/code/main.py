import utils
from analysis import bias_var_tradeoff, tmp_func_name

utils.np.random.seed(136)


def main():
    args = utils.parse_args()
    if args.resampling == "None":
        tmp_func_name(args)
    else:
        bias_var_tradeoff(args)

if __name__ == "__main__":
    main()
