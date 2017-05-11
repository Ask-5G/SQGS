import sys
import os
import django
import unirest
import json
import logging
import time
from django.core.wsgi import get_wsgi_application
from logging.config import dictConfig

# Django setup env

sys.path.append("/home/linuxuser/TAFE/tafe-sqgs/api/src")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqgs.settings")
application = get_wsgi_application()
django.setup()

# Models import

from basemodel.models import *
from checkpoints.models import *
from inspection.models import *
from organization.models import *
from reports.models import *
from threshold.models import *
from basemodel.serializers import *
from checkpoints.serializers import *
from inspection.serializers import *
from organization.serializers import *
from reports.serializers import *
from threshold.serializers import *

from datetime import datetime


# defult values
DEFAULT_SLEEP_TIME = 60  # 4 minutes
BASE_URL = "http://192.168.1.47:8001/"
unirest.default_header('Device', 'Type hub')
unirest.timeout(5000)
TOKEN_KEY = ""
ERR_MSG = 'ERROR : %s \nLINE NUMBER : %s'
model = None
ordered_model_items = ['Supplier', 'Part',
                       'ControlPlan', 'Process', 'Characteristics',
                       'StagingServer', 'Users', 'Employee', 'Shift',
                       'Equipment']


def setup_logging(
    default_path='/home/linuxuser/HUB_API/dqms/logging.json',
    default_level=logging.DEBUG,
    env_key='LOG_CFG'
):
    """
        Setup logging configuration
    """
    try:
        path = default_path
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(path):
            with open(path, 'rt') as f:
                config = json.load(f)
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def login():
    try:
        global TOKEN_KEY
        data = {'hardware_id': HARDWARE_ID}
        logger.info(BASE_URL + "login/")
        response = unirest.post(BASE_URL + "login/",
                                headers={"Accept": "application/json"},
                                params=data)
        if response.code == 200:
            TOKEN_KEY = response.body['key']
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def get(url, data=None):
    try:
        if url is not None:
            if data is None:
                response = unirest.get(BASE_URL + url,
                                       headers={"Key":
                                                "Token " + TOKEN_KEY})
            else:
                response = unirest.get(BASE_URL + url,
                                       headers={"Key":
                                                "Token " + TOKEN_KEY,
                                                "Content-Type":
                                                "application/json"},
                                       params=json.loads(data))
            if response.code == 200 or response.code == 201:
                logger.info(BASE_URL +
                            url + ":" + str(response.body))
                return response.body
            if response.code == 401 and \
                    response.body['detail'] == "Token has expired.":
                logger.error(BASE_URL +
                             url + ":" + str(response.body))
                login()
                if data is None:
                    response = unirest.get(BASE_URL + url,
                                           headers={"Key":
                                                    "Token " + TOKEN_KEY})
                else:
                    response = unirest.get(BASE_URL + url,
                                           headers={"Key":
                                                    "Token " + TOKEN_KEY,
                                                    "Content-Type":
                                                    "application/json"},
                                           params=data)
                logger.info(BASE_URL +
                            url + ":" + str(response.body))

                return response.body
            if response.code == 401:
                logging.error(response.body['detail'])
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def post(url, data):
    try:
        logger.info("Requesting URL:" + BASE_URL + url)
        response = unirest.post(BASE_URL + url,
                                headers={"Key":
                                         "Token " + TOKEN_KEY,
                                         "Content-Type": "application/json"},
                                params=data)
        if response.code == 200 or response.code == 201:
            logger.info(BASE_URL +
                        url + ": Data" + data + ":" + str(response.body))
            return response

        if response.code == 401 and\
                response.body['detail'] == "Token has expired.":
            logger.error(BASE_URL +
                         url + ":" + str(response.body))
            login()
            response = unirest.post(BASE_URL + url,
                                    headers={"Key":
                                             "Token " + TOKEN_KEY,
                                             "Content-Type":
                                             "application/json"},
                                    params=data)
            logger.info(BASE_URL +
                        url + ": Data" + data + ":" + str(response.body))

            return response
        if response.code == 400:
            return response
        else:
            logger.error(BASE_URL +
                         url + ": Data" + data + ":" + str(response.body))

    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def save(data=None, model=None, serializer=None):
    try:
        if (data is None or model is None or serializer is None):
            logger.error("Invalid save data.")
            return
        try:
            obejct = model.objects.get(pk=data['id'])
        except model.DoesNotExist:
            obejct = None
        if obejct is not None:
            serializer_data = serializer(obejct, data=data)
        else:
            serializer_data = serializer(data=data)
        if serializer_data.is_valid(raise_exception=True):
            serializer_data.save()
            return serializer_data.data
        else:
            logger.error(serializer_data)
            return
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def dict_to_object(dict_object):
    try:
        if dict_object:
            for key, item in dict_object.iteritems():
                model_class = eval(item[0])
                serializer_class = eval(item[2])
                del item[0]
                del item[1]
                item.append(model_class)
                item.append(serializer_class)
        return dict_object
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def get_model_config(default_path="/home/linuxuser/HUB_API/dqms/model_config.json"):
    try:
        global model
        path = default_path
        if os.path.exists(path):
            with open(path, 'rt') as f:
                model = json.load(f, object_hook=dict_to_object)
                return model
        else:
            logger.error("Initial JSON file is not exists in the path")
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def load_data(model_item=ordered_model_items):
    try:
        global model
        if model is None:
            model = get_model_config()
        for count, item in enumerate(model_item):
            print item
            if item == "Employee":
                users = Users.objects.all()
                for user in users:
                    response = get(model[item][0] + str(user.id))
                    for data in response[model[item][1]]:
                        save(data,
                             model[item][2], model[item][3])
            else:
                response = get(model[item][0])
                if len(model[item]) == 4:
                    for data in response[model[item][1]]:
                        save(data,
                             model[item][2], model[item][3])
                else:
                    save(response, model[item][1], model[item][2])

    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)

