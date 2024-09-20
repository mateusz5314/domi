source env.sh

xhost +local:docker

if ! docker volume inspect $docker_home_vol > /dev/null 2>&1; then
    echo "Docker home volume: $docker_home_vol does not exist. Creating, this might take a while."
    mkdir -p $docker_home_vol
    docker volume create $docker_home_vol
fi

devices=""
for arg in "$@"
do
    devices+="--device $arg "
done
devices=${devices% }

docker run -it --rm \
    -v $docker_home_vol:/home/$usr_name \
    -v $domi_root:/home/$usr_name/domi \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ~/.ssh:/home/$usr_name/.ssh \
    $devices \
    -e DISPLAY:$DISPLAY \
    -e TERM=xterm-256color \
    --network=host \
    --name=$container_name \
    $image_name \
    bash
