#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUF_SIZE 64
#define PORT 8080

int main() {
    char buf[BUF_SIZE];

    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = htonl(INADDR_ANY);
    server_address.sin_port = htons(PORT);

    struct sockaddr_in client_address;
    socklen_t client_address_len = sizeof(client_address);

    // create socket
    int socket_fd = socket(
            AF_INET,
            SOCK_DGRAM,
            0
    );
    if (socket_fd < 0) {
        perror("error creating socket");
        return 1;
    }

    // bind socket to address
    int bind_result = bind(
            socket_fd,
            (const struct sockaddr *) &server_address,
            sizeof(server_address)
    );
    if (bind_result < 0) {
        perror("error binding socket");
        return 1;
    }

    // listen for datagrams
    while (1) {
        printf("Listening...\n");
        int bytes_received = (int) recvfrom(
                socket_fd, buf, sizeof(buf), 0,
                (struct sockaddr *) &client_address, &client_address_len
        );
        if (bytes_received < 0) {
            perror("error receiving data");
            return 1;
        }

        printf(
                "Received %d bytes from %s:\n%.*s\n\n",
                bytes_received, inet_ntoa(client_address.sin_addr), bytes_received, buf
        );
    }

}
