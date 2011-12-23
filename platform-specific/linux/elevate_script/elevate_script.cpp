#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

// This elevates scripts to the UID which owns the script
// usage:
// elevate_script /foo/bar/script.sh
int main(int argc, char *argv[])
{
    if(argc != 2) {
        // We must be run with two arguments!
        printf("ERROR! %i\n", argc);
        return -1;
    }

    char *script = argv[1];

    // Find the UID
    struct stat buf;
    lstat(script, &buf);
    int UID = buf.st_uid;

    setuid( UID );

    return system( script );
}
