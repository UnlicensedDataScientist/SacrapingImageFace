#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 17:13:40 2023

@author: jhonnyrv
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 11:50:55 2023

@author: jhonnyrv
"""

import logging
import psutil
import colorlog
from selenium.webdriver.remote.remote_connection import LOGGER

logging.basicConfig(filename='info.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuración del logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(message)s'))
logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# logging.debug('Este es un mensaje de debug')
# logging.info('Este es un mensaje de información')
# logging.warning('Este es un mensaje de advertencia')
# logging.error('Este es un mensaje de error')
# logging.critical('Este es un mensaje crítico')

