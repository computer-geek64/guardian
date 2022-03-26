# Guardian

### Personal home surveillance and CCTV system

## Description

Guardian is my personal home surveillance system that is currently in deployment to watch over my house.
It features **motion detection** and recording with **push notifications**, as well as **real-time streaming** for multiple users.
Both **audio and video** streaming are supported and synchronized over **native HTTP** (no additional plugins or add-ons necessary; compatible with all devices).
Furthermore, instant **in-browser event playback** is available for recorded motion events.
To adhere to strict storage requirements, the software is configured with **LRU eviction** to overwrite the oldest recorded events when storage space becomes an issue.
Unfortunately, the live streaming features are some of the most resource-intensive aspects of the server, due to the large quantity of data that needs to be processed quickly from multiple sources.
To combat this and support simultaneous streams, a **load balancer** was used in tandem with **multiprocessing.**
For the fastest inter-process communication (IPC) speeds, the project employs **shared memory** to reduce duplicate actions across processes and signal them to free up threads and memory as soon a user abandons the stream.
Guardian uses a **microservice architecture** alongside **containerization** for improved scalability (allowing for the dynamic expansion of cameras), greater resilience, fault isolation, and efficient software development.
Any **IP cameras** that support RTSP (Real Time Streaming Protocol) can be easily added to the system.
Additionally, any USB or integrated **webcams** can be used with RtspSimpleServer to emulate an IP camera and generate a live RTSP stream that is compatible with Guardian.

## Software Used for Implementation

* **Docker** for containerization
* **Docker Compose** to support efficient deployment of the project's microservice architecture
* **Flask** for the back-end web application framework (both the streaming and authentication server)
* **NGINX** as a reverse proxy and for event playback/serving static files
* **NGINX Unit** as a load balancer and WSGI production server for dynamic web application deployment
* **OpenCV** for streaming live video frames using RTSP
* **FFmpeg** to process/transform video and audio streams
* **Motion Project** for motion detection
* **RtspSimpleServer** to support IP camera emulation with webcams

## Developers

Ashish D'Souza - [@computer-geek64](https://github.com/computer-geek64)

## License

This project is licensed under the [MIT License](LICENSE).
