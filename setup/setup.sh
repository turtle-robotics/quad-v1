user=robot
ip=quad1.local

ws=$(dirname $(readlink -f $BASH_SOURCE[0]))/.. # workspace path
# lsyncd -rsyncssh $ws $ip /home/$user/quad -nodaemon
alias setup="USER=$user envsubst < $ws/setup/robot.service | ssh $user@$ip 'sudo tee /etc/systemd/system/robot.service; systemctl daemon-reload'"
alias upload="rsync -av $ws $user@$ip:/home/$user/ --exclude-from .gitignore"
alias run="ssh $user@$ip 'sudo systemctl start robot.service'"
alias stop="ssh $user@$ip 'sudo systemctl stop robot.service'"
alias enable="ssh $user@$ip 'sudo systemctl enable robot.service'"
alias disable="ssh $user@$ip 'sudo systemctl disable robot.service'"