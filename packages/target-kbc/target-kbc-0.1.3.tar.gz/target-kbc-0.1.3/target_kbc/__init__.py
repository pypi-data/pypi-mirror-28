"__author__ = 'Leo Chan'"
"__credits__ = 'Keboola 2017'"

"""
Python 3 environment 
"""
#import pip
#pip.main(['install', '--disable-pip-version-check', '--no-cache-dir', 'git+https://github.com/keboola/sapi-python-client.git'])

import argparse
import io
import os
import sys
import json
import csv
import requests
import singer
from kbcstorage.client import Client


logger = singer.get_logger()


def kbc_upload(storage_token, bucket_id, file_json):
    """
    Create/upload table into KBC
    """
    client = Client('https://connection.keboola.com', storage_token)
    for i in file_json:
        file_name = i    
        file_path = i+".csv"
        try:
            client.tables.create(   
                name = file_name,
                bucket_id = bucket_id,
                file_path = file_path,
                primary_key = file_json[i]["pk"]
            )
            logger.info("Created new table: {0}".format(file_name))
            logger.info("File Destination: {0}".format(bucket_id+"."+file_name))
        except RuntimeError as err:
            logger.info(err)
            client.tables.load(
                table_id = bucket_id+"."+file_name,
                file_path = file_path,
                is_incremental = True
            )
            logger.info("Loaded into exisiting table: {0}".format(file_name))
            logger.info("File Destination: {0}".format(bucket_id+"."+file_name))
        except requests.exceptions.HTTPError as err:
            logger.error(err)
            logger.error("Please check your Storage Token/Permission.")
            raise

def flatten_json(y):
    """
    # flat out the json objects
    """
    out = {}
    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def send_usage_stats():
    try:
        version = pkg_resources.get_distribution('target-keboola').version
        conn = http.client.HTTPSConnection('collector.stitchdata.com', timeout=10)
        conn.connect()
        params = {
            'e': 'se',
            'aid': 'singer',
            'se_ca': 'target-keboola',
            'se_ac': 'open',
            'se_la': version,
        }
        conn.request('GET', '/i?' + urllib.parse.urlencode(params))
        response = conn.getresponse()
        conn.close()
    except:
        logger.debug('Collection request failed')

def main():
    """
    Main Execution Script
    """
    ### Fetching data results from Singer tabs
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file', required=True)
    args = parser.parse_args()
    
    ### Loading required information from config
    if args.config:
        with open(args.config) as input:
            config = json.load(input)
            logger.info("Configuration file loaded.")
    else:
        config = {}

    if not config.get('disable_collection', False):
        logger.info('Sending version information to stitchdata.com. ' +
                    'To disable sending anonymous usage data, set ' +
                    'the config parameter "disable_collection" to true')
        threading.Thread(target=send_usage_stats).start()

    ### Verify required parameters in configuration file
    if ("storage_token" not in config) and ("bucket_id" not in config):
        raise Exception("Please enter 'storage_token' and 'bucket_id' into your configuration.")
    storage_token = config["storage_token"]
    bucket_id = config["bucket_id"]
    
    ### Fetching tap queries
    input = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

    files_pk_output = {}
    for line in input:
        sys.stdout.write(line)
        ### Loading line as JSON
        try:
            line = json.loads(line)
        except Exception as err:
            logger.error("Unable to parse {0}".format(line))
            raise
        
        if "type" not in line:
            raise Exception("Line is missing required key 'type': {0}".format(line))

        ### Case 1: Line type =  RECORD
        if line["type"]=="RECORD":
            ### Validating stream name
            if "stream" not in line:
                raise Exception("stream is missing: {0}".format(line))
            filename = line["stream"]
            ### Validating records 
            if "record" not in line:
                raise Exception("record is missing; {0}".format(line))
            flat_data = flatten_json(line["record"])
            header = flat_data.keys()
            count = files_pk_output[filename]["output_count"]

            ### Validate if a new file is created for this run
            if count == 0:
                with open(filename+".csv", 'w') as output:
                    writer = csv.DictWriter(output, header)
                    writer.writeheader()
                    writer.writerow(flat_data)
                    files_pk_output[filename]["output_count"] += 1
            else:
                with open(filename+".csv", 'a') as output:
                    writer = csv.DictWriter(output, header)
                    writer.writerow(flat_data)

        ### Case 2: Line type =  SCHEMA
        elif line["type"]=="SCHEMA":
            ### Validating stream name
            if "stream" not in line:
                raise Exception("stream is missing: {0}".format(line))
            filename = line["stream"]
            ### Validating primary key
            if "key_properties" not in line:
                raise Exception("key_properties is missing: {0}".format(line))
            pk = line["key_properties"]
            
            ### Validate stream
            if filename not in files_pk_output:
                temp_json = {
                    #"filename": filename,
                    "pk": pk,
                    "output_count": 0
                }
                #files_pk_output.append(temp_json)
                files_pk_output[filename] = temp_json
            else:
                raise Exception("Duplicated SCHEME for {0}('stream'): {1}".format(line["stream"], line))

        ### Case 3: Line type = STATE
        elif line["type"]=="STATE":
            pass

        ### Case 4: invalid type
        else:
            raise Exception("Input row is an unknown type: {0}".format(line))


    ### Output to KBC Bucket
    kbc_upload(storage_token, bucket_id, files_pk_output)

    logger.info("Target exiting normally")



if __name__ == '__main__':
    
    main()
    
    

