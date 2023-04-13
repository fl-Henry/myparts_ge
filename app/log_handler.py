import os
import sys
import datetime
import logging
import logging.handlers
import configparser


class LogHandler:

    def __init__(self, config_file, name=__name__):
        self._name = name
        self.logger = logging.getLogger(self._name)
        print(type(self.logger))

        if os.path.exists(config_file):
            self.load_config(config_file)
        else:
            print("[Warning]: Config_file doesn't exist")
            sys.exit(1)

    def init_logger(self, date_fmt, log_level, log_dir, name):

        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % log_level)

        try:
            now = datetime.datetime.now()
            self.logger.setLevel(numeric_level)
            rfh = logging.handlers.TimedRotatingFileHandler(
                filename=f"{log_dir}/{name}.log",
                when='H',
                interval=4,
                backupCount=6
            )

            fmtr = logging.Formatter(
                '%(asctime)s [%(levelname)s] %(message)s',
                datefmt=date_fmt
            )

            rfh.setFormatter(fmtr)
            self.logger.addHandler(rfh)

        except Exception as e:
            print("Failed to initialize logger (", str(e), ")")
            sys.exit(1)

        self.logger.info("Logger has been initialized!")

    def load_config(self, file):
        print("Loading config file [", file, "]")

        # check config file
        try:
            with open(file):
                pass
        except Exception as e:
            print("Failed to open config file [", file, "]")
            print(str(e))
            sys.exit(1)

        config = configparser.ConfigParser()
        config.read(file)

        # check and/or create data directory
        data_dir = config.get('LOG', 'DATA_DIR')
        if not os.path.exists(data_dir):
            print("Creating directory [", data_dir, "]")
            os.mkdir(data_dir)

        # check log directory
        log_dir = config.get('LOG', 'LOG_DIR')
        if not os.path.exists(log_dir):
            print("Creating directory [", log_dir, "]")
            os.mkdir(log_dir)

        # initialization of logger
        self.init_logger(
            config.get('LOG', 'LOG_DATE_FMT'),
            config.get('LOG', 'LOG_LEVEL'),
            config.get('LOG', 'LOG_DIR'),
            config.get('LOG', 'LOG_FILE_PREFIX')
        )

        self.logger.debug("Displaying config values!")
        for section_name in config.sections():
            self.logger.debug("[SECTION]: %s", section_name)
            self.logger.debug("  Options: %s", config.options(section_name))
            for name, value in config.items(section_name):
                self.logger.debug("    %s = %s", name, value)

        self.logger.info("Config file [%s] has been loaded!", file)


if __name__ == '__main__':
    log = LogHandler('log_handler_01', config_file='main.cfg')
    log.logger.info('Logger is ready for work!')
