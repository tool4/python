cp get_stocks.service /etc/systemd/system/
sudo systemctl daemon-reload

sudo systemctl stop get_stocks.service
sudo systemctl enable get_stocks.service
sudo systemctl start get_stocks.service
