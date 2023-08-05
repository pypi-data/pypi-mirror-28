#-*- coding: utf-8 -*-

__version__ = "1.5.7"

#import six as _six
import warnings as _warnings
import requests as _requests
import fire as _fire
import tarfile as _tarfile
import os as _os
import sys as _sys
import kubernetes.client as _kubeclient
#from kubernetes.client.rest import ApiException as _ApiException
import kubernetes.config as _kubeconfig
#import yaml as _yaml
import json as _json
from pprint import pprint as _pprint
import subprocess as _subprocess
#from datetime import timedelta as _timedelta
import jinja2 as _jinja2
import boto3 as _boto3
import base64 as _base64
from flask import request as _requset, url_for as _url_for
from flask_api import FlaskAPI as _FlaskAPI, status as _status, exceptions as _exceptions
from inspect import getmembers as _getmembers, isfunction as _isfunction

app = _FlaskAPI(__name__)

if _sys.version_info.major == 3:
    from urllib3 import disable_warnings as _disable_warnings
    _disable_warnings()

# Deprecated
_kube_deploy_registry = {'jupyter': (['jupyterhub-deploy.yaml'], []),
                        'jupyterhub': (['jupyterhub-deploy.yaml'], []),
                        'spark': (['spark-master-deploy.yaml'], ['spark-worker', 'metastore']),
                        'spark-worker': (['spark-worker-deploy.yaml'], []),
                        'metastore': (['metastore-deploy.yaml'], ['mysql']),
                        'hdfs': (['namenode-deploy.yaml'], []),
                        'redis': (['redis-master-deploy.yaml'], []),
                        'presto': (['presto-master-deploy.yaml',
                                    'presto-worker-deploy.yaml'], ['metastore']),
                        'presto-ui': (['presto-ui-deploy.yaml'], ['presto']),
                        'airflow': (['airflow-deploy.yaml'], ['mysql', 'redis']),
                        'mysql': (['mysql-master-deploy.yaml'], []),
                        #'web-home': (['web/home-deploy.yaml'], []),
                        'zeppelin': (['zeppelin-deploy.yaml'], []),
                        #'zookeeper': (['zookeeper-deploy.yaml'], []),
                        'elasticsearch': (['elasticsearch-2-3-0-deploy.yaml'], []),
                        'kibana': (['kibana-4-5-0-deploy.yaml'], ['elasticsearch'], []), 
                        #'kafka': (['stream/kafka-0.11-deploy.yaml'], ['zookeeper']),
                        'cassandra': (['cassandra-deploy.yaml'], []),
                        'jenkins': (['jenkins-deploy.yaml'], []),
                        #'turbine': (['dashboard/turbine-deploy.yaml'], []),
                        #'hystrix': (['dashboard/hystrix-deploy.yaml'], []),
                       }

# Deprecated
_kube_svc_registry = {'jupyter': (['jupyterhub-svc.yaml'], []),
                     'jupyterhub': (['jupyterhub-svc.yaml'], []),
                     'spark': (['spark-master-svc.yaml'], ['spark-worker', 'metastore']), 
                     'spark-worker': (['spark-worker-svc.yaml'], []),
                     'metastore': (['metastore-svc.yaml'], ['mysql']),
                     'hdfs': (['namenode-svc.yaml'], []),
                     'redis': (['redis-master-svc.yaml'], []),
                     'presto': (['presto-master-svc.yaml',
                                 'presto-worker-svc.yaml'], ['metastore']),
                     'presto-ui': (['presto-ui-svc.yaml'], ['presto']),
                     'airflow': (['airflow-svc.yaml'], ['mysql', 'redis']),
                     'mysql': (['mysql-master-svc.yaml'], []),
                     #'web-home': (['web/home-svc.yaml'], []),
                     'zeppelin': (['zeppelin-svc.yaml'], []),
                     #'zookeeper': (['zookeeper/zookeeper-svc.yaml'], []),
                     'elasticsearch': (['elasticsearch-2-3-0-svc.yaml'], []),
                     'kibana': (['kibana-4-5-0-svc.yaml'], ['elasticsearch'], []),
                     #'kafka': (['stream/kafka-0.11-svc.yaml'], ['zookeeper']),
                     'cassandra': (['cassandra-svc.yaml'], []),
                     #'jenkins': (['jenkins-svc.yaml'], []),
                     #'turbine': (['dashboard/turbine-svc.yaml'], []),
                     #'hystrix': (['dashboard/hystrix-svc.yaml'], []),
                    }

_Dockerfile_template_registry = {
                                 'predict-server': (['predict-server-local-dockerfile.template'], []),
                                 'train-server': (['train-server-local-dockerfile.template'], []),
                                }
_kube_router_deploy_template_registry = {'predict-router-split': (['predict-router-split-deploy.yaml.template'], []),
                                         'predict-router-split-gpu': (['predict-router-split-gpu-deploy.yaml.template'], [])}
_kube_router_ingress_template_registry = {'predict-router-split': (['predict-router-split-ingress.yaml.template'], [])}
_kube_router_svc_template_registry = {'predict-router-split': (['predict-router-split-svc.yaml.template'], [])}
_kube_router_routerules_template_registry = {'predict-router-split': (['predict-router-split-routerules.yaml.template'], [])}
_kube_router_autoscale_template_registry = {'predict-router-split': (['predict-router-split-autoscale.yaml.template'], [])}

_kube_stream_deploy_template_registry = {'stream': (['stream-kafka-deploy.yaml.template'], [])}
_kube_stream_svc_template_registry = {'stream': (['stream-kafka-svc.yaml.template'], [])}

_kube_cluster_autoscale_template_registry = {'predict-cluster': (['predict-cluster-autoscale.yaml.template'], [])}
_kube_cluster_deploy_template_registry = {'predict-cluster': (['predict-cluster-deploy.yaml.template'], [])}
_kube_cluster_svc_template_registry = {'predict-cluster': (['predict-cluster-svc.yaml.template'], [])}

_train_kube_template_registry = {'train-cluster': (['train-cluster.yaml.template'], [])}

_pipeline_api_version = 'v1'

_default_pipeline_templates_path = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), 'templates'))
_default_pipeline_services_path = _os.path.normpath(_os.path.join(_os.path.dirname(__file__), 'services'))

_default_image_registry_url = 'docker.io'
_default_image_registry_repo = 'pipelineai'
_default_image_registry_train_namespace = 'train'
_default_image_registry_predict_namespace = 'predict' 
_default_image_registry_stream_namespace = 'stream'
_default_image_registry_base_tag = '1.5.0'

_default_model_chip = 'cpu'

_default_build_type = 'docker'
_default_build_context_path = '.'

_default_cluster_namespace = 'default'


def help():
    this_module = _sys.modules[__name__]
    functions = [o[0] for o in _getmembers(this_module) if _isfunction(o[1])]
    functions = [function for function in functions if not function.startswith('_')]
    functions = sorted(functions)
    print("\n".join(functions))


def version():
    print('')
    print('cli_version: %s' % __version__)
    print('api_version: %s' % _pipeline_api_version)
    print('')
    print('default build type: %s' % _default_build_type)

    build_context_path = _os.path.expandvars(_default_build_context_path)
    build_context_path = _os.path.expanduser(build_context_path)
    build_context_path = _os.path.abspath(build_context_path)
    build_context_path = _os.path.normpath(build_context_path)

    print('default build context path: %s => %s' % (_default_build_context_path, build_context_path))
    print('')
    print('default train base image: %s/%s/%s-%s:%s' % (_default_image_registry_url, _default_image_registry_repo, _default_image_registry_train_namespace, _default_model_chip, _default_image_registry_base_tag))
    print('default predict base image: %s/%s/%s-%s:%s' % (_default_image_registry_url, _default_image_registry_repo, _default_image_registry_predict_namespace, _default_model_chip, _default_image_registry_base_tag))
    print('')
    print('capabilities enabled: %s' % ['train-server', 'train-kube', 'train-sage', 'predict-server', 'predict-kube', 'predict-sage', 'predict-kafka'])
    print('capabilities available: %s' % ['optimize', 'jupyter', 'spark', 'airflow', 'kafka'])
    print('')
    print('Email upgrade@pipeline.ai to enable additional capabilities.')
    print('')


def _templates_path():
    print("")
    print("templates path: %s" % _default_pipeline_templates_path)
    print("")


def _get_default_model_runtime(model_type):
    model_runtime = 'python'

    if model_type in ['keras', 'python', 'scikit']:
       model_runtime = 'python'
     
    if model_type in ['java', 'pmml', 'spark', 'xgboost']:
       model_runtime = 'jvm'

    if model_type in ['tensorflow']:
       model_runtime = 'tfserving'

    return model_runtime


def _validate_and_prep_model_tag(model_tag):
    model_tag = str(model_tag)
    model_tag = model_tag.lower()
    return model_tag


def _validate_and_prep_model_tag_and_weight_dict(model_tag_and_weight_dict):
    model_weight_total = 0
    for tag, _ in model_tag_and_weight_dict.items():
        model_weight = int(model_tag_and_weight_dict[tag])
        model_weight_total += model_weight

    if model_weight_total != 100:
        raise ValueError("Total of '%s' for weights '%s' does not equal 100 as expected." % (model_weight_total, model_tag_and_weight_dict))
        
    return 


