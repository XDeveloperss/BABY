if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/farshadpyt/BABY-KUTTY.git /BABY-KUTTY
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /BABY-KUTTY
fi
cd /evarandamattebot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 bot.py
