import json
import pymysql
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def save_to_rds(item):
    rds_host = "krz-ml-mba-test-1.c30a8z23goab.us-east-1.rds.amazonaws.com"
    name = "admin"
    password = "bernardGerard"
    db_name = "pokemon_database"

    try:
        logger.info('Connecting')
        conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
        logger.info('Connected')
    except pymysql.MySQLError as e:
        logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
        logger.error(e)
        sys.exit()

    logger.info('Saving Passenger Data')
    with conn.cursor() as cur:
        condition = ("id" in item) and \
                        ("name" in item) and \
                        ("past_types" in item) and \
                        ("height" in item) and \
                        ("weight" in item) and \
                        ("moves" in item)
        if condition:
            try:
                sql = f'''insert into pokemon (id, name, past_types, height, weight, moves) values ({item['id']}, "{item['name']}", "{item['past_types']}", "{item['height']}", "{item['weight']}", "{item['moves']}")'''
                cur.execute(sql)
                conn.commit()
                logger.info('Data saved')
            except pymysql.MySQLError as e:
                logger.error("Error: Could not save item in database")
                logger.error(e)
                # So we can let the trigger automatically delete the SQS event
                logger.info("skipping")
                # sys.exit()
            except IndexError as e:
                logger.error("Error: Index error")
                logger.error(e)
                # So we can let the trigger automatically delete the SQS event
                logger.info("skipping")

        else:
            # Outputting a more useful message than if catching exception
            # Parsing exception
            logger.info('Item not in required format')
            logger.info(item)
    # conn.commit()
    return 'SUCCESS'


def lambda_handler(event, context):
    for record in event['Records']:
        payload = None
        try:
            # trying to parse json
            payload = json.loads(record["body"])
        except ValueError:
            logger.error('Could not parse json')
            logger.error(record)
        if payload is not None:
            # parsining did succeed
            # next step is trying to save in database
            save_to_rds(payload)
        return 'SUCCESS'
