Install terraform, its just an exe so you have to build the directory structure and add it to your path
create a google cloud account - https://console.cloud.google.com/ 
create a project
create a service account
generate keys

to use the kyes you can put the following in the main.tf inside the provider config
credentials="path to key json file"

or use
export GOOGLE_CREDENTIALS='path to key json file'

or if you have the gcloud sdk installed 
gcloud default auth-login

in the video he uses the export method ...

so 

export GOOGLE_CREDENTIALS='c:\Study\terrademo\keys\m-creds.json'

of course that doesn't work in windows ! so you have to set the env variable using the GUI

then check using the following command in the terminal 
echo $Env:GOOGLE_CREDENTIALS

now to get the provider run

terraform init

now we're going to create a bucket
google - gcp bucket terraform and copy the example code into main.tf


then run terraform plan to see what changes will be made
terraform apply to make the changes
terraform destroy to undo the changes


Next we created a variables.tf file and added variables in the form 


variable "project" {
  description = "Project name"
  default     = "terraform-demo-448812"
}

you can then call these variables in the main.tf using var.project ( without even importing the variables file! )
the credentials file can also be added to this.
