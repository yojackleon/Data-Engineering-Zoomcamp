Setting up a cloud VM and SSH access
First we generate keys from gitbash

https://cloud.google.com/compute/docs/connect/create-ssh-keys

use the linux instructions ( eventhough you're on windows!)

cd ~
cd .ssh
ssh-keygen -t rsa -f gcp -C jleon

cat gcp.pub to see the key

go to google console -> Metadata -> ssh Keys
add key 
copy they public key in there and save

then to go VM instances and create an instance
nothing really special in the settings, he chose ubunta and and e2 standard.
then we find the external IP of our instance

then back to gitbash locally to connect to the instance

cd ~
ssh -i ~/.ssh/gcp jleon@35.242.146.170

and we're in ...

Installing anaconda
go to anaconda.com and get the linux download link 

back to the GCP instance and 

wget https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh

then
bash Anaconda3-2024.10-1-Linux-x86_64.sh
to install

open another termina window to create a ssh config file

cd ~/.ssh
touch config
then "code config" to open VSCode and edit

Host de-zoomcamp
    Hostname 35.242.146.170
    User jleon
    IdentityFile C:/Users/jackl/.ssh/gcp
    

now cd ~ and ssh de-zoomcamp gets you in to the GCP instance.


back to the anaconda installation, got this message 

Do you wish to update your shell profile to automatically initialize conda?
This will activate conda on startup and change the command prompt when activated.
If you'd prefer that conda's base environment not be activated on startup,
   run the following command when conda is activated:

conda config --set auto_activate_base false

You can undo this by running `conda init --reverse $SHELL`? [yes|no]


i hit yes for now but might need to undo that later.

log out and log in again ( ssh de-zoomcamp )
now the prompt starts with (base)

( an alternative to loging out out and in again is to run 
source .bashrc
that re-evals the .bashrc file
)

now install docker

sudo apt-get install docker.io
but before that we need to update ubunto

with 
sudo apt-get update

then install docker

now we want to connect our local VSCode to the instance in GCP.

install the remote-ssh addon in VSCode
click the green terminal icon in the bottom left
select connect to host
de-zoomcamp should come up because we have the config file.
opens another instance of VSCode and boom you're in

OK, now back to the GCP instance and we're going to clone the zoomcamp repo, not sure why yet ...

https://github.com/DataTalksClub/data-engineering-zoomcamp

copy the link from the clone menu

https://github.com/DataTalksClub/data-engineering-zoomcamp.git

git clone https://github.com/DataTalksClub/data-engineering-zoomcamp.git


Bit of back and forth here. we're back looking at docker now, its should be installed and we're goingto run it, but we need to run it without sudo using these instructions

https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md

on the virtual instance run the following

$ sudo groupadd docker
$ sudo gpasswd -a $USER docker
$ sudo service docker restart
log out and log in again to re-eval group membership

now we don't have to type sudo when running docker

try the following to test it
docker run hello-world

then we install docker compose

go to the docker compose repo
https://github.com/docker/compose
find the latest linux release and copy the link 

https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64

back to our instance in the cloud

cd ~
mkdir bin
cd bin 
wget https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64 -O docker-compose

make it executable
chmod +x docker-compose

it's now green ( if you do a ls ). test it
./docker-compose version

now add it to path
nano .bashrc

add line

export PATH="${HOME}/bin:${PATH}"

control O to save
Control X to exit

source .bashrc
to re-evaluate it ( or log out and log back in)

now we can go to data-engineering-zoomcamp/01-docker_terraform/2_docker_sql and find a docker-compose file there and run it

docker-compose up -d

check everything is running 

docker ps


then install pgcli
cd ~
pip install pgcli


ok, now log into the running instance of our database

pgcli -h localhost -U root -d ny_taxi

it ucking works !!

( if that doesn't work you can uninstall pgcli and then use conda to install it

conda install -c conda-forge pcli 
pip install -U mycli
)


OK, so everthing is installed, so how do we access the database from our local machine ? 
we need to forward the port from the virtual instance to our local machine

go to the VSCode instance running on the virtual machine
add port 5432 from the ports tab ( which comes up when you open the terminal window)
forward address will default to localhost:5432

now you can run 
pgcli -h localhost -U root -d ny_taxi
locally to access the database running in docker in the cloud instance!!

if you also forward 8080 you can access pgadmin locally on localhost:8080

OK, now to start Jupyter on the cloud instance

go back to the data-engineering-zoomcamp/01-docker_terraform/2_docker_sql directory

jupyter notebook

Back to te the cloud connected VSCode and forward 8888 to localhost:8888

open the upload-data notebook

paused at 36.46 minutes - https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=15

stopped the notebook with contrl D
docker-compose down
stopped the instance.

To restart everything
1. start the cloud instance
2. ssh in using ssh de-zoomcamp
3. cd to the course directory ( data-engineering-zoomcamp/01-docker_terraform/2_docker_sql directory)
4. docker-compose up -d
5. open VSCode, connect to host, select de-zoomcamp
6. port forward 8080, 8888, 5432 to localhost on same port

OK, next we load the taxi data files into the working directory
data-engineering-zoomcamp/01-docker_terraform/2_docker_sql directory

yellow_tripdata_2021-01.csv
taxi_zone_lookup.csv

he uses wget from the cloud instance, i just wacked it from my local drive into the VSCode instance connected to that cloud host.
then click through the commands in the upload_data.ipynd notebook to load the data

now install terraform
https://developer.hashicorp.com/terraform/install
we're going to download the AMD64 binary

https://releases.hashicorp.com/terraform/1.10.5/terraform_1.10.5_linux_amd64.zip

back to the cloud instance
cd ~
cd bin
wget https://releases.hashicorp.com/terraform/1.10.5/terraform_1.10.5_linux_amd64.zip
sudo apt-get install unzip
unzip terraform_1.10.5_linux_amd64.zip
rm terraform_1.10.5_linux_amd64.zip

test using 
cd ~
terraform -version

now we're goingto try out terraform
cd ~
cd data-engineering-zoomcamp/01-docker-terraform/1_terraform_gcp/terraform/

before that we need to give that cloud instance access to our service account for our project
so go generate some keys in json format, download them into local windows home directory under .gc, call the file ny-rides.json

then on local bash
sftp de-zoomcamp
mkdir .gc
cd .gc
put ny-rides.json

No we configure our google cloud CLI

set up key file location
export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/ny-rides.json

authenticate service account
gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS

ok, we,re ready to terraform
cd ~/data-engineering-zoomcamp/01-docker-terraform/1_terraform_gcp/terraform/terraform_basic
terraform init
terraform plan

now you can shutdown or delete the instance and go to bed.