def load_device_data():
        logger.info(BASE_URL + "device/")
        try:
            last_updated = UpdatedTables.objects.get(name = "Device")
            serializer = UpdatedTablesSerializer(last_updated, many=False)
            data = {"last_updated":last_updated.last_modified_date}
        except UpdatedTables.DoesNotExist:
            data = {"last_updated": ""}
        response = unirest.get(BASE_URL + "device/",
                                headers={"Key":"Token " + TOKEN_KEY},
                                params = data)
        device_create_or_update(response.body)


        

def device_create_or_update(data):
    print data
    for device in data["Device"]:
        try:
            device = Device.objects.get(id = device['id'])
            Device.objects.filter(id= device['id']).update(name=device['name'], calibration_count=device['calibration_count'],\
                device_id=device['device_id'], duration_in_days=device['duration_in_days'],\
                last_modified_date=device['last_modified_date'], \
                is_active = device['is_active'], \
                stagingserver_id = device['stagingserver'])
            write_updates(device)
            logger.info("Device Updated")
        except Device.DoesNotExist:
            Device.objects.create(name=device['name'], calibration_count=device['calibration_count'],\
                device_id=device['device_id'], duration_in_days=device['duration_in_days'],\
                last_modified_date=device['last_modified_date'], \
                is_active = device['is_active'], id = device['id'], \
                stagingserver_id = device['stagingserver'])
            write_updates(device)
            logger.info("Device Created")
       
def write_updates(device):
    print "write updates"
    stagingserver = StagingServer.objects.get(id = device['stagingserver'])
    print stagingserver.supplier.id
    try:
        updated = UpdatedTables.objects.get(name = "Device")
        # updated.name = "Device"
        updated.supplier_id = stagingserver.supplier.id
        # updated.priority = 11
        updated.last_modified_date = datetime.now
        updated.save()
    except UpdatedTables.DoesNotExist:
        UpdatedTables.objects.create(name = "Device",\
            supplier_id = stagingserver.supplier.id, priority = 11,\
            last_modified_date = datetime.now)

def load_tool_data():
        logger.info(BASE_URL + "tool/")
        try:
            last_updated = UpdatedTables.objects.get(name = "Tool")
            serializer = UpdatedTablesSerializer(last_updated, many=False)
            data = {"last_updated":last_updated.last_modified_date}
        except UpdatedTables.DoesNotExist:
            data = {"last_updated": ""}
        response = unirest.get(BASE_URL + "tool/",
                                headers={"Key":"Token " + TOKEN_KEY},
                                params = data)
        device_create_or_update(response.body)


        

def tool_create_or_update(data):
    for tool in data["Tool"]:
        try:
            tool = Tool.objects.get(id = tool['id'])
            Tool.objects.filter(id= tool['id']).update(name=tool['name'], regrind_count=tool['regrind_count'],\
                tool_id=tool['tool_id'], duration_in_days=tool['duration_in_days'],\
                last_modified_date=tool['last_modified_date'], \
                is_active = tool['is_active'], \
                stagingserver = tool['stagingserver'],
                replace_count = tool['replace_count'],
                equipment = tool['equipment'])
            write_updates(tool)
            logger.info("Tool Updated")
        except Tool.DoesNotExist:
            Tool.objects.create(name=tool['name'], regrind_count=tool['regrind_count'],\
                tool_id=tool['tool_id'], duration_in_days=tool['duration_in_days'],\
                last_modified_date=tool['last_modified_date'], \
                is_active = tool['is_active'], id = tool['id'], \
                stagingserver = tool['stagingserver'], \
                replace_count = tool['replace_count'], equipment = tool['equipment'])
            write_updates(tool)
            logger.info("Tool Created")
       
