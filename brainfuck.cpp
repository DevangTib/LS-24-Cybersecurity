#include <stdio.h>
#include <stdlib.h>

#define TAPE_SIZE 30000

void execute_brainfuck(const char *code) {
    char tape[TAPE_SIZE] = {0};
    char *ptr = tape;
    const char *pc = code;
    const char *loop;

    while (*pc) {
        switch (*pc) {
            case '>':
                ++ptr;
                break;
            case '<':
                --ptr;
                break;
            case '+':
                ++(*ptr);
                break;
            case '-':
                --(*ptr);
                break;
            case '.':
                putchar(*ptr);
                break;
            case ',':
                *ptr = getchar();
                break;
            case '[':
                if (*ptr == 0) {
                    int bracket_balance = 1;
                    while (bracket_balance > 0) {
                        ++pc;
                        if (*pc == '[') {
                            ++bracket_balance;
                        } else if (*pc == ']') {
                            --bracket_balance;
                        }
                    }
                }
                break;
            case ']':
                if (*ptr != 0) {
                    int bracket_balance = 1;
                    while (bracket_balance > 0) {
                        --pc;
                        if (*pc == '[') {
                            --bracket_balance;
                        } else if (*pc == ']') {
                            ++bracket_balance;
                        }
                    }
                }
                break;
            default:
                // Ignore any non-Brainfuck characters
                break;
        }
        ++pc;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s \"<brainfuck code>\"\n", argv[0]);
        return 1;
    }

    execute_brainfuck(argv[1]);

    return 0;
}