@app.route("/predict-kube-endpoint/<string:model_name>/", methods=['GET'])
def predict_kube_endpoint(model_name,
                          cluster_namespace=None,
                          image_registry_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        ingress = _get_model_endpoint(model_name=model_name, 
                                      cluster_namespace=cluster_namespace,
                                      image_registry_namespace=image_registry_namespace)

        response = kubeclient_v1_beta1.list_namespaced_deployment(namespace=cluster_namespace,
                                                                  include_uninitialized=True,
                                                                  watch=False,
                                                                  limit=1000,
                                                                  pretty=False)

        deployments = response.items
        model_variant_list = [deployment.metadata.name for deployment in deployments
                               if 'predict-%s' % model_name in deployment.metadata.name]

    return {"endpoint": ingress, "model_variants": model_variant_list}


@app.route("/predict-kube-endpoints/", methods=['GET'])
def predict_kube_endpoints(cluster_namespace=None,
                           image_registry_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    endpoint_list = []
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")

        # TODO: Get all ingresses starting with 'predict-'
        endpoint_list = _get_all_model_endpoints(cluster_namespace=cluster_namespace,
                                                 image_registry_namespace=image_registry_namespace)

    return {"endpoints": endpoint_list}


#@app.route("/predict-kube-status/<string:model_type>/<string:model_name>/", methods=['GET', 'PUT'])
#def predict_kube_status(model_type,
#                        model_name):
#    import glob as _glob
#
#    models_path = _os.path.expandvars('.')
#    models_path = _os.path.expanduser(models_path)
#    models_path = _os.path.abspath(models_path)
#    models_path = _os.path.normpath(models_path)
#
#    status_filename_prefix = 'pipeline_status'
#
#    glob_path = '%s/%s/status/%s.*' % (model_type, model_name, status_filename_prefix)
#    print(glob_path)
#
#    glob_paths = _glob.glob(glob_path)
#    print(glob_paths)
#
#    statuses = []
#    for path in glob_paths:
#        with open(path, 'r') as fh:
#            status = fh.read()
#            statuses += [{"status": status.rstrip()}]
#
#    return statuses


def predict_kube_connect(model_name,
                         model_tag,
                         model_type,
                         model_runtime=None,
                         model_chip=None,
                         local_port=None,
                         service_port=None,
                         cluster_namespace=None,
                         image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_connect(service_name=service_name,
                          cluster_namespace=cluster_namespace,
                          local_port=local_port,
                          service_port=service_port)


def _service_connect(
                     service_name,
                     cluster_namespace=None,
                     local_port=None,
                     service_port=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    pod = _get_pod_by_service_name(service_name=service_name)
    if not pod:
        print("")
        print("Service '%s' is not running." % service_name)
        print("")
        return
    if not service_port:
        svc = _get_svc_by_service_name(service_name=service_name)
        if not svc:
            print("")
            print("Service '%s' proxy port cannot be found." % service_name)
            print("")
            return
        service_port = svc.spec.ports[0].target_port

    if not local_port:
        print("")
        print("Proxying local port '<randomly-chosen>' to app '%s' port '%s' using pod '%s'." % (service_port, service_name, pod.metadata.name))
        print("")
        print("Use 'http://127.0.0.1:<randomly-chosen>' to access app '%s' on port '%s'." % (service_name, service_port))
        print("")
        print("If you break out of this terminal, your proxy session will end.")
        print("")
        cmd = 'kubectl port-forward %s :%s' % (pod.metadata.name, service_port)
        print("Running command...")
        print(cmd)
        print("")
        _subprocess.call(cmd, shell=True)
        print("")
    else:
        print("")
        print("Proxying local port '%s' to app '%s' port '%s' using pod '%s'." % (local_port, service_port, service_name, pod.metadata.name))
        print("")
        print("Use 'http://127.0.0.1:%s' to access app '%s' on port '%s'." % (local_port, service_name, service_port))
        print("")
        print("If you break out of this terminal, your proxy session will end.")
        print("")
        _subprocess.call('kubectl port-forward %s %s:%s' % (pod.metadata.name, local_port, service_port), shell=True)
        print("")


def _environment_resources():
    _subprocess.call("kubectl top node", shell=True)

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                          pretty=True)
        deployments = response.items
        for deployment in deployments:
            _service_resources(deployment.metadata.name)


def _service_resources(service_name):

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()
    
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, 
                                                             pretty=True)
        pods = response.items
        for pod in pods: 
            if (service_name in pod.metadata.name):
                _subprocess.call('kubectl top pod %s' % pod.metadata.name, shell=True)
    print("")


def _create_predict_server_Dockerfile(model_name,
                                      model_tag,
                                      model_type,
                                      model_runtime,
                                      model_chip,
                                      model_path,
                                      http_proxy,
                                      https_proxy,
                                      log_stream_url,
                                      log_stream_topic,
                                      input_stream_url,
                                      input_stream_topic,
                                      output_stream_url,
                                      output_stream_topic,
                                      image_registry_url,
                                      image_registry_repo,
                                      image_registry_namespace,
                                      image_registry_base_tag,
                                      image_registry_base_chip,
                                      pipeline_templates_path,
                                      build_context_path):

    model_tag = _validate_and_prep_model_tag(model_tag)

    context = {
               'PIPELINE_MODEL_NAME': model_name,
               'PIPELINE_MODEL_TAG': model_tag,
               'PIPELINE_MODEL_TYPE': model_type,
               'PIPELINE_MODEL_RUNTIME': model_runtime,
               'PIPELINE_MODEL_CHIP': model_chip,
               'PIPELINE_MODEL_PATH': model_path,
               'PIPELINE_LOG_STREAM_URL': log_stream_url,
               'PIPELINE_LOG_STREAM_TOPIC': log_stream_topic,
               'PIPELINE_INPUT_STREAM_URL': input_stream_url,
               'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
               'PIPELINE_OUTPUT_STREAM_URL': output_stream_url,
               'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
               'PIPELINE_IMAGE_REGISTRY_URL': image_registry_url,
               'PIPELINE_IMAGE_REGISTRY_REPO': image_registry_repo,
               'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
               'PIPELINE_IMAGE_REGISTRY_BASE_TAG': image_registry_base_tag
              }

    model_predict_cpu_Dockerfile_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _Dockerfile_template_registry['predict-server'][0][0]))
    path, filename = _os.path.split(model_predict_cpu_Dockerfile_templates_path)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    rendered_Dockerfile = _os.path.normpath('%s/.pipeline-generated-%s-%s-%s-Dockerfile' % (build_context_path, image_registry_namespace, model_name, model_tag))
    with open(rendered_Dockerfile, 'wt') as fh:
        fh.write(rendered)
        print("'%s' => '%s'." % (filename, rendered_Dockerfile))

    return rendered_Dockerfile


def _predict_server_describe(model_name,
                             model_tag):
    pass        


def predict_server_build(model_name,
                         model_tag,
                         model_type,
                         model_path,
                         model_runtime=None,
                         model_chip=None,
                         http_proxy=None,
                         https_proxy=None,
                         log_stream_url=None,
                         log_stream_topic=None,
                         input_stream_url=None,
                         input_stream_topic=None,
                         output_stream_url=None,
                         output_stream_topic=None,
                         build_type=None,
                         build_context_path=None,
                         image_registry_url=None,
                         image_registry_repo=None,
                         image_registry_namespace=None,
                         image_registry_base_tag=None,
                         image_registry_base_chip=None,
                         pipeline_templates_path=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_chip:
        model_chip = _default_model_chip

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not build_type:
        build_type = _default_build_type

    if not build_context_path: 
        build_context_path = _default_build_context_path

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    if not image_registry_base_tag:
        image_registry_base_tag = _default_image_registry_base_tag

    if not image_registry_base_chip:
        image_registry_base_chip = _default_model_chip

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    build_context_path = _os.path.expandvars(build_context_path)
    build_context_path = _os.path.expanduser(build_context_path)
    build_context_path = _os.path.abspath(build_context_path)
    build_context_path = _os.path.normpath(build_context_path)

    pipeline_templates_path = _os.path.expandvars(pipeline_templates_path)
    pipeline_templates_path = _os.path.expanduser(pipeline_templates_path)
    pipeline_templates_path = _os.path.abspath(pipeline_templates_path)
    pipeline_templates_path = _os.path.normpath(pipeline_templates_path)
    pipeline_templates_path = _os.path.relpath(pipeline_templates_path, build_context_path)
    pipeline_templates_path = _os.path.normpath(pipeline_templates_path)

    model_path = _os.path.expandvars(model_path)
    model_path = _os.path.expanduser(model_path)
    model_path = _os.path.abspath(model_path)
    model_path = _os.path.normpath(model_path)
    model_path = _os.path.relpath(model_path, build_context_path)
    model_path = _os.path.normpath(model_path)

    if build_type == 'docker':
        generated_Dockerfile = _create_predict_server_Dockerfile(model_name=model_name,
                                                                      model_tag=model_tag, 
                                                                      model_type=model_type, 
                                                                      model_path=model_path,
                                                                      model_runtime=model_runtime,
                                                                      model_chip=model_chip,
                                                                      http_proxy=http_proxy,
                                                                      https_proxy=https_proxy,
                                                                      log_stream_url=log_stream_url,
                                                                      log_stream_topic=log_stream_topic,
                                                                      input_stream_url=input_stream_url,
                                                                      input_stream_topic=input_stream_topic,
                                                                      output_stream_url=output_stream_url,
                                                                      output_stream_topic=output_stream_topic,
                                                                      image_registry_url=image_registry_url,
                                                                      image_registry_repo=image_registry_repo,
                                                                      image_registry_namespace=image_registry_namespace,
                                                                      image_registry_base_tag=image_registry_base_tag,
                                                                      image_registry_base_chip=image_registry_base_chip,
                                                                      pipeline_templates_path=pipeline_templates_path,
                                                                      build_context_path=build_context_path)

        if http_proxy:
           http_proxy_build_arg_snippet = '--build-arg HTTP_PROXY=%s' % http_proxy
        else:
           http_proxy_build_arg_snippet = ''

        if https_proxy:
           https_proxy_build_arg_snippet = '--build-arg HTTPS_PROXY=%s' % https_proxy
        else:
           https_proxy_build_arg_snippet = ''

        cmd = 'docker build %s %s -t %s/%s/%s-%s:%s -f %s %s' % (http_proxy_build_arg_snippet, https_proxy_build_arg_snippet, image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag, generated_Dockerfile, build_context_path)

        print(cmd)
        print("")
        process = _subprocess.call(cmd, shell=True)
    else:
        print("Build type '%s' not found." % build_type)


def _create_predict_kube_Kubernetes_yaml(model_name,
                                         model_tag,
                                         model_type,
                                         model_runtime=None,
                                         model_chip=None,
                                         log_stream_url=None,
                                         log_stream_topic=None,
                                         input_stream_url=None,
                                         input_stream_topic=None,
                                         output_stream_url=None,
                                         output_stream_topic=None,
                                         memory_limit='2Gi',
                                         core_limit='1000m',
                                         target_core_util_percentage='50',
                                         min_replicas='1',
                                         max_replicas='2',
                                         cluster_namespace=None,
                                         image_registry_url=None,
                                         image_registry_repo=None,
                                         image_registry_namespace=None,
                                         image_registry_base_tag=None,
                                         image_registry_base_chip=None,
                                         pipeline_templates_path=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_chip:
        model_chip = _default_model_chip

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    if not image_registry_base_tag:
        image_registry_base_tag = _default_image_registry_base_tag

    if not image_registry_base_chip:
        image_registry_base_chip = _default_model_chip

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    pipeline_templates_path = _os.path.expandvars(pipeline_templates_path)
    pipeline_templates_path = _os.path.expanduser(pipeline_templates_path)
    pipeline_templates_path = _os.path.abspath(pipeline_templates_path)
    pipeline_templates_path = _os.path.normpath(pipeline_templates_path)

    context = {
               'PIPELINE_MODEL_NAME': model_name,
               'PIPELINE_MODEL_TAG': model_tag,
               'PIPELINE_MODEL_TYPE': model_type,
               'PIPELINE_MODEL_RUNTIME': model_runtime,
               'PIPELINE_MODEL_CHIP': model_chip,
               'PIPELINE_LOG_STREAM_URL': log_stream_url,
               'PIPELINE_LOG_STREAM_TOPIC': log_stream_topic,
               'PIPELINE_INPUT_STREAM_URL': input_stream_url,
               'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
               'PIPELINE_OUTPUT_STREAM_URL': output_stream_url,
               'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
               'PIPELINE_CORE_LIMIT': core_limit,
               'PIPELINE_MEMORY_LIMIT': memory_limit,
               'PIPELINE_TARGET_CORE_UTIL_PERCENTAGE': target_core_util_percentage,
               'PIPELINE_MIN_REPLICAS': min_replicas,
               'PIPELINE_MAX_REPLICAS': max_replicas,
               'PIPELINE_IMAGE_REGISTRY_URL': image_registry_url,
               'PIPELINE_IMAGE_REGISTRY_REPO': image_registry_repo,
               'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
               'PIPELINE_IMAGE_REGISTRY_BASE_TAG': image_registry_base_tag,
              }

    rendered_filenames = []

    if model_chip == 'gpu':
        model_router_deploy_yaml_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _kube_router_deploy_template_registry['predict-router-split-gpu'][0][0]))
        path, filename = _os.path.split(model_router_deploy_yaml_templates_path)
        rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-%s-router-split-gpu-deploy.yaml' % (image_registry_namespace, model_name, model_tag))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'" % (filename, rendered_filename))
            rendered_filenames += [rendered_filename]
    else:
        model_router_deploy_yaml_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _kube_router_deploy_template_registry['predict-router-split'][0][0]))
        path, filename = _os.path.split(model_router_deploy_yaml_templates_path)
        rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
        rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-%s-router-split-deploy.yaml' % (image_registry_namespace, model_name, model_tag))
        with open(rendered_filename, 'wt') as fh:
            fh.write(rendered)
            print("'%s' => '%s'" % (filename, rendered_filename))
            rendered_filenames += [rendered_filename]

    model_router_ingress_yaml_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _kube_router_ingress_template_registry['predict-router-split'][0][0]))
    path, filename = _os.path.split(model_router_ingress_yaml_templates_path)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-router-split-ingress.yaml' % (image_registry_namespace, model_name))
    with open(rendered_filename, 'wt') as fh:
        fh.write(rendered)
        print("'%s' => '%s'" % (filename, rendered_filename))
        rendered_filenames += [rendered_filename]

    model_router_svc_yaml_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _kube_router_svc_template_registry['predict-router-split'][0][0]))
    path, filename = _os.path.split(model_router_svc_yaml_templates_path)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-router-split-svc.yaml' % (image_registry_namespace, model_name))
    with open(rendered_filename, 'wt') as fh:
        fh.write(rendered)
        print("'%s' => '%s'" % (filename, rendered_filename))
        rendered_filenames += [rendered_filename]

    model_router_autoscale_yaml_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _kube_router_autoscale_template_registry['predict-router-split'][0][0]))
    path, filename = _os.path.split(model_router_autoscale_yaml_templates_path)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-%s-router-split-autoscale.yaml' % (image_registry_namespace, model_name, model_tag))
    with open(rendered_filename, 'wt') as fh:
        fh.write(rendered)
        print("'%s' => '%s'" % (filename, rendered_filename))
        rendered_filenames += [rendered_filename]

    return rendered_filenames


