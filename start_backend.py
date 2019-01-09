
import argparse
import DroneBackend.Backend

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--backbone", help="Define backbone url.")
    parser.add_argument("-i", "--ip", help="Define IP address of backend.")
    parser.add_argument("-m", "--mqtt", help="Define base mqtt-topic.")

    args = parser.parse_args()

    backbone_url = "http://smartcity.ddns.net:10000" if not args.backbone else args.backbone
    mqtt = "smartcity/drones" if not args.mqtt else args.mqtt
    ip = "0.0.0.0" if not args.ip else args.ip

    DroneBackend.Backend.start_backend(ip, mqtt, backbone_url)
