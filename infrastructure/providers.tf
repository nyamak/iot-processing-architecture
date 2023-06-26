terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.20.0"
    }
  }

  required_version = ">= 1.4.6"
}

provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context = "<YOUR_CONFIG_CONTEXT>"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
    config_context = "<YOUR_CONFIG_CONTEXT>"
  }
}
