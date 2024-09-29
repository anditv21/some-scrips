sudo nano /etc/systemd/system/nginx_error_log_discord.service

[Unit]
Description=Nginx Error Log to Discord
After=network.target

[Service]
ExecStart=/usr/bin/python3 /root/error_reporter.py
WorkingDirectory=/root
Restart=always
User=root

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reload
sudo systemctl enable nginx_error_log_discord
sudo systemctl start nginx_error_log_discord
sudo systemctl status nginx_error_log_discord