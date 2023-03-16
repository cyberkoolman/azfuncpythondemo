import logging
import os
import json
import requests
from enum import Enum
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Alert from Azure Monitor is received. Proecessing request begins.')

    RESOURCE_GROUP_NAME = os.environ["AmexResourceGroup"]
    E1_URL = os.environ["E1_URL"]
    E2_URL = os.environ["E2_URL"]
    E3_URL = os.environ["E3_URL"]
    SUBSCRIPTION_ID=os.environ["SubscriptionId"]

    # Given by runtime
    THIS_AZFUNC_ENV = os.environ["AZURE_FUNCTIONS_ENVIRONMENT"]

    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    data = req.params.get('data')
    if not data:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            data = req_body.get('data')

    alert_target_id = data['essentials']['alertTargetIDs']
    vm_name = alert_target_id[0].split('/')[-1]
    if THIS_AZFUNC_ENV == ThisRunEnvironment.DEVELOPMENT.value:
        vm_info = compute_client.virtual_machines.get(resource_group_name=RESOURCE_GROUP_NAME, vm_name=vm_name)
    else:
        vm_info = compute_client.virtual_machines.get(resource_group_name=RESOURCE_GROUP_NAME, vm_name=vm_name)
    logging.info(vm_info)
    severity = vm_info.tags.get("Severity")

    if severity == "E1":
        url = E1_URL
    elif severity == "E2":
        url = E2_URL
    else:
        url = E3_URL
  
    headers = { 
        'Content-Type': 'application/json'
    }
    body = {
        "vm_name": vm_info,
        "severity": severity,
        "requested_from": "AlertHandler"
    }
    payload = json.dumps(data)

    try:
        response = requests.post(url=url, data=payload, headers=headers)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
    return func.HttpResponse(response.raise_for_status())

class ThisRunEnvironment(Enum):
    PRODUCTION = "Production",
    DEVELOPMENT = "Development"