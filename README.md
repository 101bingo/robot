# robot

#test

#git

设置邮箱地址和姓名

git config --global user.email “your_email@email.com“       //  your_email@email.com   换成自己的邮箱
 
git config --global user.name "your name"              //    youname  换成自己的英文名字   然后按回车


设置 SSH Key
ssh-keygen -t rsa -C “your_email@email.com”       //   自己的邮箱

复制  id_rsa 密钥

cat /home/XXX /.ssh/id_rsa.pub

git remote add origin git@github.com:XXXXX/XXXX     // 自己上一步设置的邮箱用户名<br>git push -u origin master


git status 查看工作区代码相对于暂存区的差别
git add . 将当前目录下修改的所有代码从工作区添加到暂存区 . 代表当前目录
git commit -m ‘注释’ 将缓存区内容添加到本地仓库
git push origin master 将本地版本库推送到远程服务器，
git merge 分支名 合并分支
