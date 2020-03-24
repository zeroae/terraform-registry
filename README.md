# zeroae/terraform-registry
Zero A.E.'s [12-Factor][12-factor] codebase of the [Terraform Registry API][registry-api] implemented using [Chalice][chalice] and [PynamoDB][pynamodb].

## Similar projects (and likely more complete), in alphabetical order
  - [apparentlymart/terraform-aws-tf-registry](https://github.com/apparentlymart/terraform-aws-tf-registry)
  - [apparentlymart/terraform-simple-registry](https://github.com/apparentlymart/terraform-simple-registry)
  - [dflook/terraform-registry](https://github.com/dflook/terraform-registry)
  - [outsideris/citizen](https://github.com/outsideris/citizen)
  - [rmb938/tf-registry](https://github.com/rmb938/tf-registry)

## Deployments
1. Requirements: 
    - conda
    - docker-compose
    - keybase (for secrets)

1. Clone the repository and secrets
    ```shell script
    git clone https://github.com/zeroae/terraform-registry.git
    cd terraform-registry

    # Submodules did not work
    git clone keybase://team/zeroae/terraform-registry-secrets secrets
    # Fix the acme.json file permissions. 600 is not committable to Git
    find . -type f -name acme.json -exec chmod 600 {} \;
    ```
   
1. Create conda environment
    ```shell script
    conda env create 
    conda activate terraform-registry
    ```` 

### Local Deployment
1. Additional Requirements:
    - docker-compose

1. Start the app on local mode
    ```shell script
    docker-compose up -d
    ```
   
1. Wait until the `app`, `backend` and `manage` services are healthy
    ```shell script
    watch docker-compose ps  
    ```
   
1. Attach to the Management container 
    ```shell script
    docker attach terraform-registry_manage_1
    ./manage.py --help
    ```

    1. Initialize the Database
       ```shell script
       ./manage.py db init
       ./manage.py db restore tests/integration/local.ddb
       ```
    1. Verify Terraform CLI can reach the local server
        ```shell script
        cd tests/integration/tf.local.zeroae.net
        rm -rf .terraform
        terraform init
        ```
    1. Detach from the container
        ```shell script
        Ctrl-P + Ctrl-Q
        ```

1. Verify Terraform CLI can reach the local registry (outside management)
    ```shell script
    cd tests/integration/tf.local.zeroae.net
    rm -rf .terraform
    terraform init
    ```

## AWS Deployment
1. Use Chalice to (re)deploy the `dev` stage to AWS
    ```shell script
    export AWS_CONFIG_FILE="./secrets/aws/config"
    chalice --stage=dev deploy
    ```

1. Initialize the Database
    ```shell script
    ./manage.py --stage=dev db init

    # Optionally load content into the DynamoDB backend
    ./manage.py --stage=dev db restore tests/integration/local.ddb
    ```

1. Configure a custom domain name(`tf.zeroae.net`) to point to the dev stage
    1. Use the AWS Certificate Manager to register a certificate for `tf.zeroae.net`
    1. Create a custom domain name in API Gateway
        - `tf.zeroae.net`
        - Edge Optimized
        - TLS 1.2
        - The ACM certificate from the previous step
    1. Create an ALIAS DNS record for `tf.zeroae.net` pointing to the API Gateway Name and ZONE ID from previous step.
    1. Add API Mapping for the dev Stage

1. Verify Terraform CLI can reach the remote server
    ```shell script
    cd tests/integration/tf.zeroae.net
    rm -rf .terraform
    terraform init
    ```

---
[12-factor]: https://www.12factor.net
[chalice]: https://github.com/aws/chalice
[pynamodb]: https://github.com/pynamodb/PynamoDB
[registry-api]: https://www.terraform.io/docs/registry/api.html
