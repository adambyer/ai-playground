output "cluster_name" {
  value = module.eks.cluster_name
}

output "cluster_arn" {
  value = module.eks.cluster_arn
}

output "cluster_endpoint" {
  value = module.eks.cluster_endpoint
}

output "app_repository_url" {
  value = aws_ecr_repository.app_repository.repository_url
}

output "ollama_repository_url" {
  value = aws_ecr_repository.ollama_repository.repository_url
}
