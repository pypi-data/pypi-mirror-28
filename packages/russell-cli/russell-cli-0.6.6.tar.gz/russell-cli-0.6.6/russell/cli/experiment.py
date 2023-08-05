import click
import webbrowser
from tabulate import tabulate
from time import sleep
import requests
import json
import sys

import russell
from russell.cli.utils import get_task_url, get_module_task_instance_id
from russell.client.common import get_url_contents
from russell.client.experiment import ExperimentClient
from russell.client.log import LogClient
from russell.client.module import ModuleClient
from russell.client.project import ProjectClient
from russell.client.task_instance import TaskInstanceClient
from russell.config import generate_uuid
from russell.manager.auth_config import AuthConfigManager
from russell.manager.experiment_config import ExperimentConfigManager
from russell.manager.russell_ignore import RussellIgnoreManager
from russell.model.experiment_config import ExperimentConfig
from russell.log import logger as russell_logger

@click.command()
@click.argument('id', required=False, nargs=1)
def status(id):
    """
    View status of all or specific run.
    It can also list status of all the runs in the project.
    """
    if id:
        experiment = ExperimentClient().get(id)
        print_experiments([experiment])
    else:
        experiments = ExperimentClient().get_all()
        print_experiments(experiments)

def print_experiments(experiments):
    """
    Prints expt details in a table. Includes urls and mode parameters
    """
    headers = ["RUN ID", "CREATED", "STATUS", "DURATION(s)", "NAME", "INSTANCE", "VERSION"]
    expt_list = []
    for experiment in experiments:
        expt_list.append([experiment.id, experiment.created_pretty, experiment.state,
                          experiment.duration_rounded, experiment.name,
                          experiment.instance_type_trimmed, experiment.description])
    russell_logger.info(tabulate(expt_list, headers=headers))



@click.command()
@click.argument('id', nargs=1)
def info(id):
    """
    Prints detailed info for the run
    """
    experiment = ExperimentClient().get(id)
    task_instance_id = get_module_task_instance_id(experiment.task_instances)
    task_instance = TaskInstanceClient().get(task_instance_id) if task_instance_id else None
    mode = url = None
    if experiment.state == "running":
        if task_instance and task_instance.mode in ['jupyter', 'serving']:
            mode = task_instance.mode
            url = get_task_url(experiment.id,experiment.instance_type_trimmed == "gpu")
    table = [["Run ID", experiment.id], ["Name", experiment.name], ["Created", experiment.created_pretty],
             ["Status", experiment.state], ["Duration(s)", experiment.duration_rounded],
             ["Output ID", task_instance.output_ids["output"] if task_instance else None], ["Instance", experiment.instance_type_trimmed],
             ["Version", experiment.description]]
    if mode:
        table.append(["Mode", mode])
    if url:
        table.append(["Url", url])
    russell_logger.info(tabulate(table))

@click.command()
# @click.option('-u', '--url', is_flag=True, default=False, help='Only print url for accessing logs')
@click.option('-t', '--tail', is_flag=True, default=False, help='Stream the logs')
@click.argument('id', nargs=1)
def logs(id, tail, sleep_duration=1):
    """
    Print the logs of the run.
    """
    import logging
    try:
        lc = LogClient()
    except Exception as e:
        russell_logger.error(e.message)
        return
    logging.disable(sys.maxsize)
    try:
        lc.get_logs(id)
    except Exception as e:
        logging.disable(logging.NOTSET)
        russell_logger.error(e.message)
        sys.exit("""Cannot connect to the Russell server. 
    Please retry after a while or contact the development team via contact@russellcloud.cn""")
    logging.disable(logging.NOTSET)

@click.command()
@click.option('-u', '--url', is_flag=True, default=False, help='Only print url for accessing logs')
@click.argument('id', nargs=1)
def output(id, url):
    """
    Shows the output url of the run.
    By default opens the output page in your default browser.
    """
    experiment = ExperimentClient().get(id)
    task_instance = TaskInstanceClient().get(get_module_task_instance_id(experiment.task_instances))
    output_instance_id = task_instance.output_ids.get('output')
    if output_instance_id:
        access_token = AuthConfigManager.get_access_token()
        if access_token is None:
            russell_logger.error("Please login first")
            return
        output_dir_url = "{}/files/data/{}/?token={}".format(russell.russell_host,
                                                    output_instance_id,
                                                    access_token.token)
        if url:
            russell_logger.info(output_dir_url)
        else:
            russell_logger.info("Opening output directory in your browser ...")
            webbrowser.open(output_dir_url)
    else:
        russell_logger.error("Output directory not available")



@click.command()
@click.argument('id', nargs=1)
def stop(id):
    """
    Stop a run before it can finish.
    """
    experiment = ExperimentClient().get(id)
    if experiment.state not in ["waiting", "running"]:
        russell_logger.info("Experiment in {} state cannot be stopped".format(experiment.state))
        return
    if ExperimentClient().stop(id):
        russell_logger.info("Experiment shutdown request submitted. Check status to confirm shutdown")
    else:
        russell_logger.error("Failed to stop experiment")



@click.command()
@click.argument('id', nargs=1)
@click.option('-y', '--yes', is_flag=True, default=False, help='Skip confirmation')
def delete(id, yes):
    """
    Delete project run
    """
    try:
        ec = ExperimentClient()
        tc = TaskInstanceClient()
    except Exception as e:
        russell_logger.error(e.message)
        return

    experiment = ec.get(id)
    task_instance = tc.get(get_module_task_instance_id(experiment.task_instances))

    if experiment.state in ["queued", "running"]:
        russell_logger.info("Experiment in {} state cannot be deleted. Stop it first".format(experiment.state))
        return

    if not yes:
        click.confirm('Delete Run: {}?'.format(experiment.name), abort=True, default=False)

    if task_instance.module_id:
        ModuleClient().delete(task_instance.module_id)

    if ExperimentClient().delete(id):
        russell_logger.info("Experiment deleted")
    else:
        russell_logger.error("Failed to delete experiment")
