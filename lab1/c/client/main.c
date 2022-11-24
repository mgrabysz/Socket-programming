#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define BUF_SIZE 64

int main() {

    char buf[BUF_SIZE] = "Hello!";

    struct sockaddr_in client_address;
    client_address.sin_family = AF_INET;
    client_address.sin_addr.s_addr = htonl(INADDR_ANY);
    client_address.sin_port = htons(0);

    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr("127.0.0.1");
    server_address.sin_port = htons(8080);

    // create socket
    int socket_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (socket_fd < 0) {
        perror("error creating socket");
        return 1;
    }

    // bind to local address
    int bind_result = bind(socket_fd, (const struct sockaddr *) &client_address, sizeof(client_address));
    if (bind_result < 0) {
        perror("error binding socket");
        return 1;
    }

    // send data
    for (int countdown = 10; countdown >= 0; countdown--) {
        if (countdown == 0) {
            sprintf(buf, "boom!");
        } else {
            sprintf(buf, "%d", countdown);
        }

        int bytes_sent = (int) sendto(
                socket_fd, buf, sizeof(buf), 0,
                (const struct sockaddr *) &server_address, sizeof(server_address)
        );
        if (bytes_sent < 0) {
            perror("error sending data");
            return 1;
        }

        printf("sent %d bytes to server\n", bytes_sent);

    }

    return 0;
}
