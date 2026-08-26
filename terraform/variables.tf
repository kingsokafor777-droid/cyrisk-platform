variable "environment_label" {
  type        = string
  description = "Reference-only environment label; it does not select or create an infrastructure environment."
  default     = "reference"

  validation {
    condition     = contains(["reference", "development", "staging", "production"], var.environment_label)
    error_message = "environment_label must be a declared reference label."
  }
}

variable "enable_deployment" {
  type        = bool
  description = "Must remain false in this provider-free source release."
  default     = false

  validation {
    condition     = var.enable_deployment == false
    error_message = "This reference module intentionally prohibits deployment."
  }
}