def _create_stream_kube_Kubernetes_yaml(model_name,
                                        log_stream_topic,
                                        input_stream_topic,
                                        output_stream_topic,
                                        cluster_namespace=None,
                                        image_registry_namespace=None,
                                        pipeline_templates_path=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_stream_namespace

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    pipeline_templates_path = _os.path.expandvars(pipeline_templates_path)
    pipeline_templates_path = _os.path.expanduser(pipeline_templates_path)
    pipeline_templates_path = _os.path.abspath(pipeline_templates_path)
    pipeline_templates_path = _os.path.normpath(pipeline_templates_path)

    context = {
               'PIPELINE_MODEL_NAME': model_name,
               'PIPELINE_LOG_STREAM_TOPIC': log_stream_topic,
               'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
               'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
               'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
              }

    rendered_filenames = []

    model_stream_svc_yaml_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _kube_stream_svc_template_registry['stream'][0][0]))
    path, filename = _os.path.split(model_stream_svc_yaml_templates_path)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-svc.yaml' % (image_registry_namespace, model_name))
    with open(rendered_filename, 'wt') as fh:
        fh.write(rendered)
        print("'%s' => '%s'" % (filename, rendered_filename))
        rendered_filenames += [rendered_filename]

    model_stream_deploy_yaml_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _kube_stream_deploy_template_registry['stream'][0][0]))
    path, filename = _os.path.split(model_stream_deploy_yaml_templates_path)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-deploy.yaml' % (image_registry_namespace, model_name))
    with open(rendered_filename, 'wt') as fh:
        fh.write(rendered)
        print("'%s' => '%s'" % (filename, rendered_filename))
        rendered_filenames += [rendered_filename]

    return rendered_filenames


def predict_server_shell(
                         model_name,
                         model_tag,
                         model_type,
                         model_runtime=None,
                         model_chip=None,
                         image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    cmd = 'docker exec -it %s bash' % container_name 
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)


def predict_server_push(model_name,
                        model_tag,
                        image_registry_url=None,
                        image_registry_repo=None,
                        image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    cmd = 'docker push %s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)


def predict_server_pull(model_name,
                        model_tag,
                        image_registry_url=None,
                        image_registry_repo=None,
                        image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    cmd = 'docker pull %s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)


def predict_server_start(model_name,
                         model_tag,
                         log_stream_url=None,
                         log_stream_topic=None,
                         input_stream_url=None,
                         input_stream_topic=None,
                         output_stream_url=None,
                         output_stream_topic=None,
                         image_registry_url=None,
                         image_registry_repo=None,
                         image_registry_namespace=None,
                         predict_port='8080',
                         prometheus_port='9090',
                         grafana_port='3000',
                         memory_limit='2G',
                         start_cmd='docker'):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_chip:
        model_chip = _default_model_chip

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    if not log_stream_topic:
        log_stream_topic = '%s-log' % model_name

    if not input_stream_topic:
        input_stream_topic = '%s-input' % model_name

    if not output_stream_topic:
        output_stream_topic = '%s-output' % model_name        

    # Note: We added `serve` to mimic AWS SageMaker and encourage ENTRYPOINT vs CMD as detailed here:  
    #       https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-inference-code.html
    cmd = '%s run -itd -p %s:8080 -p %s:9090 -p %s:3000 -e PIPELINE_LOG_STREAM_URL=%s -e PIPELINE_LOG_STREAM_TOPIC=%s -e PIPELINE_INPUT_STREAM_URL=%s -e PIPELINE_INPUT_STREAM_TOPIC=%s -e PIPELINE_OUTPUT_STREAM_URL=%s -e PIPELINE_OUTPUT_STREAM_TOPIC=%s --name=%s -m %s %s/%s/%s-%s:%s serve' % (start_cmd, predict_port, prometheus_port, grafana_port, log_stream_url, log_stream_topic, input_stream_url, input_stream_topic, output_stream_url, output_stream_topic, container_name, memory_limit, image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)
    print("")
    print("container name: '%s'" % container_name)
    print("predict port: '%s'" % predict_port)
    print("prometheus port: '%s'" % prometheus_port)
    print("grafana port: '%s'" % grafana_port)
    print("")


def predict_server_stop(model_name,
                        model_tag,
                        image_registry_namespace=None,
                        stop_cmd='docker'): 

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    cmd = '%s rm -f %s' % (stop_cmd, container_name)
    print(cmd)
    print("")

    process = _subprocess.call(cmd, shell=True)


def predict_server_logs(model_name,
                        model_tag,
                        image_registry_namespace=None,
                        logs_cmd='docker'):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    cmd = '%s logs -f %s' % (logs_cmd, container_name)
    print(cmd)
    print("")

    process = _subprocess.call(cmd, shell=True)


def _service_rollout(service_name,
                     service_image,
                     service_tag):

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                          pretty=True)
        found = False
        deployments = response.items
        for deployment in deployments:
            if service_name in deployment.metadata.name:
                found = True
                break
        if found:
            print("")
            print("Upgrading service '%s' using Docker image '%s:%s'." % (deployment.metadata.name, service_image, service_tag))
            print("")
            cmd = "kubectl set image deploy %s %s=%s:%s" % (deployment.metadata.name, deployment.metadata.name, service_image, service_tag)
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
            cmd = "kubectl rollout status deploy %s" % deployment.metadata.name
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
            cmd = "kubectl rollout history deploy %s" % deployment.metadata.name
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
        else:
            print("")
            print("Service '%s' is not running." % service_name)
            print("")


def _service_history(
                     service_name):

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                          pretty=True)
        found = False
        deployments = response.items
        for deployment in deployments:
            if service_name in deployment.metadata.name:
                found = True
                break
        if found:
            print("")
            cmd = "kubectl rollout status deploy %s" % deployment.metadata.name
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
            cmd = "kubectl rollout history deploy %s" % deployment.metadata.name
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
        else:
            print("")
            print("Service '%s' is not running." % service_name)
            print("")


def _service_rollback(
                      service_name,
                      revision=None):

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                          pretty=True)
        found = False
        deployments = response.items
        for deployment in deployments:
            if service_name in deployment.metadata.name:
                found = True
                break
        if found:
            print("")
            if revision:
                print("Rolling back app '%s' to revision '%s'." % deployment.metadata.name, revision)
                cmd = "kubectl rollout undo deploy %s --to-revision=%s" % (deployment.metadata.name, revision)
            else:
                print("Rolling back app '%s'." % deployment.metadata.name)
                cmd = "kubectl rollout undo deploy %s" % deployment.metadata.name
            print("")
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
            cmd = "kubectl rollout status deploy %s" % deployment.metadata.name
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
            cmd = "kubectl rollout history deploy %s" % deployment.metadata.name
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
        else:
            print("")
            print("Service '%s' is not running." % service_name)
            print("")


def _filter_tar(
                tarinfo):
    ignore_list = []
    for ignore in ignore_list:
        if ignore in tarinfo.name:
            return None

    return tarinfo


def _tar(model_name,
         model_tag,
         model_type,
         model_runtime,
         model_chip,
         model_path,
         tar_path='.',
         filemode='w',
         compression='gz'):

    model_tag = _validate_and_prep_model_tag(model_tag)

    model_path = _os.path.expandvars(model_path)
    model_path = _os.path.expanduser(model_path)
    model_path = _os.path.abspath(model_path)
    model_path = _os.path.normpath(model_path)

    tar_path = _os.path.expandvars(tar_path)
    tar_path = _os.path.expanduser(tar_path)
    tar_path = _os.path.abspath(tar_path)
    tar_path = _os.path.normpath(tar_path)

    tar_filename = '%s-%s.tar.gz' % (model_name, model_tag)
    tar_path = _os.path.join(tar_path, tar_filename) 

    print("")
    print("Compressing model_path '%s' into tar_path '%s'." % (model_path, tar_path))

    with _tarfile.open(tar_path, '%s:%s' % (filemode, compression)) as tar:
        tar.add(model_path, arcname='.', filter=_filter_tar)
    
    return tar_path


@app.route("/predict-kube-start/<string:model_name>/<string:model_tag>/<string:model_type>/", methods=['GET'])
def predict_kube_start(   model_name,
                          model_tag,
                          model_type,
                          model_runtime=None,
                          model_chip=None,
                          log_stream_url=None,
                          log_stream_topic=None,
                          input_stream_url=None,
                          input_stream_topic=None,
                          output_stream_url=None,
                          output_stream_topic=None,
                          memory_limit='2Gi',
                          core_limit='1000m',
                          target_core_util_percentage='75',
                          min_replicas='1',
                          max_replicas='1',
                          cluster_namespace=None,
                          image_registry_url=None,
                          image_registry_repo=None,
                          image_registry_namespace=None,
                          image_registry_base_tag=None,
                          image_registry_base_chip=None,
                          pipeline_templates_path=None,
                          timeout_seconds=1200):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    if not image_registry_base_tag:
        image_registry_base_tag = _default_image_registry_base_tag

    if not image_registry_base_chip:
        image_registry_base_chip = _default_model_chip

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    rendered_yamls = _create_predict_kube_Kubernetes_yaml(
                                      model_name=model_name,
                                      model_tag=model_tag,
                                      model_type=model_type,
                                      model_runtime=model_runtime,
                                      model_chip=model_chip,
                                      log_stream_url=log_stream_url,
                                      log_stream_topic=log_stream_topic,
                                      input_stream_url=input_stream_url,
                                      input_stream_topic=input_stream_topic,
                                      output_stream_url=output_stream_url,
                                      output_stream_topic=output_stream_topic,
                                      memory_limit=memory_limit,
                                      core_limit=core_limit,
                                      target_core_util_percentage=target_core_util_percentage,
                                      min_replicas=min_replicas,
                                      max_replicas=max_replicas,
                                      image_registry_url=image_registry_url,
                                      image_registry_repo=image_registry_repo,
                                      image_registry_namespace=image_registry_namespace,
                                      image_registry_base_tag=image_registry_base_tag,
                                      image_registry_base_chip=image_registry_base_chip,
                                      pipeline_templates_path=pipeline_templates_path)

    for rendered_yaml in rendered_yamls:
        # For now, only handle '-deploy' and '-svc' and '-ingress' (not autoscale or routerules)
        if ('-stream-deploy' not in rendered_yaml and '-stream-svc' not in rendered_yaml) and ('-deploy' in rendered_yaml or '-svc' in rendered_yaml or '-ingress' in rendered_yaml):
            _istio_apply(yaml_path=rendered_yaml,
                         cluster_namespace=cluster_namespace)

    return ""


def predict_kafka_start(model_name,
                        log_stream_topic=None,
                        input_stream_topic=None,
                        output_stream_topic=None,
                        cluster_namespace=None,
                        image_registry_namespace=None,
                        pipeline_templates_path=None,
                        timeout_seconds=1200):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_stream_namespace

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    if not log_stream_topic:
        log_stream_topic = '%s-log' % model_name

    if not input_stream_topic:
        input_stream_topic = '%s-input' % model_name

    if not output_stream_topic:
        output_stream_topic = '%s-output' % model_name

    rendered_yamls = _create_stream_kube_Kubernetes_yaml(
                                      model_name=model_name,
                                      log_stream_topic=log_stream_topic,
                                      input_stream_topic=input_stream_topic,
                                      output_stream_topic=output_stream_topic,
                                      image_registry_namespace=image_registry_namespace,
                                      pipeline_templates_path=pipeline_templates_path)

    for rendered_yaml in rendered_yamls:
        _kube_apply(yaml_path=rendered_yaml,
                         cluster_namespace=cluster_namespace)


