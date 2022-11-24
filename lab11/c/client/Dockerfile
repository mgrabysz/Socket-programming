FROM gcc:4.9
ADD main.c /
RUN gcc -std=c11 -o main.out main.c
ENTRYPOINT ["./main.out"]