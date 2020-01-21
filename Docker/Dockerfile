FROM python:3.7.5
COPY . /home
WORKDIR /home
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
EXPOSE 1883
EXPOSE 5000
EXPOSE 8083
CMD python3 ./DroneSimCore/SimulationCore.py -b 143.129.39.127
