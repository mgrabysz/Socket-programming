#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdlib.h>

#define BUF_SIZE 1

int main(int argc, char *argv[]) {

    // read address and port from argument
    if (argc != 3) {
        printf("expected address and port arguments");
        return 1;
    }
    int address_arg = inet_addr(argv[1]);
    int port_arg = (int) strtol(argv[2], NULL, 0);

    // create needed structures
    char buf[BUF_SIZE];
    struct sockaddr_in client_address = {
            .sin_family = AF_INET,
            .sin_addr.s_addr = htonl(INADDR_ANY),
            .sin_port = htons(0)
    };
    struct sockaddr_in server_address = {
            .sin_family = AF_INET,
            .sin_addr.s_addr = address_arg,
            .sin_port = htons(port_arg)
    };

    // create socket
    int socket_fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (socket_fd < 0) {
        perror("error creating socket");
        return 1;
    }

    // bind socket to local address
    int bind_result = bind(socket_fd, (const struct sockaddr *) &client_address, sizeof(client_address));
    if (bind_result < 0) {
        perror("error binding socket");
        return 1;
    }

    // send data
    for (int countdown = 9; countdown >= 0; countdown--) {
        buf[0] = '0' + countdown;

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
