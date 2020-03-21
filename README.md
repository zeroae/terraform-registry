# zeroae/terraform-registry
Zero A.E.'s [12-Factor][12-factor] codebase of the [Terraform Registry API][registry-api] implemented using [Chalice][chalice] and [PynamoDB][pynamodb].

## Similar projects (and likely more complete), in alphabetical order
  - [apparentlymart/terraform-aws-tf-registry](https://github.com/apparentlymart/terraform-aws-tf-registry)
  - [apparentlymart/terraform-simple-registry](https://github.com/apparentlymart/terraform-simple-registry)
  - [dflook/terraform-registry](https://github.com/dflook/terraform-registry)
  - [outsideris/citizen](https://github.com/outsideris/citizen)
  - [rmb938/tf-registry](https://github.com/rmb938/tf-registry)
  
## Local Deployment
1. Requirements: 
    - conda
    - docker-compose
    - keybase

1. Clone the repository
    ```shell script
    git clone https://github.com/zeroae/terraform-registry.git
    cd terraform-registry
    ``` 
   
1. Clone the secrets (submodules did not work)
    ```shell script
    git clone keybase://team/zeroae/terraform-registry-secrets secrets
   
    # Fix the acme.json file permissions. 600 is not committable to Git
    find . -type f -name acme.json -exec chmod 600 {} \;
    ```
   
1. Create conda environment
    ```shell script
    conda env create 
    conda activate terraform-registry
    ```` 
   
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

---
[12-factor]: https://www.12factor.net
[chalice]: https://github.com/aws/chalice
[pynamodb]: https://github.com/pynamodb/PynamoDB
[registry-api]: https://www.terraform.io/docs/registry/api.html
