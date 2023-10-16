# Caikit Embeddings TLS Enablement

Enable TLS and `cross cluster` access via a route.  

## Update the caikit configuration
- The [config.yml](../../demo/config.yml) file must be updated to include where to find the server certificate and key. Note, the locations under /mnt are refenced in the yaml described below. The image must then be re-built after updating the config.yml.

```yaml
# Caikit model configuration
# Relative paths are relative to where the config is loaded
runtime:
    library: caikit_embeddings
    grpc: {"enabled": True}
    http: {"enabled": True}
    # All models in this directory are loaded at boot time
    local_models_dir: "../models"
    tls:
        server:
            key: /mnt/tls.key
            cert: /mnt/tls.crt
```
## Deploying the certificates

- The TLS certificates and keys are deployed within a OCP secret.  
- Create the `tls-secret` secret from the deployment yaml file.

- To manually create the certificates and keys, insuring the correct Subject Alternative Names (SANs) were added to the certificates. The SANs are set up to work with our routes and DNS.  
- If you want to create your own certificates/keys you can do the following:

1. Create a server-ext.cnf file with the following contents (these are for our clusters). 
 ```txt
  subjectAltName=DNS:*.hostname,DNS:servicename,IP:0.0.0.0`
```
2. Generate CA's private key and self-signed certificate
```bash
openssl req -x509 -newkey rsa:4096 -days 3650 -nodes -keyout tls/ca-key.pem -out tls/ca-cert.pem -subj "/C=US/ST=New York/L=Yorktown Heights/O=Company/OU=Company/CN=certificate-authority name"
```
3. Generate web server's private key and certificate signing request (CSR)
```bash
 openssl req -newkey rsa:4096 -nodes -keyout tls/server-key.pem -out tls/server-req.pem -subj "/C=US/ST=New York/L=Yorktown Heights/O=IBM/OU=Company/CN=*.hostname.com/emailAddress=email@host.com"
```
4. Use CA's private key to sign web server's CSR and get back the signed certificate
```bash
 openssl x509 -req -in tls/server-req.pem -days 730 -CA tls/ca-cert.pem -CAkey tls/ca-key.pem -CAcreateserial -out tls/server-cert.pem -extfile ./server-ext.cnf
```
5. Then copy the ca-cert, server-cert, and server key to secret


## Apply deployment, service, and gRPC route
- Apply [deployment-caikit-embeddings.yaml](../../deployment/deployment-caikit-embeddings.yaml)
> Note: The TLS secrets MUST BE mounted within this file!
- Update the `hostname` value in the route config then apply.