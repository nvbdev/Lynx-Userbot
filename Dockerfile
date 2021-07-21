# Docker Tag Images, Using Python Slim Buster.
FROM kenzo404/lynxuser:Buster
# ==========================================
#              Lynx - Userbot
# ==========================================
RUN git clone -b Beta https://github.com/KENZO-404/Lynx-Userbot/tree/Beta /home/Beta \
    && chmod 777 /home/Beta \
    && mkdir /home/Beta/bin/

# Copies config.env (if exists)
COPY ./sample_config.env ./config.env* /home/Beta/

WORKDIR /home/Beta/

# Finishim
CMD ["bash","./resource/startup/startup.sh"]