def write_updates(tool):
    print "write updates"
    stagingserver = StagingServer.objects.get(id = tool['stagingserver'])
    print stagingserver.supplier.id
    try:
        updated = UpdatedTables.objects.get(name = "Tool")
        # updated.name = "Device"
        updated.supplier_id = stagingserver.supplier.id
        # updated.priority = 11
        updated.last_modified_date = datetime.now
        updated.save()
    except UpdatedTables.DoesNotExist:
        UpdatedTables.objects.create(name = "Tool",\
            supplier_id = stagingserver.supplier.id, priority = 11,\
            last_modified_date = datetime.now)         


def check_updates():
    try:
        # load_device_data()
        # load_tool_data()
        updated_tables = UpdatedTables.objects.all()
        serializer = UpdatedTablesSerializer(updated_tables, many=True)
        json_data = {"data": serializer.data}
        response = post("ping/", json.dumps(json_data))
        load_data(response.body)
        
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def post_batch_data():
    batch_list = Batch.objects.filter(is_batch_ended=True).filter(
        is_updated=True).order_by('last_modified_date')
    for batch in batch_list:
        try:
            source_batch_data = []
            source_batch_list = SourceBatch.objects.filter(
                batch=batch)
            batch_serializer = BatchSerializer(batch)
            data = batch_serializer.data
            source_batch_serializer = SourceBatchSerializer(
                source_batch_list, many=True)
            source_batch_string = json.dumps(
                source_batch_serializer.data, sort_keys=True)
            for source_batch in eval(source_batch_string):
                source_batch['batch'] = ""
                source_batch_data.append(source_batch)
            data['source_batch'] = source_batch_data
            json_data = json.dumps(data)
            response = post("batch/create/", json_data)
            if response != None:
                if response.code == 200 or response.code == 201:
                    batch = Batch.objects.get(id=response.body['id'])
                    batch.is_updated = False
                    batch.save()
                    post_inspection_data(batch.id)
        except:
            error_msg = ERR_MSG % (sys.exc_info()[1],
                                   sys.exc_info()[2].tb_lineno)
            logger.error(error_msg)
        


def post_inspection_data(id=None):
    try:
        inspection_samples_list = InspectionSamples.objects.filter(
            batch_id=id)
        for inspection_samples in inspection_samples_list:

            inspection_characteristics_list = InspectionCharacteristics.objects.filter(
                inspection_samples=inspection_samples)

            inspection_samples_serializer = InspectionSamplesSerializer(
                inspection_samples)

            inspection_sample_data = inspection_samples_serializer.data

            inspection_characteristics_serializer = \
                InspectionCharacteristicsSerializer(
                    inspection_characteristics_list, many=True)

            inspection_sample_data['inspection_charateristics'] = \
                inspection_characteristics_serializer.data

            inspection_sample = json.dumps(inspection_sample_data)

            response = post(
                "inspection_data/", inspection_sample)
            if response != None:
                if response.code == 200 or response.code == 201:
                    inspection_samples = InspectionSamples.objects.get(id=response.body['id'])
                    inspection_samples.is_updated = False
                    inspection_samples.save()
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)


def post_inspection_sample_data():
    try:
        batch_list = Batch.objects.filter(is_batch_ended=True).filter(is_updated=False)\
            .filter(is_active=False).order_by('last_modified_date')
        for batch in batch_list:
            inspection_samples_list = InspectionSamples.objects.filter(
                batch_id=batch).filter(is_updated=True)
            for inspection_samples in inspection_samples_list:                

                inspection_characteristics_list = InspectionCharacteristics.objects.filter(
                    inspection_samples=inspection_samples)

                inspection_samples_serializer = InspectionSamplesSerializer(
                    inspection_samples)

                inspection_sample_data = inspection_samples_serializer.data

                inspection_characteristics_serializer = \
                    InspectionCharacteristicsSerializer(
                        inspection_characteristics_list, many=True)

                inspection_sample_data['inspection_charateristics'] = \
                    inspection_characteristics_serializer.data

                inspection_sample = json.dumps(inspection_sample_data)

                response = post(
                    "inspection_data/", inspection_sample)
                if response != None:
                    if response.code == 200 or response.code == 201:
                        inspection_samples = InspectionSamples.objects.get(id=response.body['id'])
                        inspection_samples.is_updated = False
                        inspection_samples.save()
    except:        
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)

if __name__ == '__main__':
    logging.info("Initializing Logger")
    logger = logging.getLogger(__name__)
    setup_logging()
    try:
        while True:
            logger.info("Cycle Started")
            login()
            check_updates()
            post_batch_data()
            post_inspection_sample_data()
            logger.info("Cycle Ended")
	    sys.stdout.flush()
            time.sleep(DEFAULT_SLEEP_TIME)
    except:
        error_msg = ERR_MSG % (sys.exc_info()[1],
                               sys.exc_info()[2].tb_lineno)
        logger.error(error_msg)