def predict_kafka_describe(model_name,
                           cluster_namespace=None,
                           image_registry_namespace=None,
                           timeout_seconds=15):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_stream_namespace

    service_name = "%s-%s" % (image_registry_namespace, model_name)
    stream_url = _get_cluster_service(service_name=service_name,
                                           cluster_namespace=cluster_namespace)

    full_stream_url = 'http://%s/topics' % stream_url

    print("")
    print("Describing stream at '%s'." % full_stream_url)
    print("")

    response = _requests.get(url=full_stream_url,
                            timeout=timeout_seconds)

    if response.text:
        print("")
        _pprint(response.text)

    return response.text

@app.route("/predict-kafka-consume/<string:model_name>/<string:stream_topic>/", methods=['GET'])
def predict_kafka_consume(model_name,
                          stream_topic,
                          stream_consumer_name=None,
                          stream_offset=None,
                          cluster_namespace=None,
                          image_registry_namespace=None,
                          timeout_seconds=15):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not stream_offset:
        stream_offset = "earliest"

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_stream_namespace

    service_name = "%s-%s" % (image_registry_namespace, model_name)
    stream_url = _get_cluster_service(service_name=service_name,
                                           cluster_namespace=cluster_namespace)

    if not stream_consumer_name:
        stream_consumer_name = '%s-%s' % (model_name, stream_topic)

    full_stream_url = 'http://%s/consumers/%s' % (stream_url, stream_consumer_name)

    print("")
    print("Consuming stream topic '%s' at '%s' as consumer id '%s'." % (stream_topic, full_stream_url, stream_consumer_name))
    print("")


    # Register consumer
    content_type_headers = {"Content-Type": "application/vnd.kafka.json.v2+json"}
    accept_headers = {"Accept": "application/vnd.kafka.json.v2+json"}
    
    body = '{"name": "%s", "format": "json", "auto.offset.reset": "%s"}' % (stream_consumer_name, stream_offset)

    response = _requests.post(url=full_stream_url,
                             headers=content_type_headers,
                             data=body.encode('utf-8'),
                             timeout=timeout_seconds)

    if response.text:
        print("")
        _pprint(response.text)


    # Subscribe consumer to topic
    body = '{"topics": ["%s"]}' % stream_topic
    full_stream_url = 'http://%s/consumers/%s/instances/%s/subscription' % (stream_url, stream_consumer_name, stream_consumer_name)
    response = _requests.post(url=full_stream_url,
                             headers=content_type_headers,
                             data=body.encode('utf-8'),
                             timeout=timeout_seconds)

    if response.text:
        print("")
        _pprint(response.text)


    # Get consumer topic subscription
    full_stream_url = 'http://%s/consumers/%s/instances/%s/subscription' % (stream_url, stream_consumer_name, stream_consumer_name)
    response = _requests.get(url=full_stream_url,
                            headers=accept_headers,
                            timeout=timeout_seconds)

    if response.text:
        print("")
        _pprint(response.text)


    # Consume messages from topic
    full_stream_url = 'http://%s/consumers/%s/instances/%s/records' % (stream_url, stream_consumer_name, stream_consumer_name)

    response = _requests.get(url=full_stream_url,
                            headers=accept_headers,
                            timeout=timeout_seconds)

    messages = response.text

    if response.text:
        print("")
        _pprint(response.text)


    # Remove consumer subscription from topic
    full_stream_url = 'http://%s/consumers/%s/instances/%s' % (stream_url, stream_consumer_name, stream_consumer_name)

    response = _requests.delete(url=full_stream_url,
                               headers=content_type_headers,
                               timeout=timeout_seconds)

    if response.text:
        print("")
        _pprint(response.text)

    return messages


# TODO:  Make a _single version
def predict_kafka_test(model_name,
                       test_request_path,
                       log_stream_topic=None,
                       input_stream_topic=None,
                       output_stream_topic=None,
                       cluster_namespace=None,
                       image_registry_namespace=None,
                       test_request_concurrency=1,
                       test_request_mime_type='application/json',
                       test_response_mime_type='application/json',
                       test_request_timeout_seconds=15):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_stream_namespace

    if not log_stream_topic:
        log_stream_topic = '%s-log' % model_name

    if not input_stream_topic:
        input_stream_topic = '%s-input' % model_name

    if not output_stream_topic:
        output_stream_topic = '%s-output' % model_name

    service_name = "%s-%s" % (image_registry_namespace, model_name)

    stream_url = _get_cluster_service(service_name=service_name,
                                      cluster_namespace=cluster_namespace)

    full_stream_url = 'http://%s/topics/%s' % (stream_url, input_stream_topic)

    print("")
    print("Producing stream for topic '%s' at '%s'." % (input_stream_topic, full_stream_url))
    print("")

    # Register consumer
    accept_and_content_type_headers = {"Accept": "application/vnd.kafka.v2+json", "Content-Type": "application/vnd.kafka.json.v2+json"}

    with open(test_request_path, 'rt') as fh:
        model_input_text = fh.read()

    body = '{"records": [{"value":%s}]}' % model_input_text

    response = _requests.post(url=full_stream_url,
                             headers=accept_and_content_type_headers,
                             data=body.encode('utf-8'),
                             timeout=test_request_timeout_seconds)

    if response.text:
        print("")
        _pprint(response.text)

#    return predict_kafka_consume(model_name,
#                                 output_stream_topic) 


def _predict_server_deploy(model_name,
                           model_tag,
                           model_type,
                           model_runtime,
                           model_chip,
                           model_path,
                           deploy_server_url,
                           timeout_seconds=1200):

    model_tag = _validate_and_prep_model_tag(model_tag)

    model_path = _os.path.expandvars(model_path)
    model_path = _os.path.expanduser(model_path)
    model_path = _os.path.abspath(model_path)
    model_path = _os.path.normpath(model_path)

    tar_path = _tar(model_type=model_type,
                    model_name=model_name,
                    model_tag=model_tag,
                    model_runtime=model_runtime,
                    model_chip=model_chip,
                    model_path=model_path,
                    tar_path='.',
                    filemode='w',
                    compression='gz')

    upload_key = 'file'
    upload_value = tar_path 

    full_model_deploy_url = "%s/api/%s/model/deploy/%s/%s/%s/%s/%s" % (deploy_server_url.rstrip('/'), _pipeline_api_version, model_name, model_tag, model_type, model_runtime, model_chip) 

    with open(tar_path, 'rb') as fh:
        files = [(upload_key, (upload_value, fh))]
        print("")
        print("Deploying model tar.gz '%s' to '%s'." % (tar_path, full_model_deploy_url))
        headers = {'Accept': 'application/json'}
        try:
            response = _requests.post(url=full_model_deploy_url, 
                                     headers=headers, 
                                     files=files, 
                                     timeout=timeout_seconds)

            if response.status_code != _requests.codes.ok:
                if response.text:
                    print("")
                    _pprint(response.text)

            if response.status_code == _requests.codes.ok:
                print("")
                print("Success!")
                print("")
            else:
                response.raise_for_status()
                print("")
        except _requests.exceptions.HTTPError as hte:
            print("Error while deploying model.\nError: '%s'" % str(hte))
            print("")
        except IOError as ioe:
            print("Error while deploying model.\nError: '%s'" % str(ioe))
            print("")

    if (_os.path.isfile(tar_path)):
        print("")
        print("Cleaning up temporary file tar '%s'..." % tar_path)
        print("")
        os.remove(tar_path)


def _optimize_predict(model_name,
                      model_tag,
                      model_type,
                      model_runtime,
                      model_chip,
                      model_path,
                      input_path,
                      input_host_path,
                      output_path,
                      output_host_path,
                      optimize_type,
                      optimize_params):

    model_tag = _validate_and_prep_model_tag(model_tag)

    model_path = _os.path.expandvars(model_path)
    model_path = _os.path.expanduser(model_path)
    model_path = _os.path.abspath(model_path)
    model_path = _os.path.normpath(model_path)


def _optimize_train(
             model_name,
             model_tag,
             model_type,
             model_runtime,
             model_chip,
             model_path,
             input_path,
             input_host_path,
             output_path,
             output_host_path,
             optimize_type,
             optimize_params):

    model_tag = _validate_and_prep_model_tag(model_tag)

    model_path = _os.path.expandvars(model_path)
    model_path = _os.path.expanduser(model_path)
    model_path = _os.path.abspath(model_path)
    model_path = _os.path.normpath(model_path)


def predict_server_test(model_endpoint_url,
                        test_request_path,
                        model_name=None,
                        model_tag=None,
                        model_type=None,
                        model_runtime=None,
                        model_chip=None,
                        test_request_concurrency=1,
                        test_request_mime_type='application/json',
                        test_response_mime_type='application/json',
                        test_request_timeout_seconds=15):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=test_request_concurrency) as executor:
        for _ in range(test_request_concurrency):
            executor.submit(predict_http_test(
                                          model_endpoint_url=model_endpoint_url,
                                          test_request_path=test_request_path,
                                          model_name=model_name,
                                          model_tag=model_tag,
                                          model_type=model_type,
                                          model_runtime=model_runtime,
                                          model_chip=model_chip,
                                          test_request_mime_type=test_request_mime_type,
                                          test_response_mime_type=test_response_mime_type,
                                          test_request_timeout_seconds=test_request_timeout_seconds))


# Specify model_endpoint_url if you have a specific model_endpoint_url, otherwise uses Kube to figure it out
def predict_kube_test(
                      model_name,
                      test_request_path,
                      model_tag=None,
                      model_type=None,
                      model_runtime=None,
                      model_chip=None,
                      image_registry_namespace=None,
                      cluster_namespace=None,
                      test_request_concurrency=1,
                      test_request_mime_type='application/json',
                      test_response_mime_type='application/json',
                      test_request_timeout_seconds=15):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    model_endpoint_url = _get_model_endpoint(model_name,
                                             cluster_namespace=cluster_namespace,
                                             image_registry_namespace=image_registry_namespace)

    # This is required to get around the limitation of istio managing only 1 load balancer
    # See here for more details: https://github.com/istio/istio/issues/1752
    # If this gets fixed, we can relax the -routerules.yaml and -ingress.yaml in the templates dir
    #   (we'll no longer need to scope by model_name)

    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=test_request_concurrency) as executor:
        for _ in range(test_request_concurrency):
            executor.submit(predict_http_test(model_endpoint_url=model_endpoint_url,
                                              test_request_path=test_request_path,
                                              model_name=model_name,
                                              model_tag=model_tag,
                                              model_type=model_type,
                                              model_runtime=model_runtime,
                                              model_chip=model_chip,
                                              test_request_mime_type=test_request_mime_type,
                                              test_response_mime_type=test_response_mime_type,
                                              test_request_timeout_seconds=test_request_timeout_seconds))


def predict_http_test(model_endpoint_url,
                      test_request_path,
                      model_name=None,
                      model_tag=None,
                      model_type=None,
                      model_runtime=None,
                      model_chip=None,
                      test_request_mime_type='application/json',
                      test_response_mime_type='application/json',
                      test_request_timeout_seconds=15):

    model_tag = _validate_and_prep_model_tag(model_tag)

    test_request_path = _os.path.expandvars(test_request_path)
    test_request_path = _os.path.expanduser(test_request_path)
    test_request_path = _os.path.abspath(test_request_path)
    test_request_path = _os.path.normpath(test_request_path)

    full_model_endpoint_url = model_endpoint_url.rstrip('/')
    print("")
    print("Predicting with file '%s' using '%s'" % (test_request_path, full_model_endpoint_url))
    print("")

    with open(test_request_path, 'rb') as fh:
        model_input_binary = fh.read()

    headers = {'Content-type': test_request_mime_type, 'Accept': test_response_mime_type} 
    from datetime import datetime 

    begin_time = datetime.now()
    response = _requests.post(url=full_model_endpoint_url, 
                             headers=headers, 
                             data=model_input_binary, 
                             timeout=test_request_timeout_seconds)
    end_time = datetime.now()

    if response.text:
        print("")
        _pprint(response.text)

    if response.status_code == _requests.codes.ok:
        print("")
        print("Success!")
    else:
        print(response.status_code)

    total_time = end_time - begin_time
    print("")
    print("Request time: %s milliseconds" % (total_time.microseconds / 1000))
    print("")


