import json
import time
from datetime import datetime

import configargparse
from dateutil.tz import tzlocal

from utility.api_manager import manager

p = configargparse.ArgParser(default_config_files=['settings.conf'])
p.add('--mail', required=True)
p.add('--pw', required=True)
p.add('--league', required=False)
p.add('--start', required=False)
p.add('--ignore', required=False, action='append', default=[])

options = p.parse_args()


def main():
    start = time.time()

    manager.init(options)
    manager.get_bonus()
    print(f'Bonus collected')
    print(f'Total execution time: {round(time.time() - start, 2)}s')


if __name__ == '__main__':
    main()
