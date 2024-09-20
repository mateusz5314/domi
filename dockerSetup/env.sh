env_script_dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
usr_name=develop
docker_home_vol=domi_volume
domi_root=$(realpath $env_script_dir/../)
image_name=domi_img
container_name=domi_env
