# Script created from the commands here
# https://www.raspberrypi.org/documentation/raspbian/updating.md
# Note: This will only update for the current major version, it will not update to a newer major version

# Update system's package list
sudo apt update

# upgrade all installed packages to their latest versions
sudo apt full-upgrade

# Install Sense Hat
sudo apt install sense-hat

# Note, will need to perform a `sudo reboot` after this
# Maybe that should be part of this script?
