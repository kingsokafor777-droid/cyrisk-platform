output "handoff_state" {
  description = "A declared source-reference state, not a runtime or infrastructure health claim."
  value = {
    environment_label = var.environment_label
    deployment        = "not_configured"
    providers         = "none"
    resources         = "none"
  }
}
