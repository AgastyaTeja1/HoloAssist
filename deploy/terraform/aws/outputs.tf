output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}
output "kubeconfig_certificate_authority_data" {
  value = module.eks.cluster_certificate_authority_data
}
