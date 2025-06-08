#!/usr/bin/env python3
"""
Configuration and shared constants for the Diagram Generator MCP Server
"""

import os
import logging
from pathlib import Path

try:
    from fastmcp import FastMCP
    from diagrams import Diagram, Cluster, Edge

    # Cloud providers
    from diagrams.aws.compute import EC2, ECS, EKS, Lambda
    from diagrams.aws.database import RDS, Dynamodb, ElastiCache, Redshift
    from diagrams.aws.network import ELB, Route53, VPC, InternetGateway, APIGateway
    from diagrams.aws.storage import S3
    from diagrams.aws.integration import SQS, SNS

    # Azure Analytics
    from diagrams.azure.analytics import (
        AnalysisServices, DataExplorerClusters, DataFactories, DataLakeAnalytics,
        DataLakeStoreGen1, Databricks, EventHubClusters, EventHubs,
        Hdinsightclusters, LogAnalyticsWorkspaces, StreamAnalyticsJobs, SynapseAnalytics
    )

    # Azure Compute
    from diagrams.azure.compute import (
        AppServices, AutomanagedVM, AvailabilitySets, BatchAccounts,
        CitrixVirtualDesktopsEssentials, CloudServicesClassic, CloudServices,
        CloudsimpleVirtualMachines, ContainerApps, ContainerInstances, ContainerRegistries,
        DiskEncryptionSets, DiskSnapshots, Disks, FunctionApps, ImageDefinitions,
        ImageVersions, KubernetesServices, MeshApplications, OsImages, SAPHANAOnAzure,
        ServiceFabricClusters, SharedImageGalleries, SpringCloud, VMClassic, VMImages,
        VMLinux, VMScaleSet, VMWindows, VM, Workspaces
    )

    # Azure Database
    from diagrams.azure.database import (
        BlobStorage, CacheForRedis, CosmosDb, DataExplorerClusters, DataFactory,
        DataLake, DatabaseForMariadbServers, DatabaseForMysqlServers,
        DatabaseForPostgresqlServers, ElasticDatabasePools, ElasticJobAgents,
        InstancePools, ManagedDatabases, SQLDatabases, SQLDatawarehouse,
        SQLManagedInstances, SQLServerStretchDatabases, SQLServers, SQLVM, SQL,
        SsisLiftAndShiftIr, SynapseAnalytics, VirtualClusters, VirtualDatacenter
    )

    # Azure DevOps
    from diagrams.azure.devops import (
        ApplicationInsights, Artifacts, Boards, Devops, DevtestLabs, LabServices,
        Pipelines, Repos, TestPlans
    )

    # Azure General
    from diagrams.azure.general import (
        Allresources, Azurehome, Developertools, Helpsupport, Information,
        Managementgroups, Marketplace, Quickstartcenter, Recent, Reservations,
        Resource, Resourcegroups, Servicehealth, Shareddashboard, Subscriptions,
        Support, Supportrequests, Tag, Tags, Templates, Twousericon,
        Userhealthicon, Usericon, Userprivacy, Userresource, Whatsnew
    )

    # Azure Identity
    from diagrams.azure.identity import (
        AccessReview, ActiveDirectoryConnectHealth, ActiveDirectory, ADB2C,
        ADDomainServices, ADIdentityProtection, ADPrivilegedIdentityManagement,
        AppRegistrations, ConditionalAccess, EnterpriseApplications, Groups,
        IdentityGovernance, InformationProtection, ManagedIdentities, Users
    )

    # Azure Integration
    from diagrams.azure.integration import (
        APIForFhir, APIManagement, AppConfiguration, DataCatalog, EventGridDomains,
        EventGridSubscriptions, EventGridTopics, IntegrationAccounts,
        IntegrationServiceEnvironments, LogicAppsCustomConnector, LogicApps,
        PartnerTopic, SendgridAccounts, ServiceBusRelays, ServiceBus,
        ServiceCatalogManagedApplicationDefinitions, SoftwareAsAService,
        StorsimpleDeviceManagers, SystemTopic
    )

    # Azure IoT
    from diagrams.azure.iot import (
        DeviceProvisioningServices, DigitalTwins, IotCentralApplications,
        IotHubSecurity, IotHub, Maps, Sphere, TimeSeriesInsightsEnvironments,
        TimeSeriesInsightsEventsSources, Windows10IotCoreServices
    )

    # Azure Migration
    from diagrams.azure.migration import (
        DataBoxEdge, DataBox, DatabaseMigrationServices, MigrationProjects,
        RecoveryServicesVaults
    )

    # Azure ML
    from diagrams.azure.ml import (
        AzureOpenAI, AzureSpeedToText, BatchAI, BotServices, CognitiveServices,
        GenomicsAccounts, MachineLearningServiceWorkspaces,
        MachineLearningStudioWebServicePlans, MachineLearningStudioWebServices,
        MachineLearningStudioWorkspaces
    )

    # Azure Mobile
    from diagrams.azure.mobile import (
        AppServiceMobile, MobileEngagement, NotificationHubs
    )

    # Azure Monitor
    from diagrams.azure.monitor import (
        ChangeAnalysis, Logs, Metrics, Monitor
    )

    # Azure Network
    from diagrams.azure.network import (
        ApplicationGateway, ApplicationSecurityGroups, CDNProfiles, Connections,
        DDOSProtectionPlans, DNSPrivateZones, DNSZones, ExpressrouteCircuits,
        Firewall, FrontDoors, LoadBalancers, LocalNetworkGateways, NetworkInterfaces,
        NetworkSecurityGroupsClassic, NetworkWatcher, OnPremisesDataGateways,
        PrivateEndpoint, PublicIpAddresses, ReservedIpAddressesClassic,
        RouteFilters, RouteTables, ServiceEndpointPolicies, Subnets,
        TrafficManagerProfiles, VirtualNetworkClassic, VirtualNetworkGateways,
        VirtualNetworks, VirtualWans
    )

    # Azure Security
    from diagrams.azure.security import (
        ApplicationSecurityGroups as SecurityApplicationSecurityGroups, ConditionalAccess as SecurityConditionalAccess,
        Defender, ExtendedSecurityUpdates, KeyVaults, SecurityCenter, Sentinel
    )

    # Azure Storage
    from diagrams.azure.storage import (
        ArchiveStorage, Azurefxtedgefiler, BlobStorage as StorageBlobStorage,
        DataBoxEdgeDataBoxGateway, DataBox as StorageDataBox, DataLakeStorage,
        GeneralStorage, NetappFiles, QueuesStorage, StorageAccountsClassic,
        StorageAccounts, StorageExplorer, StorageSyncServices, StorsimpleDataManagers,
        StorsimpleDeviceManagers as StorageStorsimpleDeviceManagers, TableStorage
    )

    # Azure Web
    from diagrams.azure.web import (
        APIConnections, AppServiceCertificates, AppServiceDomains,
        AppServiceEnvironments, AppServicePlans, AppServices as WebAppServices,
        MediaServices, NotificationHubNamespaces, Search, Signalr
    )

    # Kubernetes imports - all components from the official documentation
    from diagrams.k8s.chaos import ChaosMesh, LitmusChaos
    from diagrams.k8s.clusterconfig import HPA, Limits, Quota
    from diagrams.k8s.compute import Cronjob, Deployment, DaemonSet, Job, Pod, ReplicaSet, StatefulSet
    from diagrams.k8s.controlplane import APIServer, CCM, ControllerManager, KubeProxy, Kubelet, Scheduler
    from diagrams.k8s.ecosystem import ExternalDns, Helm, Krew, Kustomize
    from diagrams.k8s.group import Namespace
    from diagrams.k8s.infra import ETCD, Master, Node
    from diagrams.k8s.network import Endpoint, Ingress, NetworkPolicy, Service
    from diagrams.k8s.others import CRD, PSP
    from diagrams.k8s.podconfig import ConfigMap, Secret
    from diagrams.k8s.rbac import ClusterRole, ClusterRoleBinding, Group, Role, RoleBinding, ServiceAccount, User
    from diagrams.k8s.storage import PV, PVC, StorageClass, Volume

    from diagrams.onprem.compute import Server
    from diagrams.onprem.database import PostgreSQL, MySQL, MongoDB
    from diagrams.onprem.network import Nginx, Apache
    from diagrams.onprem.inmemory import Redis
    from diagrams.onprem.queue import Kafka, RabbitMQ
    from diagrams.onprem.monitoring import Prometheus, Grafana

