Deploy the NGINX Gateway Fabric CRDs
Stable release
kubectl apply -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.6.1/deploy/crds.yaml

Deploy NGINX Gateway Fabric
Note:
By default, NGINX Gateway Fabric is installed in the nginx-gateway namespace. You can deploy in another namespace by modifying the manifest files.
Default
AWS NLB
Azure
NGINX Plus
Experimental
NGINX Plus Experimental
NodePort
OpenShift
Deploys NGINX Gateway Fabric with NGINX OSS.

Copy
kubectl apply -f https://raw.githubusercontent.com/nginx/nginx-gateway-fabric/v1.6.1/deploy/default/deploy.yaml
Verify the Deployment
To confirm that NGINX Gateway Fabric is running, check the pods in the nginx-gateway namespace:

Copy
kubectl get pods -n nginx-gateway
The output should look similar to this (note that the pod name will include a unique string):

Copy
NAME READY STATUS RESTARTS AGE
nginx-gateway-5d4f4c7db7-xk2kq 2/2 Running 0 112s
