settings = {}
with open('config.info') as config_file:
    for parameter in config_file.readlines():
        parameter = parameter.strip()
        key, value = parameter.split(sep='=')
        try:
            value = int(value)
        except:
            try:
                value = float(value)
            finally:
                pass
        finally:
            settings[key] = value