except ImportError as e:
    print(f"Error importing dependencies: {e}")
    print("Please install the required dependencies:")
    print("pip install fastmcp diagrams python-dotenv pillow")
    exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Volume mount path where diagrams will be saved
# Can be overridden via DIAGRAM_OUTPUT_DIR environment variable
VOLUME_MOUNT_PATH = os.environ.get("DIAGRAM_OUTPUT_DIR", "/tmp")

# Component mappings for easy lookup
COMPONENT_MAPPINGS = {
    "aws": {
        "compute": {
            "ec2": EC2,
            "ecs": ECS,
            "eks": EKS,
            "lambda": Lambda
        },
        "database": {
            "rds": RDS,
            "dynamodb": Dynamodb,
            "elasticache": ElastiCache,
            "redshift": Redshift
        },
        "network": {
            "elb": ELB,
            "route53": Route53,
            "vpc": VPC,
            "igw": InternetGateway,
            "apigateway": APIGateway
        },
        "storage": {
            "s3": S3
        },
        "integration": {
            "sqs": SQS,
            "sns": SNS
        }
    },
    "azure": {
        "analytics": {
            "analysisservices": AnalysisServices,
            "dataexplorerclusters": DataExplorerClusters,
            "datafactories": DataFactories,
            "datalakeanalytics": DataLakeAnalytics,
            "datalakestoregen1": DataLakeStoreGen1,
            "databricks": Databricks,
            "eventhubclusters": EventHubClusters,
            "eventhubs": EventHubs,
            "hdinsightclusters": Hdinsightclusters,
            "loganalyticsworkspaces": LogAnalyticsWorkspaces,
            "streamanalyticsjobs": StreamAnalyticsJobs,
            "synapseanalytics": SynapseAnalytics
        },
        "compute": {
            "appservices": AppServices,
            "automanagedvm": AutomanagedVM,
            "availabilitysets": AvailabilitySets,
            "batchaccounts": BatchAccounts,
            "citrixvirtualdesktopsessentials": CitrixVirtualDesktopsEssentials,
            "cloudservicesclassic": CloudServicesClassic,
            "cloudservices": CloudServices,
            "cloudsimplevirtualmachines": CloudsimpleVirtualMachines,
            "containerapps": ContainerApps,
            "containerinstances": ContainerInstances,
            "containerregistries": ContainerRegistries,
            "diskencryptionsets": DiskEncryptionSets,
            "disksnapshots": DiskSnapshots,
            "disks": Disks,
            "functionapps": FunctionApps,
            "imagedefinitions": ImageDefinitions,
            "imageversions": ImageVersions,
            "kubernetesservices": KubernetesServices,
            "meshapplications": MeshApplications,
            "osimages": OsImages,
            "saphanaonazure": SAPHANAOnAzure,
            "servicefabricclusters": ServiceFabricClusters,
            "sharedimagegalleries": SharedImageGalleries,
            "springcloud": SpringCloud,
            "vmclassic": VMClassic,
            "vmimages": VMImages,
            "vmlinux": VMLinux,
            "vmscaleset": VMScaleSet,
            "vmwindows": VMWindows,
            "vm": VM,
            "workspaces": Workspaces,
            # Legacy aliases
            "aci": ContainerInstances,
            "aks": KubernetesServices,
            "functions": FunctionApps
        },
        "database": {
            "blobstorage": BlobStorage,
            "cacheredis": CacheForRedis,
            "cosmosdb": CosmosDb,
            "dataexplorerclusters": DataExplorerClusters,
            "datafactory": DataFactory,
            "datalake": DataLake,
            "mariadbservers": DatabaseForMariadbServers,
            "mysqlservers": DatabaseForMysqlServers,
            "postgresqlservers": DatabaseForPostgresqlServers,
            "elasticdatabasepools": ElasticDatabasePools,
            "elasticjobagents": ElasticJobAgents,
            "instancepools": InstancePools,
            "manageddatabases": ManagedDatabases,
            "sqldatabases": SQLDatabases,
            "sqldatawarehouse": SQLDatawarehouse,
            "sqlmanagedinstances": SQLManagedInstances,
            "sqlserverstretchdatabases": SQLServerStretchDatabases,
            "sqlservers": SQLServers,
            "sqlvm": SQLVM,
            "sql": SQL,
            "ssisliftandshiftir": SsisLiftAndShiftIr,
            "synapseanalytics": SynapseAnalytics,
            "virtualclusters": VirtualClusters,
            "virtualdatacenter": VirtualDatacenter,
            # Legacy aliases
            "redis": CacheForRedis
        },
        "devops": {
            "applicationinsights": ApplicationInsights,
            "artifacts": Artifacts,
            "boards": Boards,
            "devops": Devops,
            "devtestlabs": DevtestLabs,
            "labservices": LabServices,
            "pipelines": Pipelines,
            "repos": Repos,
            "testplans": TestPlans
        },
        "general": {
            "allresources": Allresources,
            "azurehome": Azurehome,
            "developertools": Developertools,
            "helpsupport": Helpsupport,
            "information": Information,
            "managementgroups": Managementgroups,
            "marketplace": Marketplace,
            "quickstartcenter": Quickstartcenter,
            "recent": Recent,
            "reservations": Reservations,
            "resource": Resource,
            "resourcegroups": Resourcegroups,
            "servicehealth": Servicehealth,
            "shareddashboard": Shareddashboard,
            "subscriptions": Subscriptions,
            "support": Support,
            "supportrequests": Supportrequests,
            "tag": Tag,
            "tags": Tags,
            "templates": Templates,
            "twousericon": Twousericon,
            "userhealthicon": Userhealthicon,
            "usericon": Usericon,
            "userprivacy": Userprivacy,
            "userresource": Userresource,
            "whatsnew": Whatsnew
        },
        "identity": {
            "accessreview": AccessReview,
            "activedirectoryconnecthealth": ActiveDirectoryConnectHealth,
            "activedirectory": ActiveDirectory,
            "adb2c": ADB2C,
            "addomainservices": ADDomainServices,
            "adidentityprotection": ADIdentityProtection,
            "adprivilegedidentitymanagement": ADPrivilegedIdentityManagement,
            "appregistrations": AppRegistrations,
            "conditionalaccess": ConditionalAccess,
            "enterpriseapplications": EnterpriseApplications,
            "groups": Groups,
            "identitygovernance": IdentityGovernance,
            "informationprotection": InformationProtection,
            "managedidentities": ManagedIdentities,
            "users": Users
        },
        "integration": {
            "apiforfhir": APIForFhir,
            "apimanagement": APIManagement,
            "appconfiguration": AppConfiguration,
            "datacatalog": DataCatalog,
            "eventgriddomains": EventGridDomains,
            "eventgridsubscriptions": EventGridSubscriptions,
            "eventgridtopics": EventGridTopics,
            "integrationaccounts": IntegrationAccounts,
            "integrationserviceenvironments": IntegrationServiceEnvironments,
            "logicappscustomconnector": LogicAppsCustomConnector,
            "logicapps": LogicApps,
            "partnertopic": PartnerTopic,
            "sendgridaccounts": SendgridAccounts,
            "servicebusrelays": ServiceBusRelays,
            "servicebus": ServiceBus,
            "servicecatalogmanagedapplicationdefinitions": ServiceCatalogManagedApplicationDefinitions,
            "softwareasaservice": SoftwareAsAService,
            "storsimpledevicemanagers": StorsimpleDeviceManagers,
            "systemtopic": SystemTopic,
            # Legacy aliases
            "eventgrid": EventGridTopics
        },
        "iot": {
            "deviceprovisioningservices": DeviceProvisioningServices,
            "digitaltwins": DigitalTwins,
            "iotcentralapplications": IotCentralApplications,
            "iothubsecurity": IotHubSecurity,
            "iothub": IotHub,
            "maps": Maps,
            "sphere": Sphere,
            "timeseriesinsightsenvironments": TimeSeriesInsightsEnvironments,
            "timeseriesinsightseventssources": TimeSeriesInsightsEventsSources,
            "windows10iotcoreservices": Windows10IotCoreServices
        },
        "migration": {
            "databoxedge": DataBoxEdge,
            "databox": DataBox,
            "databasemigrationservices": DatabaseMigrationServices,
            "migrationprojects": MigrationProjects,
            "recoveryservicesvaults": RecoveryServicesVaults
        },
        "ml": {
            "azureopenai": AzureOpenAI,
            "azurespeedtotext": AzureSpeedToText,
            "batchai": BatchAI,
            "botservices": BotServices,
            "cognitiveservices": CognitiveServices,
            "genomicsaccounts": GenomicsAccounts,
            "machinelearningserviceworkspaces": MachineLearningServiceWorkspaces,
            "machinelearingstudiowebserviceplans": MachineLearningStudioWebServicePlans,
            "machinelearingstudiowebservices": MachineLearningStudioWebServices,
            "machinelearingstudioworkspaces": MachineLearningStudioWorkspaces
        },
        "mobile": {
            "appservicemobile": AppServiceMobile,
            "mobileengagement": MobileEngagement,
            "notificationhubs": NotificationHubs
        },
        "monitor": {
            "changeanalysis": ChangeAnalysis,
            "logs": Logs,
            "metrics": Metrics,
            "monitor": Monitor
        },
        "network": {
            "applicationgateway": ApplicationGateway,
            "applicationsecuritygroups": ApplicationSecurityGroups,
            "cdnprofiles": CDNProfiles,
            "connections": Connections,
            "ddosprotectionplans": DDOSProtectionPlans,
            "dnsprivatezones": DNSPrivateZones,
            "dnszones": DNSZones,
            "expressroutecircuits": ExpressrouteCircuits,
            "firewall": Firewall,
            "frontdoors": FrontDoors,
            "loadbalancers": LoadBalancers,
            "localnetworkgateways": LocalNetworkGateways,
            "networkinterfaces": NetworkInterfaces,
            "networksecuritygroupsclassic": NetworkSecurityGroupsClassic,
            "networkwatcher": NetworkWatcher,
            "onpremisesdatagateways": OnPremisesDataGateways,
            "privateendpoint": PrivateEndpoint,
            "publicipaddresses": PublicIpAddresses,
            "reservedipaddressesclassic": ReservedIpAddressesClassic,
            "routefilters": RouteFilters,
            "routetables": RouteTables,
            "serviceendpointpolicies": ServiceEndpointPolicies,
            "subnets": Subnets,
            "trafficmanagerprofiles": TrafficManagerProfiles,
            "virtualnetworkclassic": VirtualNetworkClassic,
            "virtualnetworkgateways": VirtualNetworkGateways,
            "virtualnetworks": VirtualNetworks,
            "virtualwans": VirtualWans,
            # Legacy aliases
            "lb": LoadBalancers,
            "appgw": ApplicationGateway,
            "vnet": VirtualNetworks
        },
        "security": {
            "applicationsecuritygroups": SecurityApplicationSecurityGroups,
            "conditionalaccess": SecurityConditionalAccess,
            "defender": Defender,
            "extendedsecurityupdates": ExtendedSecurityUpdates,
            "keyvaults": KeyVaults,
            "securitycenter": SecurityCenter,
            "sentinel": Sentinel
        },
        "storage": {
            "archivestorage": ArchiveStorage,
            "azurefxtedgefiler": Azurefxtedgefiler,
            "blobstorage": StorageBlobStorage,
            "databoxedgedataboxgateway": DataBoxEdgeDataBoxGateway,
            "databox": StorageDataBox,
            "datalakestorage": DataLakeStorage,
            "generalstorage": GeneralStorage,
            "netappfiles": NetappFiles,
            "queuesstorage": QueuesStorage,
            "storageaccountsclassic": StorageAccountsClassic,
            "storageaccounts": StorageAccounts,
            "storageexplorer": StorageExplorer,
            "storagesyncservices": StorageSyncServices,
            "storsimpledatamanagers": StorsimpleDataManagers,
            "storsimpledevicemanagers": StorageStorsimpleDeviceManagers,
            "tablestorage": TableStorage,
            # Legacy aliases
            "storage": StorageAccounts,
            "blob": StorageBlobStorage
        },
        "web": {
            "apiconnections": APIConnections,
            "appservicecertificates": AppServiceCertificates,
            "appservicedomains": AppServiceDomains,
            "appserviceenvironments": AppServiceEnvironments,
            "appserviceplans": AppServicePlans,
            "appservices": WebAppServices,
            "mediaservices": MediaServices,
            "notificationhubnamespaces": NotificationHubNamespaces,
            "search": Search,
            "signalr": Signalr
        }
    },
    "k8s": {
        "chaos": {
            "chaosmesh": ChaosMesh,
            "litmuschaos": LitmusChaos
        },
        "clusterconfig": {
            "hpa": HPA,
            "horizontalpodautoscaler": HPA,  # alias
            "limits": Limits,
            "limitrange": Limits,  # alias
            "quota": Quota
        },
        "compute": {
            "cronjob": Cronjob,
            "deployment": Deployment,
            "daemonset": DaemonSet,
            "ds": DaemonSet,  # alias
            "job": Job,
            "pod": Pod,
            "replicaset": ReplicaSet,
            "rs": ReplicaSet,  # alias
            "statefulset": StatefulSet,
            "sts": StatefulSet  # alias
        },
        "controlplane": {
            "apiserver": APIServer,
            "api": APIServer,  # alias
            "ccm": CCM,
            "controllermanager": ControllerManager,
            "cm": ControllerManager,  # alias
            "kubeproxy": KubeProxy,
            "kproxy": KubeProxy,  # alias
            "kubelet": Kubelet,
            "scheduler": Scheduler,
            "sched": Scheduler  # alias
        },
        "ecosystem": {
            "externaldns": ExternalDns,
            "helm": Helm,
            "krew": Krew,
            "kustomize": Kustomize
        },
        "group": {
            "namespace": Namespace,
            "ns": Namespace  # alias
        },
        "infra": {
            "etcd": ETCD,
            "master": Master,
            "node": Node
        },
        "network": {
            "endpoint": Endpoint,
            "ep": Endpoint,  # alias
            "ingress": Ingress,
            "ing": Ingress,  # alias
            "networkpolicy": NetworkPolicy,
            "netpol": NetworkPolicy,  # alias
            "service": Service,
            "svc": Service  # alias
        },
        "others": {
            "crd": CRD,
            "psp": PSP
        },
        "podconfig": {
            "configmap": ConfigMap,
            "cm": ConfigMap,  # alias
            "secret": Secret
        },
        "rbac": {
            "clusterrole": ClusterRole,
            "crole": ClusterRole,  # alias
            "clusterrolebinding": ClusterRoleBinding,
            "crb": ClusterRoleBinding,  # alias
            "group": Group,
            "role": Role,
            "rolebinding": RoleBinding,
            "rb": RoleBinding,  # alias
            "serviceaccount": ServiceAccount,
            "sa": ServiceAccount,  # alias
            "user": User
        },
        "storage": {
            "persistentvolume": PV,
            "pv": PV,  # alias
            "persistentvolumeclaim": PVC,
            "pvc": PVC,  # alias
            "storageclass": StorageClass,
            "sc": StorageClass,  # alias
            "volume": Volume,
            "vol": Volume  # alias
        }
    },
    "onprem": {
        "compute": {
            "server": Server
        },
        "database": {
            "postgresql": PostgreSQL,
            "mysql": MySQL,
            "mongodb": MongoDB
        },
        "network": {
            "nginx": Nginx,
            "apache": Apache
        },
        "memory": {
            "redis": Redis
        },
        "queue": {
            "kafka": Kafka,
            "rabbitmq": RabbitMQ
        },
        "monitoring": {
            "prometheus": Prometheus,
            "grafana": Grafana
        }
    }
}
