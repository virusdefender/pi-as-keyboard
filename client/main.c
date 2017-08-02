#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/input.h>


void perror_exit(char *error) {
    perror(error);
    exit(1);
}

int table[4][2] = {{1, 2},
                   {0, 3},
                   {0, 3},
                   {1, 2}};


int main(int argc, char *argv[]) {
    char *device = NULL;
    char *data = NULL;
    int fd;
    size_t data_len;
    char c;
    struct input_event event;
    int last_state = 0;

    int cur_value, cur_state;

    if (argc != 3) {
        perror_exit("Invalid argument");
    }

    device = argv[1];
    if (device == NULL) {
        perror_exit("Not a valid input event device found");
    }

    data = argv[2];
    data_len = strlen(data);
    if (data_len == 0) {
        perror_exit("Invalid data length");
    }

    for (int i = 0; i < data_len; i++) {
        printf("index %d \n", i);

        c = data[i];
        cur_value = c != '0';
        cur_state = table[last_state][cur_value];

        for (int j = 0;j < 2; j++) {
            event.type = EV_LED;
            event.value = (cur_state & (j + 1)) != 0;
            event.code = (__u16)j;

            // printf("write data last state %d cur state %d code %d value %d\n", last_state, cur_state, event.code, event.value);

            if ((fd = open(device, O_RDWR)) == -1) {
                perror_exit("Unable to open input event device");
            }
            write(fd, &event, sizeof(struct input_event));
            fsync(fd);
            close(fd);
        }
        last_state = cur_state;
    }

    return 0;
}

