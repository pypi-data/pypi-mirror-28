# module to receive a ticket name or pair and convert it in a standard format
# author: Rafael Esteban Ceron Espinosa, restebance@gmail.com
import yaml
import pkg_resources

def get_product_standard(pair_tick_value, exchange_name=None):
    normalized_exchange_name = exchange_name.upper() if exchange_name else 'TICK'
    normalized_pair_tick_value = pair_tick_value.upper()
    #
    resource_package = 'cryptotranslator'  # Could be any module/package name
    # resource_path = '/'.join(('templates', 'temp_file'))  # Do not use os.path.join(), see below
    resource_path = 'info.yaml'
    stream = pkg_resources.resource_stream(resource_package, resource_path)
    try:
        exchanges_info = yaml.load(stream)
        if normalized_exchange_name in exchanges_info.keys():
            if normalized_pair_tick_value in exchanges_info[normalized_exchange_name].keys():
                return exchanges_info[normalized_exchange_name][normalized_pair_tick_value]
            else:
                return None
        else:
            return None
    except yaml.YAMLError as exc:
        print('Error reading yaml file: %s' % exc)
        raise
