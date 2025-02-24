from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException

# Load Kubernetes config
config.load_kube_config()

# API clients
api = client.CustomObjectsApi()
apps_api = client.AppsV1Api()

# Watch for database events
watcher = watch.Watch()

for event in watcher.stream(api.list_namespaced_custom_object, group="example.com", version="v1", namespace="default", plural="databases"):
    db = event["object"]
    db_name = db["metadata"]["name"]
    db_engine = db["spec"]["engine"]
    db_version = db["spec"]["version"]
    replicas = db["spec"]["replicas"]

    if event["type"] == "ADDED":
        print(f"📌 Database {db_name} detected! Deploying {db_engine} {db_version} with {replicas} replicas.")
        
        # Create a PostgreSQL Deployment dynamically
        deployment = client.V1Deployment(
            metadata=client.V1ObjectMeta(name=db_name),
            spec=client.V1DeploymentSpec(
                replicas=replicas,
                selector={"matchLabels": {"app": db_name}},
                template=client.V1PodTemplateSpec(
                    metadata=client.V1ObjectMeta(labels={"app": db_name}),
                    spec=client.V1PodSpec(
                        containers=[
                            client.V1Container(
                                name=db_name,
                                image=f"postgres:{db_version}",
                                ports=[client.V1ContainerPort(container_port=5432)],
                                env=[
                                    client.V1EnvVar(name="POSTGRES_USER", value="admin"),
                                    client.V1EnvVar(name="POSTGRES_PASSWORD", value="password"),
                                    client.V1EnvVar(name="POSTGRES_DB", value=db_name),
                                ],
                            )
                        ]
                    ),
                ),
            ),
        )
        
        # Apply deployment
        try:
            apps_api.create_namespaced_deployment(namespace="default", body=deployment)
            print(f"✅ Deployed PostgreSQL {db_version} for {db_name}")
        except ApiException as e:
            print(f"⚠️ Error deploying {db_name}: {e}")

    elif event["type"] == "DELETED":
        print(f"❌ Database {db_name} deleted! Cleaning up resources.")
        
        # Delete the PostgreSQL Deployment associated with the deleted DB
        try:
            apps_api.delete_namespaced_deployment(name=db_name, namespace="default")
            print(f"✅ Deleted Deployment for {db_name}")
        except ApiException as e:
            if e.status == 404:
                print(f"⚠️ Deployment for {db_name} not found (already deleted).")
            else:
                print(f"⚠️ Error deleting deployment for {db_name}: {e}")

        # Optionally, delete related services or other resources
        # Example: Delete a service if created for the DB
        try:
            core_api = client.CoreV1Api()
            core_api.delete_namespaced_service(name=db_name, namespace="default")
            print(f"✅ Deleted Service for {db_name}")
        except ApiException as e:
            if e.status == 404:
                print(f"⚠️ Service for {db_name} not found (already deleted).")
            else:
                print(f"⚠️ Error deleting service for {db_name}: {e}")
