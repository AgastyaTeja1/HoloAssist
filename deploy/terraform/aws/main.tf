provider "aws" {
  region = var.region
}

module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.27"
  subnets         = var.subnets
  vpc_id          = var.vpc_id

  node_groups = {
    gpu = {
      desired_capacity = 1
      max_capacity     = 3
      min_capacity     = 1
      instance_types   = ["p3.2xlarge"]
      ami_type         = "AL2_x86_64_GPU"
    }
    cpu = {
      desired_capacity = 2
      instance_types   = ["t3.medium"]
    }
  }
}
