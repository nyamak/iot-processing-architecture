terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = ">= 4.31.0"
    }
    kubernetes = {
        source = "hashicorp/kubernetes"
        version = ">= 2.13.1"
    }
  }

  required_version = ">= 0.14"
}

provider "aws" {
    profile = "default"
    region = "eu-west-1"
}

provider "kubernetes" {
    config_path = "~/.kube/config"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
  }
}
