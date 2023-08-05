# nifi-python-swagger-client

Swagger 2.0 client in python for Apache NiFi  
Backend for [NiPyAPI: A convenient Python wrapper for Apache NiFi](
https://github.com/Chaffelson/nipyapi)

## Background

Inspired by the equivalent Java client maintained over at [hermannpencole/nifi-swagger-client](https://github.com/hermannpencole/nifi-swagger-client)

The [NiFi Rest API](https://nifi.apache.org/docs/nifi-docs/rest-api/index.html) provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

This Python package provides a convenient wrapper to the NiFi Rest API for further automation, such as Ansible playbooks etc. 

It was automatically generated using the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project using swagger-codegen-cli version 2.2.3, and then cleaned up and curated by the contributors.

For more information, please visit [https://nifi.apache.org](https://nifi.apache.org)

## Versioning

- NiFi API version support: 1.2.0 - 1.5.0 tested
- Python Package version: 1.4.0
- Build package: io.swagger.codegen.languages.PythonClientCodegen

## Requirements.

Tested on Python 2.7 and 3.6, other versions may work

## Installation & Usage
### pip install

You can install directly from Github

```sh
pip install git+https://github.com/Chaffelson/nifi-python-swagger-client.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/Chaffelson/nifi-python-swagger-client.git`)

Then import the package:
```python
import swagger_client 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import swagger_client
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint
swagger_client.configuration.host = "http://localhost:8080/nifi-api"
api_instance = swagger_client.SystemdiagnosticsApi()

try:
    # Prints out the system state of the target NiFi Instance
    api_response = api_instance.get_system_diagnostics()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SystemdiagnosticsApi->get_system_diagnostics: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost/nifi-api*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AccessApi* | [**create_access_token**](docs/AccessApi.md#create_access_token) | **POST** /access/token | Creates a token for accessing the REST API via username/password
*AccessApi* | [**create_access_token_from_ticket**](docs/AccessApi.md#create_access_token_from_ticket) | **POST** /access/kerberos | Creates a token for accessing the REST API via Kerberos ticket exchange / SPNEGO negotiation
*AccessApi* | [**create_download_token**](docs/AccessApi.md#create_download_token) | **POST** /access/download-token | Creates a single use access token for downloading FlowFile content.
*AccessApi* | [**create_ui_extension_token**](docs/AccessApi.md#create_ui_extension_token) | **POST** /access/ui-extension-token | Creates a single use access token for accessing a NiFi UI extension.
*AccessApi* | [**get_access_status**](docs/AccessApi.md#get_access_status) | **GET** /access | Gets the status the client&#39;s access
*AccessApi* | [**get_login_config**](docs/AccessApi.md#get_login_config) | **GET** /access/config | Retrieves the access configuration for this NiFi
*ConnectionsApi* | [**delete_connection**](docs/ConnectionsApi.md#delete_connection) | **DELETE** /connections/{id} | Deletes a connection
*ConnectionsApi* | [**get_connection**](docs/ConnectionsApi.md#get_connection) | **GET** /connections/{id} | Gets a connection
*ConnectionsApi* | [**update_connection**](docs/ConnectionsApi.md#update_connection) | **PUT** /connections/{id} | Updates a connection
*ControllerApi* | [**create_bulletin**](docs/ControllerApi.md#create_bulletin) | **POST** /controller/bulletin | Creates a new bulletin
*ControllerApi* | [**create_controller_service**](docs/ControllerApi.md#create_controller_service) | **POST** /controller/controller-services | Creates a new controller service
*ControllerApi* | [**create_reporting_task**](docs/ControllerApi.md#create_reporting_task) | **POST** /controller/reporting-tasks | Creates a new reporting task
*ControllerApi* | [**delete_history**](docs/ControllerApi.md#delete_history) | **DELETE** /controller/history | Purges history
*ControllerApi* | [**delete_node**](docs/ControllerApi.md#delete_node) | **DELETE** /controller/cluster/nodes/{id} | Removes a node from the cluster
*ControllerApi* | [**get_cluster**](docs/ControllerApi.md#get_cluster) | **GET** /controller/cluster | Gets the contents of the cluster
*ControllerApi* | [**get_controller_config**](docs/ControllerApi.md#get_controller_config) | **GET** /controller/config | Retrieves the configuration for this NiFi Controller
*ControllerApi* | [**get_node**](docs/ControllerApi.md#get_node) | **GET** /controller/cluster/nodes/{id} | Gets a node in the cluster
*ControllerApi* | [**update_controller_config**](docs/ControllerApi.md#update_controller_config) | **PUT** /controller/config | Retrieves the configuration for this NiFi
*ControllerApi* | [**update_node**](docs/ControllerApi.md#update_node) | **PUT** /controller/cluster/nodes/{id} | Updates a node in the cluster
*ControllerservicesApi* | [**clear_state**](docs/ControllerservicesApi.md#clear_state) | **POST** /controller-services/{id}/state/clear-requests | Clears the state for a controller service
*ControllerservicesApi* | [**get_controller_service**](docs/ControllerservicesApi.md#get_controller_service) | **GET** /controller-services/{id} | Gets a controller service
*ControllerservicesApi* | [**get_controller_service_references**](docs/ControllerservicesApi.md#get_controller_service_references) | **GET** /controller-services/{id}/references | Gets a controller service
*ControllerservicesApi* | [**get_property_descriptor**](docs/ControllerservicesApi.md#get_property_descriptor) | **GET** /controller-services/{id}/descriptors | Gets a controller service property descriptor
*ControllerservicesApi* | [**get_state**](docs/ControllerservicesApi.md#get_state) | **GET** /controller-services/{id}/state | Gets the state for a controller service
*ControllerservicesApi* | [**remove_controller_service**](docs/ControllerservicesApi.md#remove_controller_service) | **DELETE** /controller-services/{id} | Deletes a controller service
*ControllerservicesApi* | [**update_controller_service**](docs/ControllerservicesApi.md#update_controller_service) | **PUT** /controller-services/{id} | Updates a controller service
*ControllerservicesApi* | [**update_controller_service_references**](docs/ControllerservicesApi.md#update_controller_service_references) | **PUT** /controller-services/{id}/references | Updates a controller services references
*CountersApi* | [**get_counters**](docs/CountersApi.md#get_counters) | **GET** /counters | Gets the current counters for this NiFi
*CountersApi* | [**update_counter**](docs/CountersApi.md#update_counter) | **PUT** /counters/{id} | Updates the specified counter. This will reset the counter value to 0
*DatatransferApi* | [**commit_input_port_transaction**](docs/DatatransferApi.md#commit_input_port_transaction) | **DELETE** /data-transfer/input-ports/{portId}/transactions/{transactionId} | Commit or cancel the specified transaction
*DatatransferApi* | [**commit_output_port_transaction**](docs/DatatransferApi.md#commit_output_port_transaction) | **DELETE** /data-transfer/output-ports/{portId}/transactions/{transactionId} | Commit or cancel the specified transaction
*DatatransferApi* | [**create_port_transaction**](docs/DatatransferApi.md#create_port_transaction) | **POST** /data-transfer/{portType}/{portId}/transactions | Create a transaction to the specified output port or input port
*DatatransferApi* | [**extend_input_port_transaction_ttl**](docs/DatatransferApi.md#extend_input_port_transaction_ttl) | **PUT** /data-transfer/input-ports/{portId}/transactions/{transactionId} | Extend transaction TTL
*DatatransferApi* | [**extend_output_port_transaction_ttl**](docs/DatatransferApi.md#extend_output_port_transaction_ttl) | **PUT** /data-transfer/output-ports/{portId}/transactions/{transactionId} | Extend transaction TTL
*DatatransferApi* | [**receive_flow_files**](docs/DatatransferApi.md#receive_flow_files) | **POST** /data-transfer/input-ports/{portId}/transactions/{transactionId}/flow-files | Transfer flow files to the input port
*DatatransferApi* | [**transfer_flow_files**](docs/DatatransferApi.md#transfer_flow_files) | **GET** /data-transfer/output-ports/{portId}/transactions/{transactionId}/flow-files | Transfer flow files from the output port
*FlowApi* | [**generate_client_id**](docs/FlowApi.md#generate_client_id) | **GET** /flow/client-id | Generates a client id.
*FlowApi* | [**get_about_info**](docs/FlowApi.md#get_about_info) | **GET** /flow/about | Retrieves details about this NiFi to put in the About dialog
*FlowApi* | [**get_action**](docs/FlowApi.md#get_action) | **GET** /flow/history/{id} | Gets an action
*FlowApi* | [**get_banners**](docs/FlowApi.md#get_banners) | **GET** /flow/banners | Retrieves the banners for this NiFi
*FlowApi* | [**get_bulletin_board**](docs/FlowApi.md#get_bulletin_board) | **GET** /flow/bulletin-board | Gets current bulletins
*FlowApi* | [**get_bulletins**](docs/FlowApi.md#get_bulletins) | **GET** /flow/controller/bulletins | Retrieves Controller level bulletins
*FlowApi* | [**get_cluster_summary**](docs/FlowApi.md#get_cluster_summary) | **GET** /flow/cluster/summary | The cluster summary for this NiFi
*FlowApi* | [**get_component_history**](docs/FlowApi.md#get_component_history) | **GET** /flow/history/components/{componentId} | Gets configuration history for a component
*FlowApi* | [**get_connection_status**](docs/FlowApi.md#get_connection_status) | **GET** /flow/connections/{id}/status | Gets status for a connection
*FlowApi* | [**get_connection_status_history**](docs/FlowApi.md#get_connection_status_history) | **GET** /flow/connections/{id}/status/history | Gets the status history for a connection
*FlowApi* | [**get_controller_service_types**](docs/FlowApi.md#get_controller_service_types) | **GET** /flow/controller-service-types | Retrieves the types of controller services that this NiFi supports
*FlowApi* | [**get_controller_services_from_controller**](docs/FlowApi.md#get_controller_services_from_controller) | **GET** /flow/controller/controller-services | Gets all controller services
*FlowApi* | [**get_controller_services_from_group**](docs/FlowApi.md#get_controller_services_from_group) | **GET** /flow/process-groups/{id}/controller-services | Gets all controller services
*FlowApi* | [**get_controller_status**](docs/FlowApi.md#get_controller_status) | **GET** /flow/status | Gets the current status of this NiFi
*FlowApi* | [**get_current_user**](docs/FlowApi.md#get_current_user) | **GET** /flow/current-user | Retrieves the user identity of the user making the request
*FlowApi* | [**get_flow**](docs/FlowApi.md#get_flow) | **GET** /flow/process-groups/{id} | Gets a process group
*FlowApi* | [**get_flow_config**](docs/FlowApi.md#get_flow_config) | **GET** /flow/config | Retrieves the configuration for this NiFi flow
*FlowApi* | [**get_input_port_status**](docs/FlowApi.md#get_input_port_status) | **GET** /flow/input-ports/{id}/status | Gets status for an input port
*FlowApi* | [**get_output_port_status**](docs/FlowApi.md#get_output_port_status) | **GET** /flow/output-ports/{id}/status | Gets status for an output port
*FlowApi* | [**get_prioritizers**](docs/FlowApi.md#get_prioritizers) | **GET** /flow/prioritizers | Retrieves the types of prioritizers that this NiFi supports
*FlowApi* | [**get_process_group_status**](docs/FlowApi.md#get_process_group_status) | **GET** /flow/process-groups/{id}/status | Gets the status for a process group
*FlowApi* | [**get_process_group_status_history**](docs/FlowApi.md#get_process_group_status_history) | **GET** /flow/process-groups/{id}/status/history | Gets status history for a remote process group
*FlowApi* | [**get_processor_status**](docs/FlowApi.md#get_processor_status) | **GET** /flow/processors/{id}/status | Gets status for a processor
*FlowApi* | [**get_processor_status_history**](docs/FlowApi.md#get_processor_status_history) | **GET** /flow/processors/{id}/status/history | Gets status history for a processor
*FlowApi* | [**get_processor_types**](docs/FlowApi.md#get_processor_types) | **GET** /flow/processor-types | Retrieves the types of processors that this NiFi supports
*FlowApi* | [**get_remote_process_group_status**](docs/FlowApi.md#get_remote_process_group_status) | **GET** /flow/remote-process-groups/{id}/status | Gets status for a remote process group
*FlowApi* | [**get_remote_process_group_status_history**](docs/FlowApi.md#get_remote_process_group_status_history) | **GET** /flow/remote-process-groups/{id}/status/history | Gets the status history
*FlowApi* | [**get_reporting_task_types**](docs/FlowApi.md#get_reporting_task_types) | **GET** /flow/reporting-task-types | Retrieves the types of reporting tasks that this NiFi supports
*FlowApi* | [**get_reporting_tasks**](docs/FlowApi.md#get_reporting_tasks) | **GET** /flow/reporting-tasks | Gets all reporting tasks
*FlowApi* | [**get_templates**](docs/FlowApi.md#get_templates) | **GET** /flow/templates | Gets all templates
*FlowApi* | [**query_history**](docs/FlowApi.md#query_history) | **GET** /flow/history | Gets configuration history
*FlowApi* | [**schedule_components**](docs/FlowApi.md#schedule_components) | **PUT** /flow/process-groups/{id} | Schedule or unschedule comopnents in the specified Process Group.
*FlowApi* | [**search_cluster**](docs/FlowApi.md#search_cluster) | **GET** /flow/cluster/search-results | Searches the cluster for a node with the specified address
*FlowApi* | [**search_flow**](docs/FlowApi.md#search_flow) | **GET** /flow/search-results | Performs a search against this NiFi using the specified search term
*FlowfilequeuesApi* | [**create_drop_request**](docs/FlowfilequeuesApi.md#create_drop_request) | **POST** /flowfile-queues/{id}/drop-requests | Creates a request to drop the contents of the queue in this connection.
*FlowfilequeuesApi* | [**create_flow_file_listing**](docs/FlowfilequeuesApi.md#create_flow_file_listing) | **POST** /flowfile-queues/{id}/listing-requests | Lists the contents of the queue in this connection.
*FlowfilequeuesApi* | [**delete_listing_request**](docs/FlowfilequeuesApi.md#delete_listing_request) | **DELETE** /flowfile-queues/{id}/listing-requests/{listing-request-id} | Cancels and/or removes a request to list the contents of this connection.
*FlowfilequeuesApi* | [**download_flow_file_content**](docs/FlowfilequeuesApi.md#download_flow_file_content) | **GET** /flowfile-queues/{id}/flowfiles/{flowfile-uuid}/content | Gets the content for a FlowFile in a Connection.
*FlowfilequeuesApi* | [**get_drop_request**](docs/FlowfilequeuesApi.md#get_drop_request) | **GET** /flowfile-queues/{id}/drop-requests/{drop-request-id} | Gets the current status of a drop request for the specified connection.
*FlowfilequeuesApi* | [**get_flow_file**](docs/FlowfilequeuesApi.md#get_flow_file) | **GET** /flowfile-queues/{id}/flowfiles/{flowfile-uuid} | Gets a FlowFile from a Connection.
*FlowfilequeuesApi* | [**get_listing_request**](docs/FlowfilequeuesApi.md#get_listing_request) | **GET** /flowfile-queues/{id}/listing-requests/{listing-request-id} | Gets the current status of a listing request for the specified connection.
*FlowfilequeuesApi* | [**remove_drop_request**](docs/FlowfilequeuesApi.md#remove_drop_request) | **DELETE** /flowfile-queues/{id}/drop-requests/{drop-request-id} | Cancels and/or removes a request to drop the contents of this connection.
*FunnelApi* | [**get_funnel**](docs/FunnelApi.md#get_funnel) | **GET** /funnels/{id} | Gets a funnel
*FunnelApi* | [**remove_funnel**](docs/FunnelApi.md#remove_funnel) | **DELETE** /funnels/{id} | Deletes a funnel
*FunnelApi* | [**update_funnel**](docs/FunnelApi.md#update_funnel) | **PUT** /funnels/{id} | Updates a funnel
*InputportsApi* | [**get_input_port**](docs/InputportsApi.md#get_input_port) | **GET** /input-ports/{id} | Gets an input port
*InputportsApi* | [**remove_input_port**](docs/InputportsApi.md#remove_input_port) | **DELETE** /input-ports/{id} | Deletes an input port
*InputportsApi* | [**update_input_port**](docs/InputportsApi.md#update_input_port) | **PUT** /input-ports/{id} | Updates an input port
*LabelsApi* | [**get_label**](docs/LabelsApi.md#get_label) | **GET** /labels/{id} | Gets a label
*LabelsApi* | [**remove_label**](docs/LabelsApi.md#remove_label) | **DELETE** /labels/{id} | Deletes a label
*LabelsApi* | [**update_label**](docs/LabelsApi.md#update_label) | **PUT** /labels/{id} | Updates a label
*OutputportsApi* | [**get_output_port**](docs/OutputportsApi.md#get_output_port) | **GET** /output-ports/{id} | Gets an output port
*OutputportsApi* | [**remove_output_port**](docs/OutputportsApi.md#remove_output_port) | **DELETE** /output-ports/{id} | Deletes an output port
*OutputportsApi* | [**update_output_port**](docs/OutputportsApi.md#update_output_port) | **PUT** /output-ports/{id} | Updates an output port
*PoliciesApi* | [**create_access_policy**](docs/PoliciesApi.md#create_access_policy) | **POST** /policies | Creates an access policy
*PoliciesApi* | [**get_access_policy**](docs/PoliciesApi.md#get_access_policy) | **GET** /policies/{id} | Gets an access policy
*PoliciesApi* | [**get_access_policy_for_resource**](docs/PoliciesApi.md#get_access_policy_for_resource) | **GET** /policies/{action}/{resource} | Gets an access policy for the specified action and resource
*PoliciesApi* | [**remove_access_policy**](docs/PoliciesApi.md#remove_access_policy) | **DELETE** /policies/{id} | Deletes an access policy
*PoliciesApi* | [**update_access_policy**](docs/PoliciesApi.md#update_access_policy) | **PUT** /policies/{id} | Updates a access policy
*ProcessgroupsApi* | [**copy_snippet**](docs/ProcessgroupsApi.md#copy_snippet) | **POST** /process-groups/{id}/snippet-instance | Copies a snippet and discards it.
*ProcessgroupsApi* | [**create_connection**](docs/ProcessgroupsApi.md#create_connection) | **POST** /process-groups/{id}/connections | Creates a connection
*ProcessgroupsApi* | [**create_controller_service**](docs/ProcessgroupsApi.md#create_controller_service) | **POST** /process-groups/{id}/controller-services | Creates a new controller service
*ProcessgroupsApi* | [**create_funnel**](docs/ProcessgroupsApi.md#create_funnel) | **POST** /process-groups/{id}/funnels | Creates a funnel
*ProcessgroupsApi* | [**create_input_port**](docs/ProcessgroupsApi.md#create_input_port) | **POST** /process-groups/{id}/input-ports | Creates an input port
*ProcessgroupsApi* | [**create_label**](docs/ProcessgroupsApi.md#create_label) | **POST** /process-groups/{id}/labels | Creates a label
*ProcessgroupsApi* | [**create_output_port**](docs/ProcessgroupsApi.md#create_output_port) | **POST** /process-groups/{id}/output-ports | Creates an output port
*ProcessgroupsApi* | [**create_process_group**](docs/ProcessgroupsApi.md#create_process_group) | **POST** /process-groups/{id}/process-groups | Creates a process group
*ProcessgroupsApi* | [**create_processor**](docs/ProcessgroupsApi.md#create_processor) | **POST** /process-groups/{id}/processors | Creates a new processor
*ProcessgroupsApi* | [**create_remote_process_group**](docs/ProcessgroupsApi.md#create_remote_process_group) | **POST** /process-groups/{id}/remote-process-groups | Creates a new process group
*ProcessgroupsApi* | [**create_template**](docs/ProcessgroupsApi.md#create_template) | **POST** /process-groups/{id}/templates | Creates a template and discards the specified snippet.
*ProcessgroupsApi* | [**get_connections**](docs/ProcessgroupsApi.md#get_connections) | **GET** /process-groups/{id}/connections | Gets all connections
*ProcessgroupsApi* | [**get_funnels**](docs/ProcessgroupsApi.md#get_funnels) | **GET** /process-groups/{id}/funnels | Gets all funnels
*ProcessgroupsApi* | [**get_input_ports**](docs/ProcessgroupsApi.md#get_input_ports) | **GET** /process-groups/{id}/input-ports | Gets all input ports
*ProcessgroupsApi* | [**get_labels**](docs/ProcessgroupsApi.md#get_labels) | **GET** /process-groups/{id}/labels | Gets all labels
*ProcessgroupsApi* | [**get_output_ports**](docs/ProcessgroupsApi.md#get_output_ports) | **GET** /process-groups/{id}/output-ports | Gets all output ports
*ProcessgroupsApi* | [**get_process_group**](docs/ProcessgroupsApi.md#get_process_group) | **GET** /process-groups/{id} | Gets a process group
*ProcessgroupsApi* | [**get_process_groups**](docs/ProcessgroupsApi.md#get_process_groups) | **GET** /process-groups/{id}/process-groups | Gets all process groups
*ProcessgroupsApi* | [**get_processors**](docs/ProcessgroupsApi.md#get_processors) | **GET** /process-groups/{id}/processors | Gets all processors
*ProcessgroupsApi* | [**get_remote_process_groups**](docs/ProcessgroupsApi.md#get_remote_process_groups) | **GET** /process-groups/{id}/remote-process-groups | Gets all remote process groups
*ProcessgroupsApi* | [**import_template**](docs/ProcessgroupsApi.md#import_template) | **POST** /process-groups/{id}/templates/import | Imports a template
*ProcessgroupsApi* | [**instantiate_template**](docs/ProcessgroupsApi.md#instantiate_template) | **POST** /process-groups/{id}/template-instance | Instantiates a template
*ProcessgroupsApi* | [**remove_process_group**](docs/ProcessgroupsApi.md#remove_process_group) | **DELETE** /process-groups/{id} | Deletes a process group
*ProcessgroupsApi* | [**update_process_group**](docs/ProcessgroupsApi.md#update_process_group) | **PUT** /process-groups/{id} | Updates a process group
*ProcessgroupsApi* | [**upload_template**](docs/ProcessgroupsApi.md#upload_template) | **POST** /process-groups/{id}/templates/upload | Uploads a template
*ProcessorsApi* | [**clear_state**](docs/ProcessorsApi.md#clear_state) | **POST** /processors/{id}/state/clear-requests | Clears the state for a processor
*ProcessorsApi* | [**delete_processor**](docs/ProcessorsApi.md#delete_processor) | **DELETE** /processors/{id} | Deletes a processor
*ProcessorsApi* | [**get_processor**](docs/ProcessorsApi.md#get_processor) | **GET** /processors/{id} | Gets a processor
*ProcessorsApi* | [**get_property_descriptor**](docs/ProcessorsApi.md#get_property_descriptor) | **GET** /processors/{id}/descriptors | Gets the descriptor for a processor property
*ProcessorsApi* | [**get_state**](docs/ProcessorsApi.md#get_state) | **GET** /processors/{id}/state | Gets the state for a processor
*ProcessorsApi* | [**update_processor**](docs/ProcessorsApi.md#update_processor) | **PUT** /processors/{id} | Updates a processor
*ProvenanceApi* | [**delete_lineage**](docs/ProvenanceApi.md#delete_lineage) | **DELETE** /provenance/lineage/{id} | Deletes a lineage query
*ProvenanceApi* | [**delete_provenance**](docs/ProvenanceApi.md#delete_provenance) | **DELETE** /provenance/{id} | Deletes a provenance query
*ProvenanceApi* | [**get_lineage**](docs/ProvenanceApi.md#get_lineage) | **GET** /provenance/lineage/{id} | Gets a lineage query
*ProvenanceApi* | [**get_provenance**](docs/ProvenanceApi.md#get_provenance) | **GET** /provenance/{id} | Gets a provenance query
*ProvenanceApi* | [**get_search_options**](docs/ProvenanceApi.md#get_search_options) | **GET** /provenance/search-options | Gets the searchable attributes for provenance events
*ProvenanceApi* | [**submit_lineage_request**](docs/ProvenanceApi.md#submit_lineage_request) | **POST** /provenance/lineage | Submits a lineage query
*ProvenanceApi* | [**submit_provenance_request**](docs/ProvenanceApi.md#submit_provenance_request) | **POST** /provenance | Submits a provenance query
*ProvenanceeventsApi* | [**get_input_content**](docs/ProvenanceeventsApi.md#get_input_content) | **GET** /provenance-events/{id}/content/input | Gets the input content for a provenance event
*ProvenanceeventsApi* | [**get_output_content**](docs/ProvenanceeventsApi.md#get_output_content) | **GET** /provenance-events/{id}/content/output | Gets the output content for a provenance event
*ProvenanceeventsApi* | [**get_provenance_event**](docs/ProvenanceeventsApi.md#get_provenance_event) | **GET** /provenance-events/{id} | Gets a provenance event
*ProvenanceeventsApi* | [**submit_replay**](docs/ProvenanceeventsApi.md#submit_replay) | **POST** /provenance-events/replays | Replays content from a provenance event
*RemoteprocessgroupsApi* | [**get_remote_process_group**](docs/RemoteprocessgroupsApi.md#get_remote_process_group) | **GET** /remote-process-groups/{id} | Gets a remote process group
*RemoteprocessgroupsApi* | [**remove_remote_process_group**](docs/RemoteprocessgroupsApi.md#remove_remote_process_group) | **DELETE** /remote-process-groups/{id} | Deletes a remote process group
*RemoteprocessgroupsApi* | [**update_remote_process_group**](docs/RemoteprocessgroupsApi.md#update_remote_process_group) | **PUT** /remote-process-groups/{id} | Updates a remote process group
*RemoteprocessgroupsApi* | [**update_remote_process_group_input_port**](docs/RemoteprocessgroupsApi.md#update_remote_process_group_input_port) | **PUT** /remote-process-groups/{id}/input-ports/{port-id} | Updates a remote port
*RemoteprocessgroupsApi* | [**update_remote_process_group_output_port**](docs/RemoteprocessgroupsApi.md#update_remote_process_group_output_port) | **PUT** /remote-process-groups/{id}/output-ports/{port-id} | Updates a remote port
*ReportingtasksApi* | [**clear_state**](docs/ReportingtasksApi.md#clear_state) | **POST** /reporting-tasks/{id}/state/clear-requests | Clears the state for a reporting task
*ReportingtasksApi* | [**get_property_descriptor**](docs/ReportingtasksApi.md#get_property_descriptor) | **GET** /reporting-tasks/{id}/descriptors | Gets a reporting task property descriptor
*ReportingtasksApi* | [**get_reporting_task**](docs/ReportingtasksApi.md#get_reporting_task) | **GET** /reporting-tasks/{id} | Gets a reporting task
*ReportingtasksApi* | [**get_state**](docs/ReportingtasksApi.md#get_state) | **GET** /reporting-tasks/{id}/state | Gets the state for a reporting task
*ReportingtasksApi* | [**remove_reporting_task**](docs/ReportingtasksApi.md#remove_reporting_task) | **DELETE** /reporting-tasks/{id} | Deletes a reporting task
*ReportingtasksApi* | [**update_reporting_task**](docs/ReportingtasksApi.md#update_reporting_task) | **PUT** /reporting-tasks/{id} | Updates a reporting task
*ResourcesApi* | [**get_resources**](docs/ResourcesApi.md#get_resources) | **GET** /resources | Gets the available resources that support access/authorization policies
*SitetositeApi* | [**get_peers**](docs/SitetositeApi.md#get_peers) | **GET** /site-to-site/peers | Returns the available Peers and its status of this NiFi
*SitetositeApi* | [**get_site_to_site_details**](docs/SitetositeApi.md#get_site_to_site_details) | **GET** /site-to-site | Returns the details about this NiFi necessary to communicate via site to site
*SnippetsApi* | [**create_snippet**](docs/SnippetsApi.md#create_snippet) | **POST** /snippets | Creates a snippet. The snippet will be automatically discarded if not used in a subsequent request after 1 minute.
*SnippetsApi* | [**delete_snippet**](docs/SnippetsApi.md#delete_snippet) | **DELETE** /snippets/{id} | Deletes the components in a snippet and discards the snippet
*SnippetsApi* | [**update_snippet**](docs/SnippetsApi.md#update_snippet) | **PUT** /snippets/{id} | Move&#39;s the components in this Snippet into a new Process Group and discards the snippet
*SystemdiagnosticsApi* | [**get_system_diagnostics**](docs/SystemdiagnosticsApi.md#get_system_diagnostics) | **GET** /system-diagnostics | Gets the diagnostics for the system NiFi is running on
*TemplatesApi* | [**export_template**](docs/TemplatesApi.md#export_template) | **GET** /templates/{id}/download | Exports a template
*TemplatesApi* | [**remove_template**](docs/TemplatesApi.md#remove_template) | **DELETE** /templates/{id} | Deletes a template
*TenantsApi* | [**create_user**](docs/TenantsApi.md#create_user) | **POST** /tenants/users | Creates a user
*TenantsApi* | [**create_user_group**](docs/TenantsApi.md#create_user_group) | **POST** /tenants/user-groups | Creates a user group
*TenantsApi* | [**get_user**](docs/TenantsApi.md#get_user) | **GET** /tenants/users/{id} | Gets a user
*TenantsApi* | [**get_user_group**](docs/TenantsApi.md#get_user_group) | **GET** /tenants/user-groups/{id} | Gets a user group
*TenantsApi* | [**get_user_groups**](docs/TenantsApi.md#get_user_groups) | **GET** /tenants/user-groups | Gets all user groups
*TenantsApi* | [**get_users**](docs/TenantsApi.md#get_users) | **GET** /tenants/users | Gets all users
*TenantsApi* | [**remove_user**](docs/TenantsApi.md#remove_user) | **DELETE** /tenants/users/{id} | Deletes a user
*TenantsApi* | [**remove_user_group**](docs/TenantsApi.md#remove_user_group) | **DELETE** /tenants/user-groups/{id} | Deletes a user group
*TenantsApi* | [**search_cluster**](docs/TenantsApi.md#search_cluster) | **GET** /tenants/search-results | Searches for a tenant with the specified identity
*TenantsApi* | [**update_user**](docs/TenantsApi.md#update_user) | **PUT** /tenants/users/{id} | Updates a user
*TenantsApi* | [**update_user_group**](docs/TenantsApi.md#update_user_group) | **PUT** /tenants/user-groups/{id} | Updates a user group


## Documentation For Models

 - [AboutDTO](docs/AboutDTO.md)
 - [AboutEntity](docs/AboutEntity.md)
 - [AccessConfigurationDTO](docs/AccessConfigurationDTO.md)
 - [AccessConfigurationEntity](docs/AccessConfigurationEntity.md)
 - [AccessPolicyDTO](docs/AccessPolicyDTO.md)
 - [AccessPolicyEntity](docs/AccessPolicyEntity.md)
 - [AccessPolicySummaryDTO](docs/AccessPolicySummaryDTO.md)
 - [AccessPolicySummaryEntity](docs/AccessPolicySummaryEntity.md)
 - [AccessStatusDTO](docs/AccessStatusDTO.md)
 - [AccessStatusEntity](docs/AccessStatusEntity.md)
 - [ActionDTO](docs/ActionDTO.md)
 - [ActionDetailsDTO](docs/ActionDetailsDTO.md)
 - [ActionEntity](docs/ActionEntity.md)
 - [AllowableValueDTO](docs/AllowableValueDTO.md)
 - [AllowableValueEntity](docs/AllowableValueEntity.md)
 - [AttributeDTO](docs/AttributeDTO.md)
 - [BannerDTO](docs/BannerDTO.md)
 - [BannerEntity](docs/BannerEntity.md)
 - [BatchSettingsDTO](docs/BatchSettingsDTO.md)
 - [BulletinBoardDTO](docs/BulletinBoardDTO.md)
 - [BulletinBoardEntity](docs/BulletinBoardEntity.md)
 - [BulletinDTO](docs/BulletinDTO.md)
 - [BulletinEntity](docs/BulletinEntity.md)
 - [BundleDTO](docs/BundleDTO.md)
 - [ClusteSummaryEntity](docs/ClusteSummaryEntity.md)
 - [ClusterDTO](docs/ClusterDTO.md)
 - [ClusterEntity](docs/ClusterEntity.md)
 - [ClusterSearchResultsEntity](docs/ClusterSearchResultsEntity.md)
 - [ClusterSummaryDTO](docs/ClusterSummaryDTO.md)
 - [ComponentDetailsDTO](docs/ComponentDetailsDTO.md)
 - [ComponentHistoryDTO](docs/ComponentHistoryDTO.md)
 - [ComponentHistoryEntity](docs/ComponentHistoryEntity.md)
 - [ComponentReferenceDTO](docs/ComponentReferenceDTO.md)
 - [ComponentReferenceEntity](docs/ComponentReferenceEntity.md)
 - [ComponentSearchResultDTO](docs/ComponentSearchResultDTO.md)
 - [ComponentStateDTO](docs/ComponentStateDTO.md)
 - [ConnectableDTO](docs/ConnectableDTO.md)
 - [ConnectionDTO](docs/ConnectionDTO.md)
 - [ConnectionEntity](docs/ConnectionEntity.md)
 - [ConnectionStatusDTO](docs/ConnectionStatusDTO.md)
 - [ConnectionStatusEntity](docs/ConnectionStatusEntity.md)
 - [ConnectionStatusSnapshotDTO](docs/ConnectionStatusSnapshotDTO.md)
 - [ConnectionStatusSnapshotEntity](docs/ConnectionStatusSnapshotEntity.md)
 - [ConnectionsEntity](docs/ConnectionsEntity.md)
 - [ControllerBulletinsEntity](docs/ControllerBulletinsEntity.md)
 - [ControllerConfigurationDTO](docs/ControllerConfigurationDTO.md)
 - [ControllerConfigurationEntity](docs/ControllerConfigurationEntity.md)
 - [ControllerDTO](docs/ControllerDTO.md)
 - [ControllerEntity](docs/ControllerEntity.md)
 - [ControllerServiceApiDTO](docs/ControllerServiceApiDTO.md)
 - [ControllerServiceDTO](docs/ControllerServiceDTO.md)
 - [ControllerServiceEntity](docs/ControllerServiceEntity.md)
 - [ControllerServiceReferencingComponentDTO](docs/ControllerServiceReferencingComponentDTO.md)
 - [ControllerServiceReferencingComponentEntity](docs/ControllerServiceReferencingComponentEntity.md)
 - [ControllerServiceReferencingComponentsEntity](docs/ControllerServiceReferencingComponentsEntity.md)
 - [ControllerServiceTypesEntity](docs/ControllerServiceTypesEntity.md)
 - [ControllerServicesEntity](docs/ControllerServicesEntity.md)
 - [ControllerStatusDTO](docs/ControllerStatusDTO.md)
 - [ControllerStatusEntity](docs/ControllerStatusEntity.md)
 - [CopySnippetRequestEntity](docs/CopySnippetRequestEntity.md)
 - [CounterDTO](docs/CounterDTO.md)
 - [CounterEntity](docs/CounterEntity.md)
 - [CountersDTO](docs/CountersDTO.md)
 - [CountersEntity](docs/CountersEntity.md)
 - [CountersSnapshotDTO](docs/CountersSnapshotDTO.md)
 - [CreateTemplateRequestEntity](docs/CreateTemplateRequestEntity.md)
 - [CurrentUserEntity](docs/CurrentUserEntity.md)
 - [DimensionsDTO](docs/DimensionsDTO.md)
 - [DocumentedTypeDTO](docs/DocumentedTypeDTO.md)
 - [DropRequestDTO](docs/DropRequestDTO.md)
 - [DropRequestEntity](docs/DropRequestEntity.md)
 - [FlowBreadcrumbDTO](docs/FlowBreadcrumbDTO.md)
 - [FlowBreadcrumbEntity](docs/FlowBreadcrumbEntity.md)
 - [FlowConfigurationDTO](docs/FlowConfigurationDTO.md)
 - [FlowConfigurationEntity](docs/FlowConfigurationEntity.md)
 - [FlowDTO](docs/FlowDTO.md)
 - [FlowEntity](docs/FlowEntity.md)
 - [FlowFileSummaryDTO](docs/FlowFileSummaryDTO.md)
 - [FlowSnippetDTO](docs/FlowSnippetDTO.md)
 - [FlowSnippetEntity](docs/FlowSnippetEntity.md)
 - [FunnelDTO](docs/FunnelDTO.md)
 - [FunnelEntity](docs/FunnelEntity.md)
 - [FunnelsEntity](docs/FunnelsEntity.md)
 - [GarbageCollectionDTO](docs/GarbageCollectionDTO.md)
 - [HistoryDTO](docs/HistoryDTO.md)
 - [HistoryEntity](docs/HistoryEntity.md)
 - [InputPortsEntity](docs/InputPortsEntity.md)
 - [InstantiateTemplateRequestEntity](docs/InstantiateTemplateRequestEntity.md)
 - [LabelDTO](docs/LabelDTO.md)
 - [LabelEntity](docs/LabelEntity.md)
 - [LabelsEntity](docs/LabelsEntity.md)
 - [LineageDTO](docs/LineageDTO.md)
 - [LineageEntity](docs/LineageEntity.md)
 - [LineageRequestDTO](docs/LineageRequestDTO.md)
 - [LineageResultsDTO](docs/LineageResultsDTO.md)
 - [ListingRequestDTO](docs/ListingRequestDTO.md)
 - [ListingRequestEntity](docs/ListingRequestEntity.md)
 - [NodeConnectionStatusSnapshotDTO](docs/NodeConnectionStatusSnapshotDTO.md)
 - [NodeCountersSnapshotDTO](docs/NodeCountersSnapshotDTO.md)
 - [NodeDTO](docs/NodeDTO.md)
 - [NodeEntity](docs/NodeEntity.md)
 - [NodeEventDTO](docs/NodeEventDTO.md)
 - [NodePortStatusSnapshotDTO](docs/NodePortStatusSnapshotDTO.md)
 - [NodeProcessGroupStatusSnapshotDTO](docs/NodeProcessGroupStatusSnapshotDTO.md)
 - [NodeProcessorStatusSnapshotDTO](docs/NodeProcessorStatusSnapshotDTO.md)
 - [NodeRemoteProcessGroupStatusSnapshotDTO](docs/NodeRemoteProcessGroupStatusSnapshotDTO.md)
 - [NodeSearchResultDTO](docs/NodeSearchResultDTO.md)
 - [NodeStatusSnapshotsDTO](docs/NodeStatusSnapshotsDTO.md)
 - [NodeSystemDiagnosticsSnapshotDTO](docs/NodeSystemDiagnosticsSnapshotDTO.md)
 - [OutputPortsEntity](docs/OutputPortsEntity.md)
 - [PeerDTO](docs/PeerDTO.md)
 - [PeersEntity](docs/PeersEntity.md)
 - [PermissionsDTO](docs/PermissionsDTO.md)
 - [PortDTO](docs/PortDTO.md)
 - [PortEntity](docs/PortEntity.md)
 - [PortStatusDTO](docs/PortStatusDTO.md)
 - [PortStatusEntity](docs/PortStatusEntity.md)
 - [PortStatusSnapshotDTO](docs/PortStatusSnapshotDTO.md)
 - [PortStatusSnapshotEntity](docs/PortStatusSnapshotEntity.md)
 - [PositionDTO](docs/PositionDTO.md)
 - [PreviousValueDTO](docs/PreviousValueDTO.md)
 - [PrioritizerTypesEntity](docs/PrioritizerTypesEntity.md)
 - [ProcessGroupDTO](docs/ProcessGroupDTO.md)
 - [ProcessGroupEntity](docs/ProcessGroupEntity.md)
 - [ProcessGroupFlowDTO](docs/ProcessGroupFlowDTO.md)
 - [ProcessGroupFlowEntity](docs/ProcessGroupFlowEntity.md)
 - [ProcessGroupStatusDTO](docs/ProcessGroupStatusDTO.md)
 - [ProcessGroupStatusEntity](docs/ProcessGroupStatusEntity.md)
 - [ProcessGroupStatusSnapshotDTO](docs/ProcessGroupStatusSnapshotDTO.md)
 - [ProcessGroupStatusSnapshotEntity](docs/ProcessGroupStatusSnapshotEntity.md)
 - [ProcessorConfigDTO](docs/ProcessorConfigDTO.md)
 - [ProcessorDTO](docs/ProcessorDTO.md)
 - [ProcessorEntity](docs/ProcessorEntity.md)
 - [ProcessorStatusDTO](docs/ProcessorStatusDTO.md)
 - [ProcessorStatusEntity](docs/ProcessorStatusEntity.md)
 - [ProcessorStatusSnapshotDTO](docs/ProcessorStatusSnapshotDTO.md)
 - [ProcessorStatusSnapshotEntity](docs/ProcessorStatusSnapshotEntity.md)
 - [ProcessorTypesEntity](docs/ProcessorTypesEntity.md)
 - [ProcessorsEntity](docs/ProcessorsEntity.md)
 - [PropertyDescriptorDTO](docs/PropertyDescriptorDTO.md)
 - [PropertyDescriptorEntity](docs/PropertyDescriptorEntity.md)
 - [PropertyHistoryDTO](docs/PropertyHistoryDTO.md)
 - [ProvenanceDTO](docs/ProvenanceDTO.md)
 - [ProvenanceEntity](docs/ProvenanceEntity.md)
 - [ProvenanceEventDTO](docs/ProvenanceEventDTO.md)
 - [ProvenanceEventEntity](docs/ProvenanceEventEntity.md)
 - [ProvenanceLinkDTO](docs/ProvenanceLinkDTO.md)
 - [ProvenanceNodeDTO](docs/ProvenanceNodeDTO.md)
 - [ProvenanceOptionsDTO](docs/ProvenanceOptionsDTO.md)
 - [ProvenanceOptionsEntity](docs/ProvenanceOptionsEntity.md)
 - [ProvenanceRequestDTO](docs/ProvenanceRequestDTO.md)
 - [ProvenanceResultsDTO](docs/ProvenanceResultsDTO.md)
 - [ProvenanceSearchableFieldDTO](docs/ProvenanceSearchableFieldDTO.md)
 - [QueueSizeDTO](docs/QueueSizeDTO.md)
 - [RelationshipDTO](docs/RelationshipDTO.md)
 - [RemoteProcessGroupContentsDTO](docs/RemoteProcessGroupContentsDTO.md)
 - [RemoteProcessGroupDTO](docs/RemoteProcessGroupDTO.md)
 - [RemoteProcessGroupEntity](docs/RemoteProcessGroupEntity.md)
 - [RemoteProcessGroupPortDTO](docs/RemoteProcessGroupPortDTO.md)
 - [RemoteProcessGroupPortEntity](docs/RemoteProcessGroupPortEntity.md)
 - [RemoteProcessGroupStatusDTO](docs/RemoteProcessGroupStatusDTO.md)
 - [RemoteProcessGroupStatusSnapshotDTO](docs/RemoteProcessGroupStatusSnapshotDTO.md)
 - [RemoteProcessGroupStatusSnapshotEntity](docs/RemoteProcessGroupStatusSnapshotEntity.md)
 - [RemoteProcessGroupsEntity](docs/RemoteProcessGroupsEntity.md)
 - [ReportingTaskDTO](docs/ReportingTaskDTO.md)
 - [ReportingTaskEntity](docs/ReportingTaskEntity.md)
 - [ReportingTaskTypesEntity](docs/ReportingTaskTypesEntity.md)
 - [ReportingTasksEntity](docs/ReportingTasksEntity.md)
 - [ResourceDTO](docs/ResourceDTO.md)
 - [ResourcesEntity](docs/ResourcesEntity.md)
 - [RevisionDTO](docs/RevisionDTO.md)
 - [ScheduleComponentsEntity](docs/ScheduleComponentsEntity.md)
 - [SearchResultsDTO](docs/SearchResultsDTO.md)
 - [SearchResultsEntity](docs/SearchResultsEntity.md)
 - [Set](docs/Set.md)
 - [SnippetDTO](docs/SnippetDTO.md)
 - [SnippetEntity](docs/SnippetEntity.md)
 - [StateEntryDTO](docs/StateEntryDTO.md)
 - [StateMapDTO](docs/StateMapDTO.md)
 - [StatusDescriptorDTO](docs/StatusDescriptorDTO.md)
 - [StatusHistoryDTO](docs/StatusHistoryDTO.md)
 - [StatusHistoryEntity](docs/StatusHistoryEntity.md)
 - [StatusSnapshotDTO](docs/StatusSnapshotDTO.md)
 - [StorageUsageDTO](docs/StorageUsageDTO.md)
 - [StreamingOutput](docs/StreamingOutput.md)
 - [SubmitReplayRequestEntity](docs/SubmitReplayRequestEntity.md)
 - [SystemDiagnosticsDTO](docs/SystemDiagnosticsDTO.md)
 - [SystemDiagnosticsEntity](docs/SystemDiagnosticsEntity.md)
 - [SystemDiagnosticsSnapshotDTO](docs/SystemDiagnosticsSnapshotDTO.md)
 - [TemplateDTO](docs/TemplateDTO.md)
 - [TemplateEntity](docs/TemplateEntity.md)
 - [TemplatesEntity](docs/TemplatesEntity.md)
 - [TenantDTO](docs/TenantDTO.md)
 - [TenantEntity](docs/TenantEntity.md)
 - [TenantsEntity](docs/TenantsEntity.md)
 - [TransactionResultEntity](docs/TransactionResultEntity.md)
 - [UpdateControllerServiceReferenceRequestEntity](docs/UpdateControllerServiceReferenceRequestEntity.md)
 - [UserDTO](docs/UserDTO.md)
 - [UserEntity](docs/UserEntity.md)
 - [UserGroupDTO](docs/UserGroupDTO.md)
 - [UserGroupEntity](docs/UserGroupEntity.md)
 - [UserGroupsEntity](docs/UserGroupsEntity.md)
 - [UsersEntity](docs/UsersEntity.md)
 - [VersionInfoDTO](docs/VersionInfoDTO.md)


## Documentation For Authorization

TBD


## Author

Apache NiFi: dev@nifi.apache.org  
nifi-python-swagger-client: chaffelson@gmail.com

