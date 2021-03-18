import time

from typing import Union

from flask import current_app
from celery import Celery
from celery.utils.log import get_task_logger

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .__main__ import celery
from . import models


logger = get_task_logger(__name__)

# CONSTANTS FOR THE SCRAPER
URL = f"https://pulse.strukton.com/comfortsensor/"
WAIT_TIME = 5  # secconds

# Bind the tasks, so that it can trigger it's own retry based on the problem encoutnered
@celery.task(bind=True)
def update_sensor(self, uuid: str):

    sensor_url = f"{URL}{uuid}"

    # TODO: Handle WebDriverException for connection errors and stuff
    # When WebDriverException retry with quite some delay
    driver = webdriver.Remote(
        desired_capabilities=webdriver.DesiredCapabilities.CHROME,
        command_executor=current_app.config["WEBDRIVER_URL"],
    )

    logger.debug("Connected to the webdriver")

    # Get the URL - Load the page
    logger.debug(f"Getting url: {sensor_url}")
    driver.get(sensor_url)
    # Sleep to allow page load (and svg fetching on the page)
    time.sleep(WAIT_TIME)

    onload_value = ""

    try:
        # Find the first iframe on the page
        ifame_elem = driver.find_elements_by_tag_name("iframe")[0]
        # Switch the driver to that iframe
        driver.switch_to.frame(ifame_elem)
        # Get the body elements
        body_elem = driver.find_elements_by_tag_name("body")[0]
        # The `onload` attribute contains the value that needs to be parsed
        onload_value = body_elem.get_attribute("onload")
    except NoSuchElementException as e:
        logger.warning("Could not find the iframe that contains the data.")
        logger.info("Retryin in 1minute")
        # Wait a minute before retrying
        raise self.retry(exc=e, countdown=60)

    # Close the connection to the webdriver
    logger.debug("Closing connection to the webdriver")
    driver.quit()

    logger.debug(f"Onload value: {onload_value}")

    temp = None
    hum = None
    aq = None

    # Parse the onload value into the arguments when not empty
    if len(onload_value) > 0:
        onload_args = onload_value.split(",")
        logger.debug(f"Onload args: {onload_args}")
        # Extract the values

        if len(onload_args) < 1:
            # The onload value was retreived, but was empty
            # So the sensor probably does not have any data
            # Retry should wait quite some time (5min)
            raise self.retry(countdown=60 * 5)

        # The temperature is the 3th element in the onload_args array
        # The first and last character are quotation marks, so these need to
        # be removed
        temp = int(onload_args[3][1:-1])

        # The humidity value is the 5th element in the onload_args array
        # The first and last character are quotation marks, so these need to
        # be removed
        hum = int(onload_args[5][1:-1])
        # The air quality value is the 7th element in the onload_args array
        # The first and last character are quotation marks, so these need to
        # be removed and there is alse a ) at the end.
        aq = int(onload_args[7][1:-2])
    else:
        # The onload value was retreived, but was empty
        # So the sensor probably does not have any data
        # Retry should wait quite some time (5min)
        raise self.retry(countdown=60 * 5)

    # Save the values to the database
    sensor_res = current_app.session.query(models.Sensor).filter(
        models.Sensor.uuid == uuid
    )
    sensor: Union[models.Sensor, None] = sensor_res.first()
    if sensor is None:
        return {
            "error": f"Could not update sensor with uuid: {uuid}",
            "uuid": uuid,
            "temperature": temp,
            "humidity": hum,
            "air_quality": aq,
        }

    new_temp = models.Temperature(value=temp, sensor=sensor)
    new_hum = models.Humidity(value=hum, sensor=sensor)
    new_aq = models.AirQuality(value=aq, sensor=sensor)

    current_app.session.add_all([new_temp, new_hum, new_aq])
    current_app.session.commit()

    return {
        "uuid": uuid,
        "temperature": temp,
        "humidity": hum,
        "air_quality": aq,
    }


@celery.task
def update_all_sensors():
    logger.info("Updating all sensors...")
    all_sensors = current_app.session.query(models.Sensor).all()

    for sensor in all_sensors:
        logger.info(f"Added sensor {sensor.uuid} to queue")
        update_sensor.delay(sensor.uuid)
