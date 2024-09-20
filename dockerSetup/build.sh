source env.sh

echo "Building docker image: $image_name"
echo "Docker user: $usr_name"
echo "User home location on host: $docker_home"

docker build --build-arg USR_NAME=$usr_name -t $image_name $env_script_dir