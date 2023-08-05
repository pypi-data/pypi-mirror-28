import os


DEFAULT = "main"
BUNDLE_URL = "http://p065psqpy.bkt.clouddn.com/data_bundle.tar.gz"


def get(name=DEFAULT):
    paths = get_config_paths()

    if name in paths:
        return paths[name]
    else:
        if name == DEFAULT:
            raise KeyError("Main config path not set, "
                           "use command 'DataAPI add' and 'DataAPI use' to set main config to set main config path")
        else:
            raise KeyError("%s not in paths, "
                           "use command 'DataAPI add' to add config path" % name)


def get_root():
    root = os.environ.get("fxdayu", os.path.expanduser(os.path.join('~', '.fxdayu')))
    if not os.path.exists(root):
        os.makedirs(root)
    return root


def default_bundle_path():
    return os.path.join(get_root(), "bundle")


def config_paths_file():
    root = get_root()
    return os.path.join(root, 'DataAPIConfig.json')


def get_config_paths():
    import json

    try:
        return json.load(open(config_paths_file()))
    except IOError:
        return {}


def set_config_paths(paths):
    import json

    file_path = config_paths_file()
    json.dump(paths, open(file_path, 'w'))
