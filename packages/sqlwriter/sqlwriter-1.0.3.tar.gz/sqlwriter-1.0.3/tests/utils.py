import yaml


def get_config(prog=None):
    cfg_file = 'test_conf.yaml'

    with open(cfg_file, 'r') as f:
        config = yaml.load(f)

    if prog is None:
        return config

    try:
        return config[prog]
    except KeyError:
        print('No config found for {}. Exiting now.'.format(prog))
        sys.exit(1)