def predict_sage_test(model_name,
                      test_request_path,
                      model_tag=None,
                      model_type=None,
                      model_runtime=None,
                      model_chip=None,
                      test_request_concurrency=1,
                      test_request_mime_type='application/json',
                      test_response_mime_type='application/json',
                      test_request_timeout_seconds=15):

    from concurrent.futures import ThreadPoolExecutor, as_completed

    with ThreadPoolExecutor(max_workers=test_request_concurrency) as executor:
        for _ in range(test_request_concurrency):
            executor.submit(_test_single_prediction_sage(
                                          model_name=model_name,
                                          test_request_path=test_request_path,
                                          model_tag=model_tag,
                                          model_type=model_type,
                                          model_runtime=model_runtime,
                                          model_chip=model_chip,
                                          test_request_mime_type=test_request_mime_type,
                                          test_response_mime_type=test_response_mime_type,
                                          test_request_timeout_seconds=test_request_timeout_seconds))


def _test_single_prediction_sage(
                                 model_name,
                                 test_request_path,
                                 model_tag=None,
                                 model_type=None,
                                 model_runtime=None,
                                 model_chip=None,
                                 image_registry_namespace=None,
                                 test_request_mime_type='application/json',
                                 test_response_mime_type='application/json',
                                 test_request_timeout_seconds=15):

    model_tag = _validate_and_prep_model_tag(model_tag)

    test_request_path = _os.path.expandvars(test_request_path)
    test_request_path = _os.path.expanduser(test_request_path)
    test_request_path = _os.path.abspath(test_request_path)
    test_request_path = _os.path.normpath(test_request_path)

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    print("")
    print("Predicting with file '%s' using endpoint '%s-%s'" % (test_request_path, image_registry_namespace, model_name))
    print("")

    with open(test_request_path, 'rb') as fh:
        model_input_binary = fh.read()

    from datetime import datetime

    begin_time = datetime.now()
    body = model_input_binary.decode('utf-8')

    sagemaker_client = _boto3.client('runtime.sagemaker')
    response = sagemaker_client.invoke_endpoint(
                                          EndpointName='%s-%s' % (image_registry_namespace, model_name),
                                          Body=model_input_binary,
                                          ContentType=test_request_mime_type,
                                          Accept=test_response_mime_type)
    end_time = datetime.now()

    if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("")
        print("Variant: '%s'" % response['InvokedProductionVariant'])
        print("")
        _pprint(response['Body'].read().decode('utf-8'))
   
        print("")
        print("Success!")
        print("")
    else:
        exit(1)

    total_time = end_time - begin_time
    print("")
    print("Request time: %s milliseconds" % (total_time.microseconds / 1000))
    print("")


#def train_kube_status():
#    _cluster_status()


#def predict_kube_status():
#    _cluster_status()


def _cluster_status():
    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    print("")
    print("Versions")
    print("********")
    version()

    print("")
    print("Nodes")
    print("*****")
    _get_all_nodes()

    _environment_volumes()

    print("")
    print("Environment Resources")
    print("*********************")        
    _environment_resources()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_service_for_all_namespaces(watch=False,
                                                                 pretty=True)
        services = response.items
        for svc in services:
            _service_resources(service_name=svc.metadata.name)

    print("")
    print("Service Descriptions")
    print("********************")
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_service_for_all_namespaces(watch=False,
                                                                 pretty=True)
        services = response.items
        for svc in services:
            _service_describe(service_name=svc.metadata.name)

    print("")
    print("DNS Internal (Public)")
    print("*********************")
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_service_for_all_namespaces(watch=False, 
                                                                 pretty=True)
        services = response.items
        for svc in services:
            ingress = 'Not public' 
            if svc.status.load_balancer.ingress and len(svc.status.load_balancer.ingress) > 0:
                if (svc.status.load_balancer.ingress[0].hostname):
                    ingress = svc.status.load_balancer.ingress[0].hostname
                if (svc.status.load_balancer.ingress[0].ip):
                    ingress = svc.status.load_balancer.ingress[0].ip               
            print("%s (%s)" % (svc.metadata.name, ingress))

    print("")
    print("Deployments")
    print("***********")
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False,
                                                                          pretty=True)
        deployments = response.items
        for deployment in deployments:
            print("%s (Available Replicas: %s)" % (deployment.metadata.name, deployment.status.available_replicas))

    print("")
    print("Pods")
    print("****")
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, 
                                                             pretty=True)
        pods = response.items
        for pod in pods:
            print("%s (%s)" % (pod.metadata.name, pod.status.phase))

    print("")
    print("Note:  If you are using Minikube, use 'minikube service list'.")
    print("")

    predict_kube_describe()


def _get_pod_by_service_name(
                             service_name):

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    found = False 
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, pretty=True)
        pods = response.items
        for pod in pods:
            if service_name in pod.metadata.name:
                found = True
                break
    if found:
        return pod
    else:
        return None


def _get_svc_by_service_name(
                             service_name):

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    found = False
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_service_for_all_namespaces(watch=False, 
                                                                 pretty=True)
        services = response.items
        for svc in services:
            if service_name in svc.metadata.name:
                found = True
                break
    if found:
        return svc 
    else:
        return None


def _get_all_available_services():

    available_services = list(_kube_deploy_registry.keys())
    available_services.sort()
    for service in available_services:
        print(service)


def _get_all_nodes():

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_node(watch=False, pretty=True)
        nodes = response.items
        for node in nodes:
            print("%s" % node.metadata.labels['kubernetes.io/hostname'])


