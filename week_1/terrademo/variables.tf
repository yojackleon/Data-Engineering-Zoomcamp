variable "credentials" {
  description = "My GCS creds"
  default     = "./keys/my-creds.json"
}

variable "project" {
  description = "Project name"
  default     = "terraform-demo-448812"

}
variable "location" {
  description = "Project Location"
  default     = "EU"

}
variable "region" {
  description = "Region"
  default     = "europe-west2"

}

variable "bq_dataset_name" {
  description = "My BigQuery dataset name"
  default     = "demo_dataset"
}
variable "gcs_bucket_name" {
  description = "My Storage bucket name"
  default     = "terraform-demo-448812-terra-bucket"

}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"

}