import logging

LOGGER = logging.getLogger("report_llm_agent")
LOGGER.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

ch.setFormatter(formatter)
LOGGER.addHandler(ch)