def predict_kube_shell(model_name,
                       model_tag,
                       model_type,
                       model_runtime=None,
                       model_chip=None,
                       cluster_namespace=None,
                       image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip: 
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_shell(service_name=service_name,
                        cluster_namespace=cluster_namespace)


def _service_shell(service_name,
                   cluster_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, 
                                                             pretty=True)
        pods = response.items
        for pod in pods:
            if service_name in pod.metadata.name:
                break
        print("")
        print("Connecting to '%s'" % pod.metadata.name)      
        print("")
        _subprocess.call("kubectl exec -it %s bash" % pod.metadata.name, shell=True)
    print("")


def predict_kube_logs(model_name,
                      model_tag,
                      model_type,
                      model_runtime=None,
                      model_chip=None,
                      cluster_namespace=None,
                      image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_logs(service_name=service_name,
                       cluster_namespace=cluster_namespace)


def _service_logs(
                  service_name,
                  cluster_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_pod_for_all_namespaces(watch=False, 
                                                             pretty=True)
        found = False
        pods = response.items
        for pod in pods:
            if service_name in pod.metadata.name:
                found = True
                break
        if found:
            print("")
            print("Tailing logs on '%s'." % pod.metadata.name)
            print("")
            _subprocess.call("kubectl logs -f %s" % pod.metadata.name, shell=True)
            print("")
        else:
            print("")
            print("Service '%s' is not running." % service_name)
            print("")


def _service_describe(
                      service_name):

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_pod_for_all_namespaces(watch=False,
                                                             pretty=True)
        pods = response.items
        for pod in pods:
            if service_name in pod.metadata.name:
                break
        print("")
        print("Connecting to '%s'" % pod.metadata.name)
        print("")
        _subprocess.call("kubectl describe pod %s" % pod.metadata.name, shell=True)
    print("")


def predict_kube_scale(
                       model_name,
                       model_tag,
                       model_type,
                       replicas,
                       model_runtime=None,
                       model_chip=None,
                       cluster_namespace=None,
                       image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_scale(service_name=service_name,
                        replicas=replicas,
                        cluster_namespace=cluster_namespace)


# TODO:  See https://github.com/istio/istio/tree/master/samples/helloworld
#             for more details on how istio + autoscaling work
def predict_kube_autoscale(
                              model_name,
                              model_tag,
                              model_type,
                              cpu_percent,
                              min_replicas,
                              max_replicas,
                              model_runtime=None,
                              model_chip=None,
                              cluster_namespace=None,
                              image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    # TODO:  make sure resources/requests/cpu has been set to something in the yaml
    #        ie. istioctl kube-inject -f helloworld.yaml -o helloworld-istio.yaml
    #        then manually edit as follows:
    #
    #  resources:
    #    requests:
    #      cpu: 100m

    cmd = "kubectl autoscale deployment %s-%s-%s --cpu-percent=%s --min=%s --max=%s" % (image_registry_namespace, model_name, model_tag, cpu_percent, min_replicas, max_replicas)
    print("")
    print("Running '%s'." % cmd)
    print("")
    _subprocess.call(cmd, shell=True)
    cmd = "kubectl get hpa"
    print("")
    print("Running '%s'." % cmd)
    print("")
    _subprocess.call(cmd, shell=True)
    print("")


def _service_scale(
                   service_name,
                   replicas,
                   cluster_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    # TODO:  Filter by namespace
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False, 
                                                                          pretty=True)
        found = False
        deployments = response.items
        for deploy in deployments:
            if service_name in deploy.metadata.name:
                found = True
                break
        if found:
            print("")
            print("Scaling service '%s' to '%s' replicas." % (deploy.metadata.name, replicas))
            print("")
            cmd = "kubectl scale deploy %s --replicas=%s --namespace=%s" % (deploy.metadata.name, replicas, cluster_namespace)
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
        else:
            print("")
            print("Service '%s' is not running." % service_name)
            print("") 


def _environment_volumes():

    print("")
    print("Volumes")
    print("*******")
    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_persistent_volume(watch=False,
                                                        pretty=True)
        claims = response.items
        for claim in claims:
            print("%s" % (claim.metadata.name))

    print("")
    print("Volume Claims")
    print("*************")
    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1.list_persistent_volume_claim_for_all_namespaces(watch=False,
                                                                                 pretty=True)
        claims = response.items
        for claim in claims:
            print("%s" % (claim.metadata.name))


def _get_deploy_yamls( 
                      service_name):
    try:
        (deploy_yamls, dependencies) = _kube_deploy_registry[service_name]
    except:
        dependencies = []
        deploy_yamls = []

    if len(dependencies) > 0:
        for dependency in dependencies:
            deploy_yamls = deploy_yamls + _get_deploy_yamls(service_name=dependency)

    return deploy_yamls 


def _get_svc_yamls( 
                   service_name):
    try:
        (svc_yamls, dependencies) = _kube_svc_registry[service_name]
    except:
        dependencies = []
        svc_yamls = []
   
    if len(dependencies) > 0:
        for dependency_service_name in dependencies:
            svc_yamls = svc_yamls + _get_svc_yamls(service_name=dependency_service_name)

    return svc_yamls


def _kube_apply(
                yaml_path,
                cluster_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    yaml_path = _os.path.normpath(yaml_path)

    cmd = "kubectl apply --namespace %s -f %s" % (cluster_namespace, yaml_path)
    _kube(cmd=cmd)


def _kube_create(
                 yaml_path,
                 cluster_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    yaml_path = _os.path.normpath(yaml_path)

    cmd = "kubectl create --namespace %s -f %s --save-config --record" % (cluster_namespace, yaml_path)
    _kube(cmd=cmd)


def _kube_delete(
                 yaml_path,
                 cluster_namespace=None):

    yaml_path = _os.path.normpath(yaml_path)

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    cmd = "kubectl delete --namespace %s -f %s" % (cluster_namespace, yaml_path)
    _kube(cmd=cmd) 


def _kube( cmd):
    print("")
    print("Running '%s'." % cmd)
    print("")
    _subprocess.call(cmd, shell=True)
    print("")


def predict_kube_describe():
    print("")
    print("Traffic Ingress")
    print("***************")
    cmd = "kubectl get ingress -o wide --all-namespaces"
    _subprocess.call(cmd, shell=True)

    print("")
    print("Traffic Route Rules")
    print("********************")
    cmd = "kubectl get routerules -o wide --all-namespaces"
    _subprocess.call(cmd, shell=True)

    print("")
    cmd = "kubectl describe routerules --all-namespaces"
    _subprocess.call(cmd, shell=True)
    print("")


def _get_model_endpoint(model_name,
                        cluster_namespace=None,
                        image_registry_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    ingress_name = '%s-%s' % (image_registry_namespace, model_name)

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        ingress = kubeclient_v1_beta1.read_namespaced_ingress(name=ingress_name, 
                                                              namespace=cluster_namespace)

        endpoint = None
        if ingress.status.load_balancer.ingress and len(ingress.status.load_balancer.ingress) > 0:
            if (ingress.status.load_balancer.ingress[0].hostname):
                endpoint = ingress.status.load_balancer.ingress[0].hostname
            if (ingress.status.load_balancer.ingress[0].ip):
                endpoint = ingress.status.load_balancer.ingress[0].ip

        path = ingress.spec.rules[0].http.paths[0].path
        endpoint = 'http://%s%s' % (endpoint, path)
        endpoint = endpoint.replace(".*", "invocations")

        return endpoint


def _get_all_model_endpoints(cluster_namespace=None,
                             image_registry_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    endpoint_list = []
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        ingresses = kubeclient_v1_beta1.list_namespaced_ingress(namespace=cluster_namespace)
        for ingress in ingresses.items:
            endpoint = None
            if ingress.status.load_balancer.ingress and len(ingress.status.load_balancer.ingress) > 0:
                if (ingress.status.load_balancer.ingress[0].hostname):
                    endpoint = ingress.status.load_balancer.ingress[0].hostname
                if (ingress.status.load_balancer.ingress[0].ip):
                    endpoint = ingress.status.load_balancer.ingress[0].ip

            path = ingress.spec.rules[0].http.paths[0].path
            endpoint = 'http://%s%s' % (endpoint, path)
            endpoint = endpoint.replace(".*", "invocations")
            endpoint_list += [endpoint]

    return endpoint_list


def _get_cluster_service(service_name,
                         cluster_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    endpoint = None
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        service = kubeclient_v1.read_namespaced_service(name=service_name,
                                                        namespace=cluster_namespace)

        if service.status.load_balancer.ingress and len(service.status.load_balancer.ingress) > 0:
            if (service.status.load_balancer.ingress[0].hostname):
                endpoint = service.status.load_balancer.ingress[0].hostname
            if (service.status.load_balancer.ingress[0].ip):
                endpoint = service.status.load_balancer.ingress[0].ip

    return endpoint


def _istio_apply(yaml_path,
                 cluster_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    yaml_path = _os.path.normpath(yaml_path)

    cmd = "istioctl kube-inject -f %s" % yaml_path
    print("")
    print("Running '%s'." % cmd)
    print("")
    new_yaml_bytes = _subprocess.check_output(cmd, shell=True)
    new_yaml_path = '%s-istio' % yaml_path
    with open(new_yaml_path, 'wt') as fh:
        fh.write(new_yaml_bytes.decode('utf-8'))
        print("'%s' => '%s'" % (yaml_path, new_yaml_path))
    print("")

    cmd = "kubectl apply --namespace %s -f %s" % (cluster_namespace, new_yaml_path)
    print("")
    print("Running '%s'." % cmd)
    print("")
    _subprocess.call(cmd, shell=True)
    print("")


@app.route("/predict-kube-route/<string:model_name>/<string:model_tag_and_weight_dict>/", methods=['GET'])
def predict_kube_route(model_name,
#                       model_type,
                       model_tag_and_weight_dict,
#                       model_runtime=None,
#                       model_chip=None,
                       traffic_type='split',
                       pipeline_templates_path=None,
                       image_registry_namespace=None,
                       cluster_namespace=None):

    if type(model_tag_and_weight_dict) is str:
        model_tag_and_weight_dict = _base64.b64decode(model_tag_and_weight_dict) 
        model_tag_and_weight_dict = _json.loads(model_tag_and_weight_dict)

#    if request.method == 'PUT':
#        post_data= str(request.data.get('text', ''))
#        idx = max(notes.keys()) + 1
#        notes[idx] = note
#        return model_name, status.HTTP_200_OK

#    if not model_runtime:
#        model_runtime = _get_default_model_runtime(model_type)

#    if not model_chip:
#        model_chip = _default_model_chip

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

#    if len(model_tag_list) != len(model_weight_list):
#        print("`model_tag_list` and `model_weight_list` must be the same length.  The `model_weight_list` should consist of integers or floats between 0 and 100.  All weights should total 100.")
#        print("")
#        return

    _validate_and_prep_model_tag_and_weight_dict(model_tag_and_weight_dict)

    model_tag_list = [ _validate_and_prep_model_tag(model_tag) for model_tag in model_tag_and_weight_dict.keys() ]

    model_weight_list = list(model_tag_and_weight_dict.values())

    context = {'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
               'PIPELINE_MODEL_NAME': model_name,
#               'PIPELINE_MODEL_TYPE': model_type,
#               'PIPELINE_MODEL_RUNTIME': model_runtime,
#               'PIPELINE_MODEL_CHIP': model_chip,
               'PIPELINE_MODEL_TAG_LIST': model_tag_list,
               'PIPELINE_MODEL_WEIGHT_LIST': model_weight_list,
               'PIPELINE_MODEL_NUM_TAGS_AND_WEIGHTS': len(model_tag_list)}

    model_router_routerules_yaml_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _kube_router_routerules_template_registry['predict-router-split'][0][0]))
    path, filename = _os.path.split(model_router_routerules_yaml_templates_path)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    tag_weight_filename_snippet = '' 
    for idx in range(len(model_tag_list)):
        tag_weight_filename_snippet = '%s-%s-%s' % (tag_weight_filename_snippet, model_tag_list[idx], model_weight_list[idx])

    tag_weight_filename_snippet = tag_weight_filename_snippet.lstrip('-')
    tag_weight_filename_snippet = tag_weight_filename_snippet.rstrip('-')

    rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-%s-router-split-routerules.yaml' % (image_registry_namespace, model_name, tag_weight_filename_snippet))
    with open(rendered_filename, 'wt') as fh:
        fh.write(rendered)
        print("'%s' => '%s'." % (filename, rendered_filename))

    _kube_apply(rendered_filename, cluster_namespace)

    return "" 


def predict_sage_route(model_name,
#                       model_type,
                       model_tag_and_weight_dict,
#                       model_runtime=None,
#                       model_chip=None,
                       router_type='split',
                       pipeline_templates_path=None,
                       image_registry_namespace=None):

    if type(model_tag_and_weight_dict) is str:
        model_tag_and_weight_dict = _base64.b64decode(model_tag_and_weight_dict)
        model_tag_and_weight_dict = _json.loads(model_tag_and_weight_dict)

#    if not model_runtime:
#        model_runtime = _get_default_model_runtime(model_type)

#    if not model_chip:
#        model_chip = _default_model_chip

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    _validate_and_prep_model_tag_and_weight_dict(model_tag_and_weight_dict)

    model_tag_list = [ _validate_and_prep_model_tag(model_tag) for model_tag in model_tag_and_weight_dict.keys() ]

    tag_weight_dict_list = [] 

    for model_tag in model_tag_list:
        tag_weight_dict = {
            'VariantName': '%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
            'DesiredWeight': model_tag_and_weight_dict[model_tag],
            'DesiredInstanceCount': 1
        }

        tag_weight_dict_list += tag_weight_dict

    sagemaker_admin_client = _boto3.client('sagemaker')

    from datetime import datetime

    begin_time = datetime.now()

    response = client.update_endpoint_weights_and_capacities(
        EndpointName='%s-%s' % (image_registry_namespace, model_name),
        DesiredWeightsAndCapacities=tag_weight_dict_list,
    )

    total_time = end_time - begin_time

    if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("")
        print("EndpointArn: '%s'" % response['EndpointArn'])
        print("")
        print("Success!")
        print("")
    else:
        print(response['ResponseMetadata']['HTTPStatusCode'])
        return

    print("")
    print("Request time: %s milliseconds" % (total_time.microseconds / 1000))
    print("")


#(Enterprise) pipeline experiment-add              <-- Add Cluster to Experiment
#             pipeline experiment-start            <-- Start Experiment
#             pipeline experiment-status           <-- Experiment Status (Bandit-based Rewards)
#             pipeline experiment-stop             <-- Stop Experiment
#             pipeline experiment-update           <-- Update Experiment (Bandit-based Routing)

#    def _experiment_start(
#                         experiment_name,
#                         experiment_tag,
#                         experiment_type):
#
#        pass


def _service_start(
                   service_name,
                   pipeline_services_path=None,
                   cluster_namespace=None):

    if not pipeline_services_path:
        pipeline_services_path = _default_pipeline_services_path

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    deploy_yaml_filenames = []
    svc_yaml_filenames = []

    deploy_yaml_filenames = deploy_yaml_filenames + _get_deploy_yamls(service_name=service_name)
    deploy_yaml_filenames = ['%s/%s' % (pipeline_services_path, deploy_yaml_filename) for deploy_yaml_filename in deploy_yaml_filenames]
    print("Using '%s'" % deploy_yaml_filenames)

    svc_yaml_filenames = svc_yaml_filenames + _get_svc_yamls(service_name=service_name)
    svc_yaml_filenames = ['%s/%s' % (pipeline_services_path, svc_yaml_filename) for svc_yaml_filename in svc_yaml_filenames]
    print("Using '%s'" % svc_yaml_filenames)

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    print("")
    print("Starting service '%s'." % service_name)
    print("")
    print("Kubernetes Deployments:")
    print("")
    for deploy_yaml_filename in deploy_yaml_filenames:
        deploy_yaml_filename = _os.path.normpath(deploy_yaml_filename)
        cmd = "kubectl apply -f %s" % deploy_yaml_filename
        print("Running '%s'." % cmd)
        print("")
        _subprocess.call(cmd, shell=True)
        print("")
    print("")
    print("Kubernetes Services:")
    print("")
    for svc_yaml_filename in svc_yaml_filenames:
        svc_yaml_filename = _os.path.normpath(svc_yaml_filename)
        cmd = "kubectl apply -f %s" % svc_yaml_filename
        print("Running '%s'." % cmd)
        print("")
        _subprocess.call(cmd, shell=True)
        print("")
    print("")


def predict_kube_stop(model_name,
                      model_tag,
                      model_type,
                      model_runtime=None,
                      model_chip=None,
                      cluster_namespace=None,
                      image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)
    _service_stop(service_name=service_name, 
                       cluster_namespace=cluster_namespace)


def _service_stop(
                  service_name,
                  cluster_namespace=None):

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    _kubeconfig.load_kube_config()
    kubeclient_v1 = _kubeclient.CoreV1Api()
    kubeclient_v1_beta1 = _kubeclient.ExtensionsV1beta1Api()

    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore")
        response = kubeclient_v1_beta1.list_deployment_for_all_namespaces(watch=False, pretty=True)
        found = False
        deployments = response.items
        for deploy in deployments:
            if service_name in deploy.metadata.name:
                found = True
                break
        if found:
            print("")
            print("Deleting service '%s'." % deploy.metadata.name)
            print("")
            cmd = "kubectl delete deploy %s --namespace %s" % (deploy.metadata.name, cluster_namespace)
            print("Running '%s'." % cmd)
            print("")
            _subprocess.call(cmd, shell=True)
            print("")
        else:
            print("")
            print("Service '%s' is not running." % service_name)
            print("")


def train_server_pull(model_name,
                      model_tag,
                      model_type,
                      model_runtime=None,
                      model_chip=None,
                      image_registry_url=None,
                      image_registry_repo=None,
                      image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    cmd = 'docker pull %s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)


def train_server_push(model_name,
                      model_tag,
                      model_type,
                      model_runtime=None,
                      model_chip=None,
                      image_registry_url=None,
                      image_registry_repo=None,
                      image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    cmd = 'docker push %s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)


def train_server_logs(
                      model_name,
                      model_tag,
                      model_type,
                      model_runtime=None,
                      model_chip=None,
                      image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    cmd = 'docker logs -f %s' % container_name
    print(cmd)
    print("")

    process = _subprocess.call(cmd, shell=True)


def train_server_shell(
                       model_name,
                       model_tag,
                       model_type,
                       model_runtime=None,
                       model_chip=None,
                       image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    cmd = 'docker exec -it %s bash' % container_name 
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)


def _create_train_server_Dockerfile(model_name,
                                    model_tag,
                                    model_type,
                                    model_runtime,
                                    model_chip,
                                    model_path,
                                    build_context_path,
                                    log_stream_url,
                                    log_stream_topic,
                                    input_stream_url,
                                    input_stream_topic,
                                    output_stream_url,
                                    output_stream_topic,
                                    image_registry_url,
                                    image_registry_repo,
                                    image_registry_namespace,
                                    image_registry_base_tag,
                                    image_registry_base_chip,
                                    pipeline_templates_path):

    model_tag = _validate_and_prep_model_tag(model_tag)

    print("")
    print("Using templates in '%s'." % pipeline_templates_path)
    print("(Specify --pipeline-templates-path if the templates live elsewhere.)")
    print("")

    context = {
               'PIPELINE_MODEL_NAME': model_name,
               'PIPELINE_MODEL_TAG': model_tag,
               'PIPELINE_MODEL_TYPE': model_type,
               'PIPELINE_MODEL_RUNTIME': model_runtime,
               'PIPELINE_MODEL_CHIP': model_chip,
               'PIPELINE_MODEL_PATH': model_path,
               'PIPELINE_LOG_STREAM_URL': log_stream_url,
               'PIPELINE_LOG_STREAM_TOPIC': log_stream_topic,
               'PIPELINE_INPUT_STREAM_URL': input_stream_url,
               'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
               'PIPELINE_OUTPUT_STREAM_URL': output_stream_url,
               'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
               'PIPELINE_IMAGE_REGISTRY_URL': image_registry_url,
               'PIPELINE_IMAGE_REGISTRY_REPO': image_registry_repo,
               'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
               'PIPELINE_IMAGE_REGISTRY_BASE_TAG': image_registry_base_tag
              }

    model_train_cpu_Dockerfile_templates_path = _os.path.normpath(_os.path.join(pipeline_templates_path, _Dockerfile_template_registry['train-server'][0][0]))
    path, filename = _os.path.split(model_train_cpu_Dockerfile_templates_path)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    rendered_filename = _os.path.normpath('%s/.pipeline-generated-%s-%s-%s-Dockerfile' % (build_context_path, image_registry_namespace, model_name, model_tag))
    with open(rendered_filename, 'wt') as fh:
        fh.write(rendered)
        print("'%s' => '%s'." % (filename, rendered_filename))

    return rendered_filename


def train_server_build(model_name,
                       model_tag,
                       model_type,
                       model_path,
                       model_runtime=None,
                       model_chip=None,
                       http_proxy=None,
                       https_proxy=None,
                       log_stream_url=None,
                       log_stream_topic=None,
                       input_stream_url=None,
                       input_stream_topic=None,
                       output_stream_url=None,
                       output_stream_topic=None,
                       build_type=None,
                       build_context_path=None,
                       image_registry_url=None,
                       image_registry_repo=None,
                       image_registry_namespace=None,
                       image_registry_base_tag=None,
                       image_registry_base_chip=None,
                       pipeline_templates_path=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip: 
        model_chip = _default_model_chip

    if not build_type:
        build_type = _default_build_type

    if not build_context_path:
        build_context_path = _default_build_context_path

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    if not image_registry_base_tag:
        image_registry_base_tag = _default_image_registry_base_tag

    if not image_registry_base_chip:
        image_registry_base_chip = _default_model_chip

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    build_context_path = _os.path.normpath(build_context_path)
    build_context_path = _os.path.expandvars(build_context_path)
    build_context_path = _os.path.expanduser(build_context_path)
    build_context_path = _os.path.normpath(build_context_path)
    build_context_path = _os.path.abspath(build_context_path)
    build_context_path = _os.path.normpath(build_context_path)
    print(build_context_path)

    pipeline_templates_path = _os.path.normpath(pipeline_templates_path)
    pipeline_templates_path = _os.path.expandvars(pipeline_templates_path)
    pipeline_templates_path = _os.path.expanduser(pipeline_templates_path)
    pipeline_templates_path = _os.path.abspath(pipeline_templates_path)
    pipeline_templates_path = _os.path.normpath(pipeline_templates_path)
    pipeline_templates_path = _os.path.relpath(pipeline_templates_path, build_context_path)
    pipeline_templates_path = _os.path.normpath(pipeline_templates_path)
    print(pipeline_templates_path)

    model_path = _os.path.normpath(model_path)
    model_path = _os.path.expandvars(model_path)
    model_path = _os.path.expanduser(model_path)
    model_path = _os.path.abspath(model_path)
    model_path = _os.path.normpath(model_path)
    model_path = _os.path.relpath(model_path, build_context_path)
    model_path = _os.path.normpath(model_path)
    print(model_path)

    if build_type == 'docker':
        generated_Dockerfile = _create_train_server_Dockerfile(model_name=model_name,
                                                                    model_tag=model_tag,
                                                                    model_type=model_type,
                                                                    model_runtime=model_runtime,
                                                                    model_chip=model_chip,
                                                                    model_path=model_path,
                                                                    http_proxy=http_proxy,
                                                                    https_proxy=https_proxy,
                                                                    log_stream_url=log_stream_url,
                                                                    log_stream_topic=log_stream_topic,
                                                                    input_stream_url=input_stream_url,
                                                                    input_stream_topic=input_stream_topic,
                                                                    output_stream_url=output_stream_url,
                                                                    output_stream_topic=output_stream_topic,
                                                                    build_context_path=build_context_path,
                                                                    image_registry_url=image_registry_url,
                                                                    image_registry_repo=image_registry_repo,
                                                                    image_registry_namespace=image_registry_namespace,
                                                                    image_registry_base_tag=image_registry_base_tag,
                                                                    image_registry_base_chip=image_registry_base_chip,
                                                                    pipeline_templates_path=pipeline_templates_path)

        if http_proxy:
           http_proxy_build_arg_snippet = '--build-arg HTTP_PROXY=%s' % http_proxy
        else:
           http_proxy_build_arg_snippet = ''

        if https_proxy:
           https_proxy_build_arg_snippet = '--build-arg HTTPS_PROXY=%s' % https_proxy
        else:
           https_proxy_build_arg_snippet = ''

        cmd = 'docker build %s %s -t %s/%s/%s-%s:%s -f %s %s' % (http_proxy_build_arg_snippet, https_proxy_build_arg_snippet, image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag, generated_Dockerfile, build_context_path)

        print(cmd)
        print("")
        process = _subprocess.call(cmd, shell=True)
    else:
        print("Build type '%s' not found." % build_type)


def train_server_start(model_name,
                       model_tag,
                       model_type,
                       model_runtime=None,
                       model_chip=None,
                       input_path=None,
                       output_path=None,
                       log_stream_url=None,
                       log_stream_topic=None,
                       input_stream_url=None,
                       input_stream_topic=None,
                       output_stream_url=None,
                       output_stream_topic=None,
                       train_args='',
                       memory_limit='2G',
                       core_limit='1000m',
                       image_registry_url=None,
                       image_registry_repo=None,
                       image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if input_path:
        input_path = _os.path.expandvars(input_path)
        input_path = _os.path.expanduser(input_path)
        input_path = _os.path.abspath(input_path)
        input_path = _os.path.normpath(input_path)

    if output_path:
        output_path = _os.path.expandvars(output_path)
        output_path = _os.path.expanduser(output_path)
        output_path = _os.path.abspath(output_path)
        output_path = _os.path.normpath(output_path)

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    # environment == local, task type == worker, and no cluster definition
    tf_config_local_run = '\'{\"environment\": \"local\", \"task\":{\"type\": \"worker\"}}\''

    # Note:  We added `train` to mimic AWS SageMaker and encourage ENTRYPOINT vs CMD per https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html
    # /opt/ml/input/data/{training|validation|testing} per https://docs.aws.amazon.com/sagemaker/latest/dg/your-algorithms-training-algo.html

    container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    if model_chip == 'gpu':
        docker_cmd = 'nvidia-docker'
    else:
        docker_cmd = 'docker'

    cmd = '%s run -itd -p 2222:2222 -p 6006:6006 -e PIPELINE_LOG_STREAM_URL=%s -e PIPELINE_LOG_STREAM_TOPIC=%s -e PIPELINE_INPUT_STREAM_URL=%s -e PIPELINE_INPUT_STREAM_TOPIC=%s -e PIPELINE_OUTPUT_STREAM_URL=%s -e PIPELINE_OUTPUT_STREAM_TOPIC=%s -e TF_CONFIG=%s -e PIPELINE_MODEL_TRAIN_ARGS=%s -v %s:/opt/ml/input/ -v %s:/opt/ml/output/ --name=%s -m %s %s/%s/%s-%s:%s train' % (docker_cmd, log_stream_url, log_stream_topic, input_stream_url, input_stream_topic, output_stream_url, output_stream_topic, tf_config_local_run, train_args, input_path, output_path, image_registry_namespace, container_name, memory_limit, image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag)
    print(cmd)
    print("")
    process = _subprocess.call(cmd, shell=True)

    print("")
    print("container name: '%s'" % container_name)


def train_server_stop(
                      model_name,
                      model_tag,
                      model_type,
                      model_runtime=None,
                      model_chip=None,
                      image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    container_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    cmd = 'docker rm -f %s' % container_name 

    print(cmd)
    print("")

    process = _subprocess.call(cmd, shell=True)


def _create_train_kube_yaml(
                            model_name,
                            model_tag,
                            model_type,
                            model_runtime,
                            model_chip,
                            input_path,
                            output_path,
                            log_stream_url,
                            log_stream_topic,
                            input_stream_url,
                            input_stream_topic,
                            output_stream_url,
                            output_stream_topic,
                            master_replicas,
                            ps_replicas,
                            worker_replicas,
                            train_args,
                            image_registry_url,
                            image_registry_repo,
                            image_registry_namespace,
                            image_registry_base_tag,
                            image_registry_base_chip,
                            pipeline_templates_path,
                            cluster_namespace,
                            worker_memory_limit,
                            worker_core_limit):

    model_tag = _validate_and_prep_model_tag(model_tag)

    context = {
               'PIPELINE_MODEL_NAME': model_name,
               'PIPELINE_MODEL_TAG': model_tag,
               'PIPELINE_MODEL_TYPE': model_type,
               'PIPELINE_MODEL_RUNTIME': model_runtime,
               'PIPELINE_MODEL_CHIP': model_chip,
               'PIPELINE_INPUT_HOST_PATH': input_path,
               'PIPELINE_OUTPUT_HOST_PATH': output_path,
               'PIPELINE_LOG_STREAM_URL': log_stream_url,
               'PIPELINE_LOG_STREAM_TOPIC': log_stream_topic,
               'PIPELINE_INPUT_STREAM_URL': input_stream_url,
               'PIPELINE_INPUT_STREAM_TOPIC': input_stream_topic,
               'PIPELINE_OUTPUT_STREAM_URL': output_stream_url,
               'PIPELINE_OUTPUT_STREAM_TOPIC': output_stream_topic,
               'PIPELINE_MODEL_TRAIN_ARGS': train_args,
               'PIPELINE_WORKER_CORE_LIMIT': worker_core_limit,
               'PIPELINE_WORKER_MEMORY_LIMIT': worker_memory_limit,
               'PIPELINE_MASTER_REPLICAS': int(master_replicas),
               'PIPELINE_PS_REPLICAS': int(ps_replicas),
               'PIPELINE_WORKER_REPLICAS': int(worker_replicas),
               'PIPELINE_IMAGE_REGISTRY_URL': image_registry_url,
               'PIPELINE_IMAGE_REGISTRY_REPO': image_registry_repo,
               'PIPELINE_IMAGE_REGISTRY_NAMESPACE': image_registry_namespace,
               'PIPELINE_IMAGE_REGISTRY_BASE_TAG': image_registry_base_tag,
               }

    predict_clustered_template = _os.path.normpath(_os.path.join(pipeline_templates_path, _train_kube_template_registry['train-cluster'][0][0]))
    path, filename = _os.path.split(predict_clustered_template)
    rendered = _jinja2.Environment(loader=_jinja2.FileSystemLoader(path)).get_template(filename).render(context)
    rendered_filename = _os.path.normpath('.pipeline-generated-%s-%s-%s.yaml' % (image_registry_namespace, model_name, model_tag))
    with open(rendered_filename, 'wt') as fh:
        fh.write(rendered)
    print("'%s' => '%s'." % (filename, rendered_filename))

    return rendered_filename


def train_kube_connect(
                          model_name,
                          model_tag,
                          model_type,                            
                          model_runtime=None,
                          model_chip=None,
                          local_port=None,
                          service_port=None,
                          cluster_namespace=None,
                          image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_connect(service_name=service_name,
                          cluster_namespace=cluster_namespace,
                          local_port=local_port,
                          service_port=service_port)


def train_kube_describe(
                           model_name,
                           model_tag,
                           model_type,
                           model_runtime=None,
                           model_chip=None,
                           cluster_namespace=None,
                           image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_describe(service_name=service_name)


def train_kube_shell(
                        model_name,
                        model_tag,
                        model_type,
                        model_runtime=None,
                        model_chip=None,
                        cluster_namespace=None,
                        image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = PipelienCli._default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_shell(service_name=service_name,
                        cluster_namespace=cluster_namespace)


def train_kube_start(model_name,
                     model_tag,
                     model_type,
                     input_path,
                     output_path,
                     master_replicas,
                     ps_replicas,
                     worker_replicas,
                     model_runtime=None,
                     model_chip=None,
                     log_stream_url=None,
                     log_stream_topic=None,
                     input_stream_url=None,
                     input_stream_topic=None,
                     output_stream_url=None,
                     output_stream_topic=None,                            
                     train_args='',
                     image_registry_url=None,
                     image_registry_repo=None,
                     image_registry_namespace=None,
                     image_registry_base_tag=None,
                     image_registry_base_chip=None,
                     pipeline_templates_path=None,
                     cluster_namespace=None,
                     worker_memory_limit=None,
                     worker_core_limit=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if input_path:
        input_path = _os.path.expandvars(input_path)
        input_path = _os.path.expanduser(input_path)
        input_path = _os.path.abspath(input_path)
        input_path = _os.path.normpath(input_path)

    if output_path:
        output_path = _os.path.expandvars(output_path)
        output_path = _os.path.expanduser(output_path)
        output_path = _os.path.abspath(output_path)
        output_path = _os.path.normpath(output_path)

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    if not image_registry_base_tag:
        image_registry_base_tag = _default_image_registry_base_tag

    if not image_registry_base_chip:
        image_registry_base_chip = _default_model_chip

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    pipeline_templates_path = _os.path.expandvars(pipeline_templates_path)
    pipeline_templates_path = _os.path.expanduser(pipeline_templates_path)
    pipeline_templates_path = _os.path.abspath(pipeline_templates_path)
    pipeline_templates_path = _os.path.normpath(pipeline_templates_path)

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    generated_yaml_path = _create_train_kube_yaml(
                                                       model_name=model_name,
                                                       model_tag=model_tag,
                                                       model_type=model_type,
                                                       model_runtime=model_runtime,
                                                       model_chip=model_chip,
                                                       input_path=input_path,
                                                       output_path=output_path,
                                                       master_replicas=master_replicas,
                                                       ps_replicas=ps_replicas,
                                                       worker_replicas=worker_replicas,
                                                       log_stream_url=log_stream_url,
                                                       log_stream_topic=log_stream_topic,
                                                       input_stream_url=input_stream_url,
                                                       input_stream_topic=input_stream_topic,
                                                       output_stream_url=output_stream_url,
                                                       output_stream_topic=output_stream_topic,
                                                       train_args=train_args,
                                                       image_registry_url=image_registry_url,
                                                       image_registry_repo=image_registry_repo,
                                                       image_registry_namespace=image_registry_namespace,
                                                       image_registry_base_tag=image_registry_base_tag,
                                                       image_registry_base_chip=image_registry_base_chip,
                                                       pipeline_templates_path=pipeline_templates_path,
                                                       cluster_namespace=cluster_namespace,
                                                       worker_memory_limit=worker_memory_limit,
                                                       worker_core_limit=worker_core_limit)

    generated_yaml_path = _os.path.normpath(generated_yaml_path)

    # For now, only handle '-deploy' and '-svc' yaml's
    _kube_apply(yaml_path=generated_yaml_path,
                     cluster_namespace=cluster_namespace)


# TODO:  Fix this
def train_kube_stop(
                       model_name,
                       model_tag,
                       model_type,
                       model_runtime=None,
                       model_chip=None,
                       cluster_namespace=None,
                       image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_stop(service_name=service_name,
                       cluster_namespace=cluster_namespace)


# TODO:  Fix this
def train_kube_logs(
                       model_name,
                       model_tag,
                       model_type,
                       model_runtime=None,
                       model_chip=None,
                       cluster_namespace=None,
                       image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_logs(service_name=service_name,
                       cluster_namespace=cluster_namespace)


# TODO:  Fix this
def train_kube_scale(
                        model_name,
                        model_tag,
                        model_type,
                        replicas,
                        model_runtime=None,
                        model_chip=None,
                        cluster_namespace=None,
                        image_registry_namespace=None):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_train_namespace

    service_name = '%s-%s-%s' % (image_registry_namespace, model_name, model_tag)

    _service_scale(service_name=service_name,
                        replicas=replicas,
                        cluster_namespace=cluster_namespace)


def predict_sage_start(
                       model_name,
                       model_tag,
                       model_type,
                       aws_iam_arn,
                       aws_instance_type,
                       model_runtime=None,
                       model_chip=None,
                       log_stream_url=None,
                       log_stream_topic=None,
                       input_stream_url=None,
                       input_stream_topic=None,
                       output_stream_url=None,
                       output_stream_topic=None,
                       memory_limit='2Gi',
                       core_limit='1000m',
                       target_core_util_percentage='75',
                       min_replicas='1',
                       max_replicas='1',
                       cluster_namespace=None,
                       image_registry_url=None,
                       image_registry_repo=None,
                       image_registry_namespace=None,
                       image_registry_base_tag=None,
                       image_registry_base_chip=None,
                       pipeline_templates_path=None,
                       timeout_seconds=1200):

    model_tag = _validate_and_prep_model_tag(model_tag)

    if not model_runtime:
        model_runtime = _get_default_model_runtime(model_type)

    if not model_chip:
        model_chip = _default_model_chip

    if not cluster_namespace:
        cluster_namespace = _default_cluster_namespace

    if not image_registry_url:
        image_registry_url = _default_image_registry_url

    if not image_registry_repo:
        image_registry_repo = _default_image_registry_repo

    if not image_registry_namespace:
        image_registry_namespace = _default_image_registry_predict_namespace

    if not image_registry_base_tag:
        image_registry_base_tag = _default_image_registry_base_tag

    if not image_registry_base_chip:
        image_registry_base_chip = _default_model_chip

    if not pipeline_templates_path:
        pipeline_templates_path = _default_pipeline_templates_path

    # Create Model
    from datetime import datetime

    begin_time = datetime.now()

    sagemaker_admin_client = _boto3.client('sagemaker')
    response = sagemaker_admin_client.create_model(
        ModelName='%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
        PrimaryContainer={
            'ContainerHostname': '%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
            'Image': '%s/%s/%s-%s:%s' % (image_registry_url, image_registry_repo, image_registry_namespace, model_name, model_tag),
            'Environment': {
            }
        },
        SupplementalContainers=[],
        ExecutionRoleArn='%s' % aws_iam_arn,
        Tags=[
            {
                'Key': 'PIPELINE_MODEL_NAME',
                'Value': '%s' % model_name
            },
            {
                'Key': 'PIPELINE_MODEL_TAG',
                'Value': '%s' % model_tag
            },
            {
                'Key': 'PIPELINE_MODEL_TYPE',
                'Value': '%s' % model_type
            },
            {
                'Key': 'PIPELINE_MODEL_RUNTIME',
                'Value': '%s' % model_runtime
            },
            {
                'Key': 'PIPELINE_MODEL_CHIP',
                'Value': '%s' % model_chip
            },
        ]
    )

    if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("")
        print("ModelArn: '%s'" % response['ModelArn'])
        print("")
        print("Success!")
        print("")
    else:
        exit(1)

    # Create Endpoint Configuration
    response = sagemaker_admin_client.create_endpoint_config(
        EndpointConfigName='%s-%s' % (image_registry_namespace, model_name),
        ProductionVariants=[
            {
                'VariantName': '%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
                'ModelName': '%s-%s-%s' % (image_registry_namespace, model_name, model_tag),
                'InitialInstanceCount': 1,
                'InstanceType': '%s' % aws_instance_type,
                 # 'ml.c4.2xlarge'|'ml.c4.8xlarge'|'ml.c4.xlarge'|'ml.c5.2xlarge'|'ml.c5.9xlarge'|'ml.c5.xlarge'|'ml.m4.xlarge'|'ml.p2.xlarge'|'ml.p3.2xlarge'|'ml.t2.medium',
                'InitialVariantWeight': 100
            },
        ],
        Tags=[
            {
                'Key': 'PIPELINE_MODEL_NAME',
                'Value': '%s' % model_name
            },
            {
                'Key': 'PIPELINE_MODEL_TAG',
                'Value': '%s' % model_tag
            },
            {
                'Key': 'PIPELINE_MODEL_TYPE',
                'Value': '%s' % model_type
            },
            {
                'Key': 'PIPELINE_MODEL_RUNTIME',
                'Value': '%s' % model_runtime
            },
            {
                'Key': 'PIPELINE_MODEL_CHIP',
                'Value': '%s' % model_chip
            },
        ]
    )

    if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("")
        print("EndpointConfigArn: '%s'" % response['EndpointConfigArn'])
        print("")
        print("Success!")
        print("")
    else:
        exit(1)

    # Create Endpoint (Models + Endpoint Configuration)
    response = sagemaker_admin_client.create_endpoint(
        EndpointName='%s-%s' % (image_registry_namespace, model_name),
        EndpointConfigName='%s-%s' % (image_registry_namespace, model_name),
        Tags=[
            {
                'Key': 'PIPELINE_MODEL_NAME',
                'Value': '%s' % model_name
            },
            {
                'Key': 'PIPELINE_MODEL_TAG',
                'Value': '%s' % model_tag
            },
            {
                'Key': 'PIPELINE_MODEL_TYPE',
                'Value': '%s' % model_type
            },
            {
                'Key': 'PIPELINE_MODEL_RUNTIME',
                'Value': '%s' % model_runtime
            },
            {
                'Key': 'PIPELINE_MODEL_CHIP',
                'Value': '%s' % model_chip
            },
        ]
    )

    if response and response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("")
        print("EndpointArn: '%s'" % response['EndpointArn'])
        print("")
        print("Success!")
        print("")
    else:
        exit(1)

    end_time = datetime.now()
    total_time = end_time - begin_time
    print("")
    print("Request time: %s milliseconds" % (total_time.microseconds / 1000))
    print("")


# TODO:  Fix this
def _image_to_json(
                  image_path,
                  image_format):

    image_path = _os.path.expandvars(image_path)
    image_path = _os.path.expanduser(image_path)
    image_path = _os.path.abspath(image_path)
    image_path = _os.path.normpath(image_path)

    print('image_path: %s' % image_path)
    print('image_format: %s' % image_format)

    #image = Image.open(image_path)
    #image_str = BytesIO()
    #image.save(image_str, format=image_format)
    #return _json.dumps(str(image_str.getvalue()))
#    import numpy as np
#    img = Image.open("input.png")
#    arr = np.array(img)
#    return arr


def _image_to_numpy(
                   image_path):
    """Convert image to np array.
    Returns:
        Numpy array of size (1, 28, 28, 1) with MNIST sample images.
    """
    image_as_numpy = np.zeros((1, 28, 28))
    print(image_as_numpy.shape)
    for idx, image_path in enumerate(image_path):
        image_read = skimage.io.imread(fname=image_path, as_grey=True)
        print(image_read.shape)
        image_as_numpy[idx, :, :] = image_read

    return _json.dumps(list(image_as_numpy.flatten()))


def _main():
    if len(_sys.argv) == 1:
        return help()

    if len(_sys.argv) > 1 and _sys.argv[1] == 'http':
        app.run(debug=True)
    else:
        _fire.Fire()

if __name__ == '__main__':
    
    _main()
