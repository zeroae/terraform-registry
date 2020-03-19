# zeroae/terraform-registry
Zero A.E.'s [12-Factor][12-factor] codebase of the [Terraform Registry API][registry-api] implemented using [Chalice][chalice] and [PynamoDB][pynamodb].

## Similar projects (and likely more complete), in alphabetical order
  - [apparentlymart/terraform-aws-tf-registry](https://github.com/apparentlymart/terraform-aws-tf-registry)
  - [apparentlymart/terraform-simple-registry](https://github.com/apparentlymart/terraform-simple-registry)
  - [dflook/terraform-registry](https://github.com/dflook/terraform-registry)
  - [outsideris/citizen](https://github.com/outsideris/citizen)
  - [rmb938/tf-registry](https://github.com/rmb938/tf-registry)
  
## Deployment on AWS

## Development
1. Requirements: 
    - conda
    - docker

1. Clone the repository
    ```shell script
    git clone https://github.com/zeroae/terraform-registry.git
    cd terraform-registry
    ``` 
   
1. Create the conda environment and activate it
    ```shell script
    conda env create
    conda activate terraform-registry
    ```

1. Start the app on local mode
    ```shell script
    docker-compose up -d
    ```
   
1. Attach to the Management container (Detach Ctrl-P + Ctrl-Q)
    ```shell script
    docker attach terraform-registry_management_1
    conda activate terraform-registry
    ./manage.py --help
    ```
   
1. Initialize Database (from inside management container)
    ```shell script
    ./manage.py db init
    ./manage.py record import terraform-aws-modules/vpc/2.29.0
    ```


---
[12-factor]: https://www.12factor.net
[chalice]: https://github.com/aws/chalice
[pynamodb]: https://github.com/pynamodb/PynamoDB
[registry-api]: https://www.terraform.io/docs/registry/api.html
