# -*- coding: utf-8 -*-
#
#  __   __.  _______ ____    __    ____   ______   ______        _______.
# |  \ |  | |   ____|\   \  /  \  /   /  /      | /  __  \      /       |
# |   \|  | |  |__    \   \/    \/   /  |  ,----'|  |  |  |    |   (----`
# |  . `  | |   __|    \            /   |  |     |  |  |  |     \   \    
# |  |\   | |  |____    \    /\    /    |  `----.|  `--'  | .----)   |   
# |__| \__| |_______|    \__/  \__/      \______| \______/  |_______/      

#   http://www.apache.org/licenses/LICENSE-2.0

########################################################################################################################
###########################################                       ######################################################
###########################################  READ ONLY LIBRARIES  ######################################################
###########################################                       ######################################################
########################################################################################################################

import os
import subprocess
from builtins import range
from datetime import timedelta, datetime
import pymsteams
import random
import json
import logging
log = logging.getLogger(__name__)
import base64

import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.python_operator import BranchPythonOperator

########################################################################################################################
#######################################                                  ###############################################
#######################################  CUSTOM LIBRARIES AND VARIABLES  ###############################################
#######################################                                  ###############################################
########################################################################################################################

DAGS = '/usr/local/airflow/dags'
PLAYBOOKS = '/usr/local/airflow/playbooks'
SCRIPTS = '/usr/local/airflow/scripts'

########################################################################################################################
##############################################                  ########################################################
##############################################  DAG DEFINITION  ########################################################
##############################################                  ########################################################
########################################################################################################################

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
    'provide_context': True
}

dag = DAG(
    dag_id='deploy_sbc',
    default_args=args,
    schedule_interval=None,
    dagrun_timeout=timedelta(minutes=60),
)

########################################################################################################################
##############################################                  ########################################################
##############################################  Custom Functions  ########################################################
##############################################                  ########################################################
########################################################################################################################

def rollback(**kwargs):
    print('executing rollback playbook...')
    kwargs['ti'].xcom_push(key=None, value=['rollback'])

def write_influx_result(**kwargs):
    print('Writing data feedback to influxdb')
    kwargs['ti'].xcom_push(key=None, value=['influx write metadata!'])

def send_teams_message(**kwargs):
    # get previous task value
    ti = kwargs['ti']
    v1, v2 = ti.xcom_pull(key=None, task_ids=['rollback', 'write_influx_result'])
    print('Previous task metadata: ')
    print('rollback task: ' + str(v1))
    print('influx task: ' + str(v2))

    WEBHOOK_URL = 'https://outlook.office.com/webhook/327044bc-8860-4705-a521-48cc9bfd264e@58005ddb-3d82-4718-9e75-ec5c71cca7ec/IncomingWebhook/ce255d45adfd4d94aa803a84e86e1d6f/4b94f775-45ba-4f8d-a767-252cb12f9726'
    # You must create the connectorcard object with the Microsoft Webhook URL
    myTeamsMessage = pymsteams.connectorcard(WEBHOOK_URL)

    if v1 != None: 
        msg = 'finaliza workflow por camino rollback: ' + str(v1)
    else:
        msg = 'finaliza workflow por camino influxdb: ' + str(v2)

    myTeamsMessage.text(msg)
    print('Sending message ' + str(msg))
    # send the message.
    myTeamsMessage.send()

def query_formio(**kwargs):
    print('query formio db for task information...')
    pass

def deploy_validation(**kwargs):
    answers = ['ok', 'fail']
    answer = random.choice(answers)
    if answer == 'ok':
        print('task success!')
        return 'write_influx_result'
    else:
        print('task failed!')
        return 'rollback'

def backup_sbc(**kwargs):
    print('gathering sbc information for backup...')

def send_teams_init(**kwargs):
    WEBHOOK_URL = 'https://outlook.office.com/webhook/327044bc-8860-4705-a521-48cc9bfd264e@58005ddb-3d82-4718-9e75-ec5c71cca7ec/IncomingWebhook/ce255d45adfd4d94aa803a84e86e1d6f/4b94f775-45ba-4f8d-a767-252cb12f9726'
    # You must create the connectorcard object with the Microsoft Webhook URL
    myTeamsMessage = pymsteams.connectorcard(WEBHOOK_URL)

    airflow_data = str(subprocess.check_output(['hostname']))
    # Add text to the message.
    msg = 'comienza el workflow en worker: ' + airflow_data + '!'
    myTeamsMessage.text(msg)
    print('Sending message ' + str(msg))
    # send the message.
    myTeamsMessage.send()

def context_data(**context):
    """
    Print the payload "message" passed to the DagRun conf attribute.
    :param context: The execution context
    :type context: dict
    """
    print("Remotely received value of {}".format(str(context["dag_run"].conf)))

########################################################################################################################
###############################################                     ####################################################
###############################################  TASKS DEFINITIONS  ####################################################
###############################################                     ####################################################
########################################################################################################################

newcos_init = BashOperator(task_id='newcos_init',bash_command='ansible --version -vvv', dag=dag,)
teams_message = PythonOperator(task_id='send_teams_message', python_callable=send_teams_message, trigger_rule='one_success',dag=dag,)
deploy_playbook_sbc = BashOperator(task_id='deploy_sbc',bash_command='cd ' + PLAYBOOKS + ' && ansible-playbook -i ' + PLAYBOOKS + '/inventory ' + PLAYBOOKS + '/sbc_audiocodes_telnet.yaml', dag=dag,)
deploy_validation = BranchPythonOperator(task_id='deploy_validation', python_callable=deploy_validation, dag=dag,)
query_formio = PythonOperator(task_id='query_formio', python_callable=query_formio,dag=dag,)
rollback = PythonOperator(task_id='rollback', python_callable=rollback,dag=dag,)
write_influx_result = PythonOperator(task_id='write_influx_result', python_callable=write_influx_result, trigger_rule='one_success', dag=dag,)
newcos_end = BashOperator(task_id='newcos_end', bash_command='echo "run_id={{ run_id }} | dag_run={{ dag_run }}"', trigger_rule='one_success', dag=dag,)
backup_sbc = PythonOperator(task_id='backup_sbc',python_callable=backup_sbc, dag=dag,)
context_data = PythonOperator(task_id='dag_context', python_callable=context_data, dag=dag)
init_teams_message = PythonOperator(task_id='init_teams_message', python_callable=send_teams_init, trigger_rule='one_success',dag=dag,)

########################################################################################################################
################################################                  ######################################################
################################################  TASKS WORKFLOW  ######################################################
################################################                  ######################################################
########################################################################################################################

newcos_init >> query_formio
newcos_init >> backup_sbc
newcos_init >> init_teams_message
newcos_init >> context_data
init_teams_message >> deploy_playbook_sbc
backup_sbc >> deploy_playbook_sbc
query_formio >> deploy_playbook_sbc
context_data >> deploy_playbook_sbc
deploy_playbook_sbc >> deploy_validation
deploy_validation >>  rollback >> teams_message
deploy_validation >> write_influx_result >> teams_message
write_influx_result >> teams_message
teams_message >> newcos_end

if __name__ == "__main__":
    dag.cli()
